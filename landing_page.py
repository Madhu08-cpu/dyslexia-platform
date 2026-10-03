import streamlit as st

def run_landing_page():
    # --- Hero Section ---
    st.markdown("### 📚 SMART • ACCESSIBLE • PERSONALIZED")
    st.title("Intelligent Reading & Learning Platform")
    st.write(
        "An advanced multi-tenant educational ecosystem designed for accessible reading support, "
        "vocabulary tracking, milestone goals, and seamless institutional management."
    )
    
    st.markdown("---")
    st.subheader("What Our Platform Does For You")
    st.write("Powerful learning tools designed for students, educators, parents, and institutions.")
    
    st.write("")

    # --- Feature Grid Cards using Columns ---
    col1, col2 = st.columns(2, gap="large")

    with col1:
        with st.container(border=True):
            st.markdown("### 📖 Emotion-Aware Reading")
            st.write("Features synchronized text-to-speech, adjustable font scaling, and reading controls tailored for dyslexia and accessible learning support.")
        
        st.write("")
        
        with st.container(border=True):
            st.markdown("### 🎯 Goals & Milestone Tracking")
            st.write("Empowers students to set custom weekly targets across reading sessions and vocabulary vaults with instant progress metrics.")

        st.write("")

        with st.container(border=True):
            st.markdown("### 🔊 Text-to-Speech Accessibility")
            st.write("Listen to learning content with synchronized audio support for an immersive and accessible reading experience.")

    with col2:
        with st.container(border=True):
            st.markdown("### 🧠 Vocabulary Vault & Brain Games")
            st.write("Save challenging words on the fly into a personal dictionary and keep cognitive skills sharp with interactive word games.")
        
        st.write("")
        
        with st.container(border=True):
            st.markdown("### 👩‍🏫 Educator & Parent Portal")
            st.write("Hierarchical location selection allowing teachers to assign tasks and track student progress seamlessly.")

        st.write("")

        with st.container(border=True):
            st.markdown("### 📊 Progress Analytics & Reports")
            st.write("Monitor reading activity, vocabulary growth, game performance, and learning milestones with exportable reports.")

    # --- Footer Section ---
    st.markdown("---")
    st.markdown("### 🚀 Project Team")
    st.write("**Department of Artificial Intelligence & Machine Learning (AIML)** | Academic Year 2026")
    st.write("Engineered for robust multi-user accessibility and academic excellence.")