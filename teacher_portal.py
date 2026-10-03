import streamlit as st
import pandas as pd
import os

def run_teacher_portal():
    st.title("👩‍🏫 Teacher & Parent Portal")
    st.write("Monitor student progress, reading streaks, and overall platform analytics.")
    
    # 1. Student Accounts Overview
    st.subheader("📋 Registered Students Overview")
    if os.path.exists('users.csv'):
        df_users = pd.read_csv('users.csv')
        # Hide sensitive passwords for privacy/safety
        if 'Password' in df_users.columns:
            display_users = df_users.drop(columns=['Password'])
        else:
            display_users = df_users
            
        st.dataframe(display_users, use_container_width=True)
    else:
        st.info("No student accounts registered yet.")
        
    st.divider()
    
    # 2. Performance Analytics Overview
    st.subheader("📊 Student Performance Log")
    FILE_NAME = 'student_performance.csv'
    if os.path.exists(FILE_NAME):
        df_perf = pd.read_csv(FILE_NAME)
        if 'Timestamp' in df_perf.columns and 'Time' not in df_perf.columns:
            df_perf.rename(columns={'Timestamp': 'Time'}, inplace=True)
            
        # Summary Metrics
        total_records = len(df_perf)
        avg_acc = df_perf['Accuracy'].mean() if 'Accuracy' in df_perf.columns and total_records > 0 else 0.0
        
        col1, col2 = st.columns(2)
        col1.metric("Total Reading Sessions Logged", total_records)
        col2.metric("Class Average Accuracy", f"{avg_acc:.2f}%")
        
        st.write("### Detailed Session History")
        st.dataframe(df_perf, use_container_width=True)
    else:
        st.info("No performance sessions recorded yet.")