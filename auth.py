import hashlib
from database import get_db

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = get_db()
    cur = conn.cursor()
    hashed = hash_password(password)
    cur.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, hashed)
    )
    conn.commit()

def login_user(username, password):
    conn = get_db()
    cur = conn.cursor()
    hashed = hash_password(password)
    cur.execute(
        "SELECT id FROM users WHERE username=? AND password=?",
        (username, hashed)
    )
    user = cur.fetchone()
    return user[0] if user else None


