import pandas as pd
import streamlit as st
import plotly.express as px
import os

def generate_performance_report(file_path):
    """
    Generates a visual performance report from the student_performance.csv file.
    """
    # Verify file existence
    if not os.path.exists(file_path):
        st.warning("No performance data found yet. Please run a session first.")
        return

    # Load data
    df = pd.read_csv(file_path)
    
    if df.empty:
        st.info("The performance log is currently empty.")
        return

    st.header("📊 Student Performance Report")
    
    # 1. Emotional Distribution (Pie Chart)
    st.subheader("Emotional State Overview")
    emotion_counts = df['Emotion'].value_counts().reset_index()
    emotion_counts.columns = ['Emotion', 'Frequency']
    
    fig = px.pie(emotion_counts, values='Frequency', names='Emotion', 
                 title="Time Spent in Each Emotional State", hole=0.3)
    st.plotly_chart(fig, use_container_width=True)

    # 2. Key Session Statistics
    st.subheader("Key Session Statistics")
    col1, col2, col3 = st.columns(3)
    
    col1.metric("Total Data Points", len(df))
    
    # Calculate dominant emotion
    dominant = df['Emotion'].mode()[0]
    col2.metric("Dominant Emotion", dominant)
    
    # Calculate average confidence
    if 'ConfidenceScore' in df.columns:
        avg_score = df['ConfidenceScore'].mean()
        col3.metric("Avg Confidence", f"{avg_score:.1f}/10")
    
    # 3. Raw Data Table
    with st.expander("View Raw Session Data"):
        st.dataframe(df)