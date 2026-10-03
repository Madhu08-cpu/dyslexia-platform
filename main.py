import streamlit as st
import pandas as pd
import hashlib
import os
import re
import datetime

# Import modular files
import landing_page
import app 
import games_hub
import vocabulary
import profile
import streaks
import goals
import reports_export
import educator_portal

# --- INITIALIZE SESSION STATE IN MAIN ---
if 'status' not in st.session_state: 
    st.session_state.status = 'IDLE'
if 'start_time' not in st.session_state: 
    st.session_state.start_time = None
if 'last_emotion' not in st.session_state: 
    st.session_state.last_emotion = "NEUTRAL"
if 'session_data' not in st.session_state: 
    st.session_state.session_data = []
if 'logged_in' not in st.session_state: 
    st.session_state.logged_in = False

st.set_page_config(page_title="Reading Platform", layout="wide")

def validate_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase letter."
    if not re.search(r"\d", password):
        return "Password must contain at least one number."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Password must contain at least one special character."
    return None

# --- LOGIN & REGISTER ---
if not st.session_state.logged_in:
    st.title("🎓 Student Portal")
    choice = st.sidebar.radio("Navigation", ["Login", "Register"])

    if choice == "Login":
        st.subheader("Login")
        name = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if os.path.exists('users.csv'):
                df = pd.read_csv('users.csv')
                hashed = hashlib.sha256(password.encode()).hexdigest()
                user = df[(df['Name'] == name) & (df['Password'] == hashed)]
                if not user.empty:
                    st.session_state.logged_in = True
                    st.session_state.user_name = name
                    st.rerun()
                else: 
                    st.error("Invalid credentials!")
            else: 
                st.warning("No users registered yet.")
    
    else:
        st.subheader("Register")
        with st.form("reg"):
            name = st.text_input("Full Name")
            pw = st.text_input("Password", type="password", help="Must be 8+ characters with uppercase, lowercase, number, and special character.")
            age = st.number_input("Age", min_value=1, max_value=100)
            phone = st.text_input("Phone Number") 
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            min_date = datetime.date(1900, 1, 1)
            max_date = datetime.date.today()
            dob = st.date_input("Date of Birth", min_value=min_date, max_value=max_date, value=datetime.date(2000, 1, 1))
            address = st.text_area("Address")
            
            if st.form_submit_button("Register"):
                if name and pw:
                    password_error = validate_password(pw)
                    if password_error:
                        st.error(password_error)
                    else:
                        hashed = hashlib.sha256(pw.encode()).hexdigest()
                        file_exists = os.path.exists('users.csv')
                        if file_exists:
                            df_existing = pd.read_csv('users.csv')
                            if not df_existing.empty and 'Name' in df_existing.columns and name in df_existing['Name'].values:
                                st.error("User with this name already exists. Please choose another or login.")
                            else:
                                new_user = pd.DataFrame({
                                    'Name': [name], 'Password': [hashed], 'Age': [age], 
                                    'Phone': [phone], 'Gender': [gender], 'DOB': [str(dob)], 'Address': [address],
                                    'Streak': [0], 'Last_Read_Date': [""]
                                })
                                new_user.to_csv('users.csv', mode='a', header=False, index=False)
                                st.success("Registered successfully! Please login.")
                        else:
                            new_user = pd.DataFrame({
                                'Name': [name], 'Password': [hashed], 'Age': [age], 
                                'Phone': [phone], 'Gender': [gender], 'DOB': [str(dob)], 'Address': [address],
                                'Streak': [0], 'Last_Read_Date': [""]
                            })
                            new_user.to_csv('users.csv', mode='a', header=True, index=False)
                            st.success("Registered successfully! Please login.")
                else: 
                    st.error("Name and Password are required.")

# --- DASHBOARD & ROUTING ---
else:
    menu = st.sidebar.radio("Platform Menu", [ "Dashboard", "Edit Profile", "Start Reading", "Vocabulary Vault", "Reading Goals", "Reports", "Brain Games", "Educator Portal"])

    if menu == "Home / Welcome":
        landing_page.run_landing_page()

    elif menu == "Dashboard":
        st.title(f"Welcome back, {st.session_state.user_name}!")
        
        if os.path.exists('users.csv'):
            df_users = pd.read_csv('users.csv')
            user_row = df_users[df_users['Name'] == st.session_state.user_name]
            
            if not user_row.empty:
                info = user_row.iloc[0]
                streak_val = int(info['Streak']) if 'Streak' in df_users.columns and pd.notna(info['Streak']) else 0
                badge_name = "🔥 Elite Bookworm" if streak_val >= 7 else ("⭐ Consistent Reader" if streak_val >= 3 else "🌱 Beginner Reader")

                col1, col2 = st.columns(2)
                col1.metric("🔥 Reading Streak", f"{streak_val} Days")
                col2.metric("🏆 Current Badge", badge_name)
                
                st.write("---")
                st.write("### 👤 Your Profile Details")
                st.write(f"**Name:** {info['Name']}")
                st.write(f"**Age:** {info['Age']}")
                st.write(f"**Gender:** {info['Gender']}")
                st.write(f"**Phone:** {info['Phone']}")
                st.write(f"**Address:** {info['Address']}")
                st.write(f"**Date of Birth:** {info['DOB']}")
            else: 
                st.error("Profile not found.")
        else:
            st.warning("User database not found.")

    elif menu == "Edit Profile":
        profile.run_edit_profile()

    elif menu == "Start Reading":
        streaks.update_user_streak(st.session_state.user_name)
        app.run_app()

    elif menu == "Vocabulary Vault":
        vocabulary.run_vocab_vault()

    elif menu == "Reading Goals":
        goals.run_goals_section()

    elif menu == "Reports":
        reports_export.run_advanced_reports()

    elif menu == "Brain Games":
        games_hub.run_games()

    elif menu == "Educator Portal":
        educator_portal.run_educator_portal()

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()