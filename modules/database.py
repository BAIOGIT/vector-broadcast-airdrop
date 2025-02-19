import sqlite3

def setup_database(db_path):
    """
    Sets up the database and ensures the `trades` table exists.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            signature TEXT UNIQUE,
            caption TEXT UNIQUE DEFAULT NULL,
            status TEXT DEFAULT 'found', -- 'found', 'broadcasted', 'done'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn

def get_transactions_hashes(db_path):
    """
    Fetches the transaction hashes from the database.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT signature FROM trades
    ''')
    return [row[0] for row in cursor.fetchall()]