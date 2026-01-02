import bcrypt
from database import get_db

def register_user(username, password):
    conn = get_db()
    cur = conn.cursor()
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    cur.execute("INSERT INTO users VALUES (NULL, ?, ?)", (username, hashed))
    conn.commit()

def login_user(username, password):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, password FROM users WHERE username=?", (username,))
    user = cur.fetchone()
    if user and bcrypt.checkpw(password.encode(), user[1]):
        return user[0]
    return None
