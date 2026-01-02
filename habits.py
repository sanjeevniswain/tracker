import pandas as pd
from database import get_db

# -----------------------------
# SAVE DAILY LOG
# -----------------------------
def save_log(user_id, date, vocab_done, vocab_words, exercise, study, notes):
    conn = get_db()
    cur = conn.cursor()

    # Ensure one entry per user per day
    cur.execute(
        "DELETE FROM daily_log WHERE user_id=? AND date=?",
        (user_id, date)
    )

    cur.execute("""
        INSERT INTO daily_log (
            user_id,
            date,
            vocab_done,
            vocab_words,
            exercise_minutes,
            study_minutes,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        date,
        int(vocab_done),
        vocab_words,
        exercise,
        study,
        notes
    ))

    conn.commit()

# -----------------------------
# SHARED STREAKS (COUNT-BASED)
# -----------------------------
def get_streaks():
    conn = get_db()
    users = pd.read_sql("SELECT id, username FROM users", conn)
    logs = pd.read_sql(
        "SELECT DISTINCT user_id, date FROM daily_log",
        conn
    )

    streaks = {}
    for _, user in users.iterrows():
        streaks[user.username] = len(
            logs[logs.user_id == user.id]
        )

    return streaks

# -----------------------------
# TODAY'S LOG
# -----------------------------
def get_today_log(user_id, date):
    conn = get_db()
    query = """
    SELECT *
    FROM daily_log
    WHERE user_id = ? AND date = ?
    """
    return pd.read_sql(query, conn, params=(user_id, date))

# -----------------------------
# LAST N DAYS PROGRESS
# -----------------------------
def get_last_n_days(user_id, n=7):
    conn = get_db()
    query = """
    SELECT
        date,
        vocab_done,
        exercise_minutes,
        study_minutes
    FROM daily_log
    WHERE user_id = ?
    ORDER BY date DESC
    LIMIT ?
    """
    return pd.read_sql(query, conn, params=(user_id, n))

