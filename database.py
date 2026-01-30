import sqlite3
import hashlib
import os
import json
from datetime import datetime

DB_NAME = "tutor_db.sqlite"

def init_db():
    """Initialize the database with users and progress tables."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # User Table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password_hash TEXT, created_at TEXT)''')
    
    # Progress Table
    c.execute('''CREATE TABLE IF NOT EXISTS progress
                 (username TEXT PRIMARY KEY, 
                  current_goal TEXT, 
                  current_module TEXT, 
                  completed_modules TEXT,
                  last_updated TEXT)''')
    
    conn.commit()
    conn.close()
    print(f"✅ Database {DB_NAME} initialized.")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password):
    """Register a new user."""
    if not username or not password:
        return False, "Username and password cannot be empty."
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    try:
        hashed = hash_password(password)
        c.execute("INSERT INTO users VALUES (?, ?, ?)", 
                  (username, hashed, datetime.now().isoformat()))
        conn.commit()
        return True, "User registered successfully!"
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    finally:
        conn.close()

def verify_login(username, password):
    """Verify user credentials."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    hashed = hash_password(password)
    c.execute("SELECT password_hash FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    
    if result and result[0] == hashed:
        return True
    return False

def save_progress(username, goal, module):
    """Update the user's current progress."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Check if entry exists
    c.execute("SELECT completed_modules FROM progress WHERE username=?", (username,))
    row = c.fetchone()
    
    completed = []
    if row:
        completed = json.loads(row[0])
    
    # Add current module to completed list if moving past it? 
    # For now, let's just track current state.
    
    c.execute('''INSERT OR REPLACE INTO progress 
                 (username, current_goal, current_module, completed_modules, last_updated) 
                 VALUES (?, ?, ?, ?, ?)''',
              (username, goal, module, json.dumps(completed), datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

def get_user_progress(username):
    """Retrieve user's last known state."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute("SELECT current_goal, current_module FROM progress WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    
    if row:
        return {"goal": row[0], "module": row[1]}
    return None

# Auto-initialize on import
init_db()
