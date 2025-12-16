import sqlite3
import os

DB = "APImiddleware.db"

def get_db_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row #Accessing columns by name
    return conn

def init_db():
    conn = get_db_conn()
    cursor = conn.cursor()
    
    # Create users table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    
    # Create api_keys table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS api_keys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        api_key TEXT NOT NULL,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_used TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')

    # Creating api_key usage table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS api_usage(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        api_key_id INTEGER NOT NULL,
        endpoint TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (api_key_id) REFERENCES api_keys(id)   
    )     
    ''')

    try:
        cursor.execute("SELECT last_used FROM api_keys LIMIT 1")
    except:
        cursor.execute("ALTER TABLE api_keys ADD COLUMN last_used TIMESTAMP")
    
    # Check if table was created
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    if cursor.fetchone():
        print("Users table exists")
    else:
        print("Failed to create users table")
    
    conn.commit()
    conn.close()




