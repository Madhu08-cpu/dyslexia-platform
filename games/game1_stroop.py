import streamlit as st
import random

def run_game():
    st.subheader("🎨 Stroop Effect Challenge")
    st.write("**Rule:** Select the **INK COLOR** of the word shown below, NOT the word itself! This trains cognitive flexibility and focus.")

    colors = ["Red", "Blue", "Green", "Orange", "Purple"]
    color_codes = {"Red": "red", "Blue": "blue", "Green": "green", "Orange": "orange", "Purple": "purple"}

    if 'stroop_score' not in st.session_state: st.session_state.stroop_score = 0
    if 'target_word' not in st.session_state: st.session_state.target_word = random.choice(colors)
    if 'target_color' not in st.session_state: st.session_state.target_color = random.choice(colors)

    word_display = st.session_state.target_word
    ink_color = color_codes[st.session_state.target_color]

    st.markdown(
        f"<h1 style='text-align: center; color: {ink_color}; font-size: 60px;'>{word_display}</h1>", 
        unsafe_allow_html=True
    )

    st.write("")
    st.write("What is the **INK COLOR** of the word above?")

    cols = st.columns(len(colors))
    for i, col in enumerate(cols):
        with col:
            if st.button(colors[i], key=f"stroop_{colors[i]}"):
                if colors[i] == st.session_state.target_color:
                    st.session_state.stroop_score += 1
                    st.success("Correct! 🎉")
                else:
                    st.error(f"Wrong! The ink was {st.session_state.target_color}.")
                
                st.session_state.target_word = random.choice(colors)
                st.session_state.target_color = random.choice(colors)
                st.rerun()

    st.write(f"### Current Score: {st.session_state.stroop_score}")
    if st.button("Reset Score", key="rst_stroop"):
        st.session_state.stroop_score = 0
        st.rerun()