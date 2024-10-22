import sqlite3

def setup_database():
    conn = sqlite3.connect('rule_engine.db')
    cursor = conn.cursor()

    # Create the rules table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rule_string TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_database()
