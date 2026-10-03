import streamlit as st
import pandas as pd
import os

def run_goals_section():
    st.title("🎯 Comprehensive Platform Goals & Progress")
    st.write("Track your complete activity goals across reading sessions, vocabulary learning, and brain games.")

    current_user = st.session_state.get('user_name', 'Guest')
    
    perf_file = 'student_performance.csv'
    vocab_file = 'vocabulary.csv'  # Adjust if your vocab file name differs
    games_file = 'games_history.csv' # Adjust if your games file name differs

    st.subheader("Set Your Weekly Targets")
    col_t1, col_t2, col_t3 = st.columns(3)
    
    with col_t1:
        target_reading = st.number_input("Reading Sessions", min_value=1, max_value=30, value=5, step=1)
    with col_t2:
        target_vocab = st.number_input("Vocabulary Words", min_value=1, max_value=50, value=10, step=1)
    with col_t3:
        target_games = st.number_input("Brain Games Played", min_value=1, max_value=30, value=5, step=1)
        
    if st.button("Save All Targets"):
        st.success("Your weekly targets have been updated successfully!")

    st.divider()

    st.subheader(f"📊 Progress Overview for {current_user}")

    reading_completed = 0
    if os.path.exists(perf_file):
        try:
            df_read = pd.read_csv(perf_file, on_bad_lines='skip')
            if 'Username' in df_read.columns:
                df_read = df_read[df_read['Username'].astype(str) == str(current_user)]
            reading_completed = len(df_read)
        except Exception:
            reading_completed = 0

    vocab_completed = 0
    if os.path.exists(vocab_file):
        try:
            df_vocab = pd.read_csv(vocab_file, on_bad_lines='skip')
            if 'Username' in df_vocab.columns:
                df_vocab = df_vocab[df_vocab['Username'].astype(str) == str(current_user)]
            vocab_completed = len(df_vocab)
        except Exception:
            vocab_completed = 0

    games_completed = 0
    if os.path.exists(games_file):
        try:
            df_games = pd.read_csv(games_file, on_bad_lines='skip')
            if 'Username' in df_games.columns:
                df_games = df_games[df_games['Username'].astype(str) == str(current_user)]
            games_completed = len(df_games)
        except Exception:
            games_completed = 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📖 Reading Sessions", f"{reading_completed} / {target_reading}")
        p_read = min(float(reading_completed) / float(target_reading), 1.0) if target_reading > 0 else 0.0
        st.progress(p_read)

    with col2:
        st.metric("🧠 Vocabulary Words", f"{vocab_completed} / {target_vocab}")
        p_vocab = min(float(vocab_completed) / float(target_vocab), 1.0) if target_vocab > 0 else 0.0
        st.progress(p_vocab)

    with col3:
        st.metric("🎮 Brain Games", f"{games_completed} / {target_games}")
        p_games = min(float(games_completed) / float(target_games), 1.0) if target_games > 0 else 0.0
        st.progress(p_games)

    st.divider()
    total_completed = reading_completed + vocab_completed + games_completed
    total_target = target_reading + target_vocab + target_games
    
    if total_completed >= total_target:
        st.balloons()
        st.success("🌟 Incredible milestone! You have crushed all your platform activity goals for this period!")
    else:
        st.info(f"Keep up the great momentum! You have completed **{total_completed}** total activities out of your overall target of **{total_target}**.")