import streamlit as st
import random

def run_game():
    st.subheader("🔤 Letter Reversal & Discrimination")
    st.write("Train visual-orthographic tracking by finding the **target letter** among commonly reversed mirror pairs (like **b**, **d**, **p**, **q**).")

    pairs = [
        ("Find the letter: **b**", ["d", "b", "p", "d"], "b"),
        ("Find the letter: **d**", ["b", "p", "d", "q"], "d"),
        ("Find the letter: **p**", ["q", "p", "b", "d"], "p"),
        ("Find the letter: **q**", ["d", "p", "q", "b"], "q"),
    ]

    if 'reversal_score' not in st.session_state: st.session_state.reversal_score = 0
    if 'current_round' not in st.session_state: st.session_state.current_round = random.choice(pairs)

    prompt, options, correct_answer = st.session_state.current_round

    st.write(f"### {prompt}")
    st.write(f"**Score:** {st.session_state.reversal_score}")

    cols = st.columns(len(options))
    for i, col in enumerate(cols):
        with col:
            if st.button(f"{options[i].upper()}", key=f"rev_{i}_{options[i]}"):
                if options[i] == correct_answer:
                    st.session_state.reversal_score += 1
                    st.success("Great job! Correct orientation. 🎉")
                else:
                    st.error(f"Incorrect. Look closely at the curves!")
                
                st.session_state.current_round = random.choice(pairs)
                st.rerun()

    if st.button("Reset Score", key="rst_rev"):
        st.session_state.reversal_score = 0
        st.rerun()