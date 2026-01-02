import streamlit as st

# -----------------------------
# SAFE STARTUP + DEBUG
# -----------------------------
try:
    from datetime import date
    from database import create_tables
    from auth import login_user, register_user
    from habits import (
        save_log,
        get_streaks,
        get_today_log,
        get_last_n_days
    )
    from ai_vocab import get_vocab

    create_tables()

except Exception as e:
    st.error("❌ Startup error")
    st.exception(e)
    st.stop()

# -----------------------------
# APP CONFIG
# -----------------------------
st.set_page_config(
    page_title="Daily Routine Tracker ❤️",
    layout="centered"
)

st.title("🌱 Daily Routine Tracker")

# -----------------------------
# AUTH SECTION
# -----------------------------
if "user_id" not in st.session_state:

    st.subheader("Login / Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    # LOGIN
    with col1:
        if st.button("Login"):
            if not username.strip() or not password.strip():
                st.error("❌ Please enter username and password")
            else:
                user_id = login_user(username.strip(), password)
                if user_id:
                    st.session_state.user_id = user_id
                    st.session_state.username = username.strip()
                    st.success("Logged in successfully ❤️")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")

    # REGISTER
    with col2:
        if st.button("Register"):
            if not username.strip():
                st.error("❌ Username cannot be empty")
            elif not password.strip():
                st.error("❌ Password cannot be empty")
            elif len(password) < 4:
                st.error("❌ Password must be at least 4 characters")
            else:
                try:
                    register_user(username.strip(), password)
                    st.success("✅ Registered successfully! Please login.")
                except Exception as e:
                    if "UNIQUE constraint failed" in str(e):
                        st.error("❌ Username already exists")
                    else:
                        st.error("❌ Registration failed")
                        st.exception(e)

# -----------------------------
# MAIN APP
# -----------------------------
else:
    st.success(f"Welcome, {st.session_state.username} ❤️")

    today = date.today().isoformat()

    st.header("📅 Today's Habits")

    vocab_done = st.checkbox("Learned English Vocabulary today")
    vocab_words = st.text_area("Words learned (optional)")

    exercise = st.slider("Exercise (minutes)", 0, 60, 20)
    study = st.slider("Focused Study (minutes)", 0, 180, 60)

    notes = st.text_area("Notes / Reflection")

    if st.button("💾 Save Today"):
        save_log(
            st.session_state.user_id,
            today,
            vocab_done,
            vocab_words,
            exercise,
            study,
            notes
        )
        st.success("Today's progress saved ✅")

    # -----------------------------
    # TODAY'S SUMMARY
    # -----------------------------
    st.divider()
    st.subheader("📊 Today's Summary")

    today_df = get_today_log(st.session_state.user_id, today)

    if today_df.empty:
        st.info("No data logged for today yet.")
    else:
        row = today_df.iloc[0]
        st.write(f"🧠 Vocabulary learned: {'Yes' if row['vocab_done'] else 'No'}")
        st.write(f"🏃 Exercise: {row['exercise_minutes']} minutes")
        st.write(f"📚 Focused study: {row['study_minutes']} minutes")

        if row["exercise_minutes"] >= 20:
            st.success("✅ Exercise goal met")
        if row["study_minutes"] >= 60:
            st.success("✅ Study goal met")

    # -----------------------------
    # LAST 7 DAYS PROGRESS
    # -----------------------------
    st.divider()
    st.subheader("📈 Last 7 Days Progress")

    last_7_df = get_last_n_days(st.session_state.user_id, 7)

    if last_7_df.empty:
        st.info("Start logging to see your weekly progress.")
    else:
        st.dataframe(last_7_df)

    # -----------------------------
    # SHARED STREAKS
    # -----------------------------
    st.divider()
    st.subheader("🔥 Streaks (You & Partner)")

    streaks = get_streaks()
    for user, streak in streaks.items():
        st.write(f"❤️ **{user}** — {streak} days")

    # -----------------------------
    # VOCAB
    # -----------------------------
    st.divider()
    st.subheader("🧠 Word of the Day")

    word, meaning, example = get_vocab()
    st.markdown(f"""
    **Word:** {word}  
    **Meaning:** {meaning}  
    _Example:_ {example}
    """)

    # -----------------------------
    # GENTLE REMINDER
    # -----------------------------
    if exercise == 0 and study == 0:
        st.info("🌸 Gentle reminder: even 10 minutes counts today.")

    # -----------------------------
    # LOGOUT
    # -----------------------------
    st.divider()
    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()
