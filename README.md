# ZeoTap Rule Engine with AST

## Objective
Develop a simple 3-tier rule engine application (Simple UI, API, and Backend Data) to determine user eligibility based on attributes like age, department, income, spending, etc. The system uses an Abstract Syntax Tree (AST) to represent conditional rules and allows for dynamic creation, combination, and modification of these rules.

## Features
- **AST Representation**: Utilizes an Abstract Syntax Tree to effectively represent conditional rules.
- **Animated UI**: Incorporates animations for a smoother user experience, making interactions more engaging.
- **Dynamic Rule Management**: Enables the creation, combination, and modification of rules in real-time.
- **Eligibility Evaluation**: Evaluates user eligibility based on defined rules and user attributes.
- **Web-Based Interface**: Provides a simple and intuitive user interface for rule management with animated UI elements for enhanced user experience.
- **API Integration**: Exposes API endpoints for rule creation and evaluation, facilitating easy integration with other systems.
- **Error Handling**: Implements robust error handling for invalid rule strings or data formats.
- **Attribute Validation**: Validates attributes to be part of a catalog, ensuring data integrity.
- **User-Defined Functions**: Supports user-defined functions for advanced conditions (future enhancement).
- **create_rule(rule_string)**: Takes a string representing a rule and returns a Node object representing the corresponding AST.
- **combine_rules(rules)**: Takes a list of rule strings and combines them into a single AST, optimizing for efficiency and minimizing redundant checks.
- **evaluate_rule(JSON data)**: Takes a JSON representing the combined rule's AST and a dictionary of attributes, evaluates the rule, and returns `True` or `False`.

## Additional Features
- **Real-Time Rule Feedback**: Provides immediate feedback on rule validity and user eligibility as rules are modified.
- **Dashboard Analytics**: Displays analytics on rule usage and user eligibility statistics.
- **Customizable Themes**: Allows users to choose from different themes for the UI, enhancing personalization.
- **Documentation and Tutorials**: Includes comprehensive documentation and tutorials for users to understand how to create and manage rules effectively.

# Result: 
[recording.webm](https://github.com/user-attachments/assets/5f6d7641-f1c9-4f20-b7be-a12e95ffe029)


## Data Structure
### Node Structure
The data structure for representing the AST is defined as follows:

```python
class Node:
    def __init__(self, type: str, left=None, right=None, value=None):
        self.type = type  # "operator" for AND/OR, "operand" for conditions
        self.left = left  # Reference to another Node (left child)
        self.right = right  # Reference to another Node (right child for operators)
        self.value = value  # Optional value for operand nodes (e.g., number for comparisons)
```


## Installation
To install and run the application, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/pukumars2003/ZeoTap-Rule-Engine.git
   cd ZeoTap-Rule-Engine
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the database:
   ```bash
   python setup_database.py
   ```
4. Run the application:
   ```bash
   python app.py
   ```

## License
This project does not specify a license, so the default copyright applies.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

