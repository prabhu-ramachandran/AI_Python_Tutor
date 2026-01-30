import sqlite3
import hashlib
import os
import json
from datetime import datetime

# Determine DB Path (Hugging Face Spaces often needs /tmp or a specific data dir)
DB_NAME = "tutor_db.sqlite"
if not os.access(".", os.W_OK):
    DB_NAME = "/tmp/tutor_db.sqlite"

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

def save_progress(username, goal, module, metrics=None):
    """Update the user's current progress and save metrics."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Check if entry exists
    c.execute("SELECT completed_modules FROM progress WHERE username=?", (username,))
    row = c.fetchone()
    
    completed_data = {}
    if row:
        try:
            loaded = json.loads(row[0])
            # Migration: If it was a list (old format), convert to dict
            if isinstance(loaded, list):
                completed_data = {m: {"steps": 0, "score": 0} for m in loaded}
            else:
                completed_data = loaded
        except:
            completed_data = {}
    
    # Save the metrics for the *completed* module
    # Note: 'module' here is usually the NEXT module we are moving TO.
    # The metrics provided are for the module we just FINISHED.
    # We might need to adjust logic in app.py to pass the correct finished module name.
    # For now, let's assume 'metrics' contains the name of the finished module too if needed,
    # or we handle it by passing the *finished* module as an argument.
    
    # Actually, simpler: The app calls this when a module is done.
    # Let's assume 'module' passed here is the NEW state, but we want to record metrics for the PREVIOUS state?
    # No, usually we save "I just finished Module X, here are its stats".
    
    if metrics and "completed_module_name" in metrics:
        mod_name = metrics["completed_module_name"]
        completed_data[mod_name] = {
            "steps": metrics.get("steps", 0),
            "timestamp": datetime.now().isoformat(),
            "efficiency_score": max(100 - (metrics.get("steps", 0) * 2), 10) # Simple heuristic
        }
    
    c.execute('''INSERT OR REPLACE INTO progress 
                 (username, current_goal, current_module, completed_modules, last_updated) 
                 VALUES (?, ?, ?, ?, ?)''',
              (username, goal, module, json.dumps(completed_data), datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

def ensure_user_exists(username):
    """Ensure a user exists in the DB (for OAuth users)."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT username FROM users WHERE username=?", (username,))
    if not c.fetchone():
        # Create user with a dummy password since they use OAuth
        hashed = hash_password("oauth_user") 
        c.execute("INSERT INTO users VALUES (?, ?, ?)", 
                  (username, hashed, datetime.now().isoformat()))
        conn.commit()
    conn.close()

def get_user_progress(username):
    """Retrieve user's last known state and completion history."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute("SELECT current_goal, current_module, completed_modules FROM progress WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    
    if row:
        completed = {}
        try:
            completed = json.loads(row[2])
        except:
            pass
        return {"goal": row[0], "module": row[1], "completed": completed}
    return None

# Auto-initialize on import
init_db()
