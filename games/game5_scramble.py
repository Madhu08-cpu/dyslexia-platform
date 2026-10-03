import streamlit as st
import random

def run_game():
    st.subheader("🔤 Speed Word Scramble")
    st.write("Unscramble the letters to find the correct reading word! This builds phonological awareness and orthographic processing.")

    word_bank = ["apple", "tiger", "house", "brain", "smart", "quick", "plant", "water"]

    if 'scramble_score' not in st.session_state: st.session_state.scramble_score = 0
    if 'target_word_scramble' not in st.session_state:
        word = random.choice(word_bank)
        scrambled = "".join(random.sample(word, len(word)))
        st.session_state.target_word_scramble = word
        st.session_state.scrambled_display = scrambled

    st.write(f"**Score:** {st.session_state.scramble_score}")
    st.markdown(f"### Unscramble this word: **{st.session_state.scrambled_display.upper()}**")

    user_guess = st.text_input("Type your guessed word here:", key="scramble_input")

    if st.button("Submit Guess", key="submit_scramble"):
        if user_guess.strip().lower() == st.session_state.target_word_scramble:
            st.session_state.scramble_score += 1
            st.success("Correct! Great spelling job! 🎉")
            word = random.choice(word_bank)
            st.session_state.target_word_scramble = word
            st.session_state.scrambled_display = "".join(random.sample(word, len(word)))
            st.rerun()
        else:
            st.error("Not quite right, try again!")

    if st.button("Reset Score", key="rst_scramble"):
        st.session_state.scramble_score = 0
        st.rerun()