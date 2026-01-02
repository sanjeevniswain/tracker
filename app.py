import streamlit as st
from datetime import date
from database import create_tables
from auth import login_user, register_user
from habits import save_log, get_streaks
from ai_vocab import get_vocab

st.set_page_config(page_title="Daily Routine Tracker ❤️", layout="centered")
create_tables()

st.title("🌱 Daily Routine Tracker")

if "user_id" not in st.session_state:
    st.subheader("Login / Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)
    if col1.button("Login"):
        user_id = login_user(username, password)
        if user_id:
            st.session_state.user_id = user_id
            st.session_state.username = username
            st.success("Logged in!")
            st.rerun()
        else:
            st.error("Invalid credentials")

    if col2.button("Register"):
        register_user(username, password)
        st.success("Registered! Please login.")

else:
    st.success(f"Welcome {st.session_state.username} ❤️")

    today = date.today().isoformat()

    st.header("📅 Today's Habits")

    vocab_done = st.checkbox("Learned English Vocabulary")
    vocab_words = st.text_area("Words learned")

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
        st.success("Saved successfully!")

    st.divider()

    st.header("🔥 Streaks (You & Partner)")
    streaks = get_streaks()
    for user, streak in streaks.items():
        st.write(f"❤️ **{user}**: {streak} days")

    st.divider()

    st.header("🧠 AI Daily Vocabulary")
    word, meaning, example = get_vocab()
    st.markdown(f"""
    **Word:** {word}  
    **Meaning:** {meaning}  
    _Example:_ {example}
    """)
