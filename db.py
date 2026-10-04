import os
import sqlite3
import bcrypt

DB_FILE = "users.db"


def get_db_connection():
  """Establish a connection to the SQLite database."""
  conn = sqlite3.connect(DB_FILE, check_same_thread=False)
  conn.row_factory = sqlite3.Row
  return conn


def init_db():
  """Initialize the SQLite database schema if it doesn't exist."""
  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash BLOB NOT NULL,
            role TEXT DEFAULT 'Student',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
  conn.commit()
  conn.close()


def register_user(username: str, password: str, role: str = "Student") -> bool:
  """Hash the password and insert a new user into the database."""
  init_db()  # Ensure table exists

  # Generate salt and hash password
  salt = bcrypt.gensalt()
  password_hash = bcrypt.hashpw(password.encode("utf-8"), salt)

  conn = get_db_connection()
  cursor = conn.cursor()
  try:
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role),
    )
    conn.commit()
    return True
  except sqlite3.IntegrityError:
    # Username already exists
    return False
  finally:
    conn.close()


def authenticate_user(username: str, password: str):
  """Verify username and password against stored hash."""
  init_db()  # Ensure table exists

  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute(
      "SELECT username, password_hash, role FROM users WHERE username = ?",
      (username,),
  )
  user = cursor.fetchone()
  conn.close()

  if user:
    stored_hash = user["password_hash"]
    # Check provided password against stored bcrypt hash
    if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
      return {"username": user["username"], "role": user["role"]}

  return None