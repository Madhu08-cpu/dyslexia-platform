import streamlit as st
import random

def run_game():
    st.subheader("🎯 Focus & Reaction Challenge")
    st.write("Test your hand-eye coordination and reflex speed!")

    if 'reaction_score' not in st.session_state: st.session_state.reaction_score = 0
    if 'target_pos' not in st.session_state: st.session_state.target_pos = random.randint(0, 3)

    st.write(f"**Score:** {st.session_state.reaction_score}")
    st.write("Click the button that currently has the target **⭐** as fast as you can!")

    cols = st.columns(4)
    for i in range(4):
        with cols[i]:
            label = "⭐ CATCH ME!" if i == st.session_state.target_pos else "· · ·"
            if st.button(label, key=f"target_{i}"):
                if i == st.session_state.target_pos:
                    st.session_state.reaction_score += 1
                    st.success("Got it! +1")
                else:
                    st.warning("Missed! Try the star.")
                
                st.session_state.target_pos = random.randint(0, 3)
                st.rerun()

    if st.button("Reset Score", key="rst_react"):
        st.session_state.reaction_score = 0
        st.rerun()