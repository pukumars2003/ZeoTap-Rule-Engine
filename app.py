import re
from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

class ASTNode:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # "operator" or "operand"
        self.left = left
        self.right = right
        self.value = value  # For operands, should be a tuple (attribute, operator, value)

    def to_dict(self):
        """Convert ASTNode to a dictionary for JSON serialization."""
        if self.type == "operand":
            return {
                "type": "operand",
                "value": self.value
            }
        else:
            return {
                "type": "operator",
                "value": self.value,
                "left": self.left.to_dict() if self.left else None,
                "right": self.right.to_dict() if self.right else None,
            }

def parse_condition(condition):
    """Parse a single condition into an AST node."""
    match = re.match(r"(\w+)\s*([<>!=]+)\s*['\"]?([^'\"]+)['\"]?", condition.strip())
    if match:
        attribute, operator, value = match.groups()
        return ASTNode("operand", value=(attribute, operator, value.strip()))
    return None

def create_rule(rule_string):
    """Create an AST from a rule string."""
    # Split conditions by AND/OR
    tokens = re.split(r'\s+(AND|OR)\s+', rule_string)
    ast_nodes = []

    for token in tokens:
        token = token.strip()
        if token in ["AND", "OR"]:
            continue  # Skip operators in the token list
        ast_node = parse_condition(token)
        if ast_node:
            ast_nodes.append(ast_node)

    # Combine conditions into an AST
    if not ast_nodes:
        return None

    # Build the AST
    root = ast_nodes[0]
    for i in range(1, len(ast_nodes)):
        root = ASTNode("operator", left=root, right=ast_nodes[i], value="AND")
    return root

def combine_rules(rules):
    # Return None if no rules are provided
    if not rules:
        return None
    
    # If there's only one rule, return it directly
    if len(rules) == 1:
        return rules[0]

    # Start combining rules
    combined = rules[0]

    for rule in rules[1:]:
        # Combine each rule with the previous combined result using AND
        combined = ASTNode("operator", left=combined, right=rule, value="AND")

    return combined



def evaluate_rule(ast, data):
    """Evaluate the AST against the provided data."""
    if ast.type == "operand":
        attribute, operator, value = ast.value
        value = int(value) if value.isdigit() else value.strip("'")
        if operator == '>':
            return data.get(attribute, 0) > value
        elif operator == '<':
            return data.get(attribute, 0) < value
        elif operator == '=':
            return data.get(attribute) == value
        elif operator == '!=':
            return data.get(attribute) != value
    elif ast.type == "operator":
        left_result = evaluate_rule(ast.left, data)
        if ast.right:
            right_result = evaluate_rule(ast.right, data)
            if ast.value == "AND":
                return left_result and right_result
            elif ast.value == "OR":
                return left_result or right_result
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_rule', methods=['POST'])
def handle_create_rule():
    rule_string = request.json.get('rule_string')
    ast = create_rule(rule_string)
    if ast:
        conn = sqlite3.connect('rule_engine.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO rules (rule_string) VALUES (?)", (rule_string,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Rule created", "ast": ast.to_dict()}), 201  
    return jsonify({"error": "Invalid rule format"}), 400

@app.route('/combine_rules', methods=['POST'])
def handle_combine_rules():
    rule_ids = request.json.get('rule_ids', [])
    rules = []
    
    conn = sqlite3.connect('rule_engine.db')
    cursor = conn.cursor()
    for rule_id in rule_ids:
        cursor.execute("SELECT rule_string FROM rules WHERE id = ?", (rule_id,))
        rule = cursor.fetchone()
        if rule:
            ast = create_rule(rule[0])
            rules.append(ast)
    conn.close()

    combined_ast = combine_rules(rules)
    return jsonify({"combined_ast": combined_ast.to_dict() if combined_ast else None})

@app.route('/evaluate_rule', methods=['POST'])
def handle_evaluate_rule():
    rule_id = request.json.get('rule_id')
    data = request.json.get('data')

    conn = sqlite3.connect('rule_engine.db')
    cursor = conn.cursor()
    cursor.execute("SELECT rule_string FROM rules WHERE id = ?", (rule_id,))
    rule = cursor.fetchone()
    conn.close()

    if rule:
        ast = create_rule(rule[0])
        result = evaluate_rule(ast, data)
        return jsonify({"result": result})
    return jsonify({"error": "Rule not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
