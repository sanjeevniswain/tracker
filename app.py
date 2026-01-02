import streamlit as st

# -----------------------------
# SAFE STARTUP + DEBUG BLOCK
# -----------------------------
try:
    from datetime import date
    from database import create_tables
    from auth import login_user, register_user
    from habits import save_log, get_streaks
    from ai_vocab import get_vocab

    st.write("✅ App imports successful")

    create_tables()
    st.write("✅ Database initialized")

except Exception as e:
    st.error("❌ Startup error occurred")
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
# AUTHENTICATION
# -----------------------------
if "user_id" not in st.session_state:

    st.subheader("Login / Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            user_id = login_user(username, password)
            if user_id:
                st.session_state.user_id = user_id
                st.session_state.username = username
                st.success("Logged in successfully ❤️")
                st.rerun()
            else:
                st.error("Invalid username or password")

    with col2:
        if st.button("Register"):
            try:
                register_user(username, password)
                st.success("Registered successfully! Please login.")
            except Exception as e:
                st.error("Registration failed")
                st.exception(e)

# -----------------------------
# MAIN APP (LOGGED IN)
# -----------------------------
else:
    st.success(f"Welcome, {st.session_state.username} ❤️")

    today = date.today().isoformat()

    st.header("📅 Today's Habits")

    vocab_done = st.checkbox("Learned English Vocabulary today")
    vocab_words = st.text_area("Words learned (optional)")

    exercise = st.slider("Exercise duration (minutes)", 0, 60, 20)
    study = st.slider("Focused study duration (minutes)", 0, 180, 60)

    notes = st.text_area("Notes / Reflection")

    if st.button("💾 Save Today"):
        try:
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
        except Exception as e:
            st.error("Failed to save today's log")
            st.exception(e)

    # -----------------------------
    # SHARED STREAKS
    # -----------------------------
    st.divider()
    st.header("🔥 Streaks (You & Partner)")

    try:
        streaks = get_streaks()
        for user, streak in streaks.items():
            st.write(f"❤️ **{user}** — {streak} days")
    except Exception as e:
        st.error("Failed to load streaks")
        st.exception(e)

    # -----------------------------
    # AI VOCAB (STATIC FOR NOW)
    # -----------------------------
    st.divider()
    st.header("🧠 Word of the Day")

    try:
        word, meaning, example = get_vocab()
        st.markdown(f"""
        **Word:** {word}  
        **Meaning:** {meaning}  
        _Example:_ {example}
        """)
    except Exception as e:
        st.error("Failed to load vocabulary")
        st.exception(e)

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



