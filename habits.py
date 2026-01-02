from database import get_db
import pandas as pd

def save_log(user_id, date, vocab_done, vocab_words, exercise, study, notes):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM daily_log WHERE user_id=? AND date=?", (user_id, date))
    cur.execute("""
        INSERT INTO daily_log VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, date, int(vocab_done), vocab_words, exercise, study, notes))
    conn.commit()

def get_streaks():
    conn = get_db()
    users = pd.read_sql("SELECT id, username FROM users", conn)
    logs = pd.read_sql("SELECT user_id, date FROM daily_log", conn)

    streaks = {}
    for _, user in users.iterrows():
        user_logs = logs[logs.user_id == user.id]
        streaks[user.username] = len(user_logs)

    return streaks
