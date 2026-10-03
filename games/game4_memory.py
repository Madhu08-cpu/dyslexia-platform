import streamlit as st
import random

def run_game():
    st.subheader("💡 Memory Sequence Flash")
    st.write("Test and improve your short-term working memory by repeating the correct button order sequence!")

    if 'mem_score' not in st.session_state: st.session_state.mem_score = 0
    if 'sequence' not in st.session_state: st.session_state.sequence = [random.choice([1, 2, 3]) for _ in range(3)]
    if 'user_input' not in st.session_state: st.session_state.user_input = []

    st.write(f"**Score:** {st.session_state.mem_score}")
    st.info(f"Target Sequence Pattern to Remember: **{' - '.join(map(str, st.session_state.sequence))}**")
    st.write("Click the sequence numbers in the exact correct order:")

    cols = st.columns(3)
    for i in range(1, 4):
        with cols[i-1]:
            if st.button(f"Press {i}", key=f"mem_btn_{i}"):
                st.session_state.user_input.append(i)
                
                current_idx = len(st.session_state.user_input) - 1
                if st.session_state.user_input[current_idx] != st.session_state.sequence[current_idx]:
                    st.error("Wrong sequence! Try a new pattern.")
                    st.session_state.user_input = []
                    st.session_state.sequence = [random.choice([1, 2, 3]) for _ in range(3)]
                    st.rerun()
                elif len(st.session_state.user_input) == len(st.session_state.sequence):
                    st.session_state.mem_score += 1
                    st.success("Fantastic memory! Sequence matched! 🎉")
                    st.session_state.user_input = []
                    st.session_state.sequence = [random.choice([1, 2, 3]) for _ in range(3)]
                    st.rerun()

    if st.button("Reset Score", key="rst_mem"):
        st.session_state.mem_score = 0
        st.session_state.user_input = []
        st.rerun()