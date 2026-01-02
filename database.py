import sqlite3

def get_db():
    return sqlite3.connect("/tmp/tracker.db", check_same_thread=False)

def create_tables():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS daily_log (
        user_id INTEGER,
        date TEXT,
        vocab_done INTEGER,
        vocab_words TEXT,
        exercise_minutes INTEGER,
        study_minutes INTEGER,
        notes TEXT
    )
    """)

    conn.commit()

