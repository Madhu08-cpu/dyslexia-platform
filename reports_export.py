import streamlit as st
import pandas as pd
import os
import plotly.express as px
from fpdf import FPDF
import tempfile
import datetime

def run_advanced_reports():
    st.title("📋 Comprehensive Clinical Progress Report")
    st.write("Holistic developmental progress summary across reading sessions, vocabulary vault, and brain games tailored for teachers, parents, and specialists.")
    
    current_user = st.session_state.get('user_name', 'Guest')
    
    perf_file = 'student_performance.csv'
    vocab_file = 'vocabulary.csv'
    games_file = 'games_history.csv'
    users_file = 'users.csv'

    # Retrieve User Profile Details
    user_age = "N/A"
    user_gender = "N/A"
    if os.path.exists(users_file):
        try:
            df_u = pd.read_csv(users_file)
            match = df_u[df_u['Name'] == current_user]
            if not match.empty:
                user_age = match.iloc[0].get('Age', 'N/A')
                user_gender = match.iloc[0].get('Gender', 'N/A')
        except Exception:
            pass

    # --- 1. LOAD & FILTER DATA FOR CURRENT USER ---
    # --- 1. LOAD & FILTER DATA FOR CURRENT USER ---
    def load_user_data(filename):
        if os.path.exists(filename):
            try:
                df = pd.read_csv(filename, on_bad_lines='skip')
                if 'Username' in df.columns:
                    df = df[df['Username'] == current_user]
                return df
            except Exception:
                return pd.DataFrame()
        return pd.DataFrame()

    df_read = load_user_data(perf_file)
    
    # Check for any variation of the date/time column and normalize it to 'Time'
    for possible_date_col in ['Timestamp', 'Date', 'Datetime', 'Created_At']:
        if possible_date_col in df_read.columns and 'Time' not in df_read.columns:
            df_read.rename(columns={possible_date_col: 'Time'}, inplace=True)
            break

    # If no date/time column exists at all in the reading file, generate one dynamically from file creation time or row index as a fallback
    if not df_read.empty and 'Time' not in df_read.columns:
        df_read['Time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Safely clean and convert Accuracy to numeric if data exists
    if not df_read.empty and 'Accuracy' in df_read.columns:
        df_read['Accuracy_Numeric'] = df_read['Accuracy'].astype(str).str.rstrip('%').astype(float)
    else:
        df_read['Accuracy_Numeric'] = 0.0

    df_vocab = load_user_data(vocab_file)
    df_games = load_user_data(games_file)
    
    total_sessions = len(df_read)
    avg_accuracy = df_read['Accuracy_Numeric'].mean() if total_sessions > 0 else 0.0
    total_vocab = len(df_vocab)
    total_games = len(df_games)

    # --- UI DISPLAY & CLINICAL HEADER ---
    st.markdown("---")
    col_u1, col_u2, col_u3 = st.columns(3)
    col_u1.write(f"**Student Name:** {current_user}")
    col_u2.write(f"**Age / Gender:** {user_age} / {user_gender}")
    col_u3.write(f"**Report Date:** {datetime.date.today()}")
    st.markdown("---")

    # Comprehensive Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Reading Sessions", total_sessions)
    m2.metric("Avg Accuracy", f"{avg_accuracy:.2f}%")
    m3.metric("Vocabulary Saved", total_vocab)
    m4.metric("Brain Games Played", total_games)
    
    if total_sessions > 0 and 'Time' in df_read.columns:
        st.markdown("---")
        st.write("### 📈 Comprehensive Reading Accuracy Trend")
        fig = px.line(df_read, x='Time', y='Accuracy_Numeric', markers=True, title=f"Performance Over Time - {current_user}")
        fig.update_yaxes(title_text="Accuracy (%)")
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed Records Tables for ALL Activities
    st.markdown("---")
    st.write("### 📖 Detailed Reading Session Records")
    if not df_read.empty:
        # Drop temporary numeric column for display view cleanliness if desired, or keep it
        display_df = df_read.drop(columns=['Accuracy_Numeric'], errors='ignore')
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("No reading records found.")

    st.write("### 🧠 Vocabulary Vault Records")
    if not df_vocab.empty:
        st.dataframe(df_vocab, use_container_width=True)
    else:
        st.info("No vocabulary words saved yet.")

    st.write("### 🎮 Brain Games History Records")
    if not df_games.empty:
        st.dataframe(df_games, use_container_width=True)
    else:
        st.info("No brain games completed yet. Play games from the menu to populate this section.")

    st.markdown("---")
    st.subheader("📥 Export Comprehensive Clinical Report (PDF)")
    
    if st.button("Generate All-Inclusive PDF Summary Report"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 13)
        
        # Header
        pdf.cell(200, 7, txt="NeuroRead AI - Comprehensive Clinical Progress Report", ln=True, align="C")
        pdf.set_font("Arial", "", 10)
        pdf.cell(200, 6, txt=f"Student Name: {current_user} | Age: {user_age} | Gender: {user_gender}", ln=True, align="C")
        pdf.cell(200, 6, txt=f"Date Generated: {datetime.date.today()}", ln=True, align="C")
        pdf.ln(5)
        
        # Summary Statistics
        pdf.set_font("Arial", "B", 10)
        pdf.cell(200, 6, txt="Overall Activity Summary Statistics:", ln=True)
        pdf.set_font("Arial", "", 9)
        pdf.cell(200, 5, txt=f"- Total Reading Sessions Completed: {total_sessions}", ln=True)
        pdf.cell(200, 5, txt=f"- Average Reading Accuracy: {avg_accuracy:.2f}%", ln=True)
        pdf.cell(200, 5, txt=f"- Vocabulary Words Mastered: {total_vocab}", ln=True)
        pdf.cell(200, 5, txt=f"- Brain Games Completed: {total_games}", ln=True)
        pdf.ln(5)
        
        # 1. Reading Logs Section in PDF
        pdf.set_font("Arial", "B", 10)
        pdf.cell(200, 6, txt="1. Reading Session Logs:", ln=True)
        pdf.set_font("Arial", "B", 8)
        pdf.cell(60, 5, "Time", border=1)
        pdf.cell(40, 5, "Accuracy (%)", border=1)
        pdf.cell(50, 5, "Emotion", border=1)
        pdf.ln()
        
        pdf.set_font("Arial", "", 8)
        if not df_read.empty:
            for _, row in df_read.iterrows():
                pdf.cell(60, 5, str(row.get('Time', 'N/A'))[:19], border=1)
                pdf.cell(40, 5, str(row.get('Accuracy', 'N/A')), border=1)
                pdf.cell(50, 5, str(row.get('Emotion', 'N/A')), border=1)
                pdf.ln()
        else:
            pdf.cell(150, 5, "No reading records available.", border=1, ln=True)
        pdf.ln(4)

        # 2. Brain Games Logs Section in PDF
        pdf.set_font("Arial", "B", 10)
        pdf.cell(200, 6, txt="2. Brain Games Activity Logs:", ln=True)
        pdf.set_font("Arial", "B", 8)
        pdf.cell(60, 5, "Time", border=1)
        pdf.cell(60, 5, "Game Name", border=1)
        pdf.cell(40, 5, "Status", border=1)
        pdf.ln()
        
        pdf.set_font("Arial", "", 8)
        if not df_games.empty:
            for _, row in df_games.iterrows():
                pdf.cell(60, 5, str(row.get('Time', 'N/A'))[:19], border=1)
                pdf.cell(60, 5, str(row.get('Game_Name', 'N/A')), border=1)
                pdf.cell(40, 5, str(row.get('Status', 'N/A')), border=1)
                pdf.ln()
        else:
            pdf.cell(160, 5, "No brain game records available.", border=1, ln=True)
            
        # Save to temporary file for download
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            pdf.output(tmp_file.name)
            with open(tmp_file.name, "rb") as pdf_file:
                PDFbyte = pdf_file.read()
                
        st.download_button(
            label="📥 Download Official All-Inclusive PDF Report",
            data=PDFbyte,
            file_name=f"{current_user}_Comprehensive_Clinical_Report.pdf",
            mime="application/pdf"
        )
        st.success("Comprehensive PDF Report generated successfully!")

if __name__ == "__main__":
    run_advanced_reports()