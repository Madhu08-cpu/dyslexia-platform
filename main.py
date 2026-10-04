import datetime
import hashlib
import os
import re
import pandas as pd
import streamlit as st

# Import modular files
import app
import educator_portal
import games_hub
import goals
import landing_page
import profile
import reports_export
import start_reading
import streaks
import ui
import vocabulary

# --- INITIALIZE SESSION STATE ---
if "status" not in st.session_state:
  st.session_state.status = "IDLE"
if "start_time" not in st.session_state:
  st.session_state.start_time = None
if "last_emotion" not in st.session_state:
  st.session_state.last_emotion = "NEUTRAL"
if "session_data" not in st.session_state:
  st.session_state.session_data = []
if "logged_in" not in st.session_state:
  st.session_state.logged_in = False
if "user_role" not in st.session_state:
  st.session_state.user_role = "Student / Parent"

st.set_page_config(
    page_title="Reading Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --- LOAD EXTERNAL CSS ---
def load_css(file_name="style.css"):
  if os.path.exists(file_name):
    with open(file_name) as f:
      st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("style.css")


def validate_password(password):
  if len(password) < 8:
    return "Password must be at least 8 characters long."
  if not re.search(r"[A-Z]", password):
    return "Password must contain at least one uppercase letter."
  if not re.search(r"[a-z]", password):
    return "Password must contain at least one lowercase letter."
  if not re.search(r"\d", password):
    return "Password must contain at least one number."
  if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
    return "Password must contain at least one special character."
  return None


# --- LOGIN & REGISTER SCREEN ---
if not st.session_state.logged_in:
  st.sidebar.markdown(
      """
        <div style="padding: 10px 0 15px 0;">
            <h2 style="margin:0; font-size: 1.3rem; color: #FFFFFF;">🧠 NeuroRead Portal</h2>
            <p style="color: #94A3B8; font-size: 0.8rem; margin-top: 2px;">AI Reading & Learning Platform</p>
        </div>
    """,
      unsafe_allow_html=True,
  )

  choice = st.sidebar.radio("Navigation", ["Login", "Register"])

  col_l, col_m, col_r = st.columns([1, 2, 1])

  with col_m:
    if choice == "Login":
      ui.render_header("Welcome Back 👋", "Log in to access your platform")

      ui.render_card_start("Sign In")
      selected_role = st.selectbox(
          "I am a...", ["Student / Parent", "Teacher / Educator"]
      )
      name = st.text_input("Username")
      password = st.text_input("Password", type="password")

      st.markdown("<br>", unsafe_allow_html=True)
      if st.button("Login", use_container_width=True):
        if os.path.exists("users.csv"):
          df = pd.read_csv("users.csv")

          # Ensure 'Role' column exists for legacy user database compatibility
          if "Role" not in df.columns:
            df["Role"] = "Student / Parent"

          hashed = hashlib.sha256(password.encode()).hexdigest()
          user = df[
              (df["Name"] == name)
              & (df["Password"] == hashed)
              & (df["Role"] == selected_role)
          ]

          if not user.empty:
            st.session_state.logged_in = True
            st.session_state.user_name = name
            st.session_state.user_role = selected_role
            st.rerun()
          else:
            st.error(
                "Invalid credentials or incorrect role selected! Check your"
                " username, password, and role."
            )
        else:
          st.warning("No users registered yet.")
      ui.render_card_end()

    else:
      ui.render_header(
          "Create Account ✨", "Register to access customized tools"
      )

      ui.render_card_start("User Registration")
      with st.form("reg"):
        reg_role = st.selectbox(
            "Account Type", ["Student / Parent", "Teacher / Educator"]
        )
        name = st.text_input("Full Name")
        pw = st.text_input(
            "Password",
            type="password",
            help=(
                "Must be 8+ characters with uppercase, lowercase, number, and"
                " special character."
            ),
        )
        age = st.number_input("Age", min_value=1, max_value=100)
        phone = st.text_input("Phone Number")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        min_date = datetime.date(1900, 1, 1)
        max_date = datetime.date.today()
        dob = st.date_input(
            "Date of Birth",
            min_value=min_date,
            max_value=max_date,
            value=datetime.date(2000, 1, 1),
        )
        address = st.text_area("Address")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.form_submit_button("Register"):
          if name and pw:
            password_error = validate_password(pw)
            if password_error:
              st.error(password_error)
            else:
              hashed = hashlib.sha256(pw.encode()).hexdigest()
              file_exists = os.path.exists("users.csv")

              new_user_data = {
                  "Name": [name],
                  "Password": [hashed],
                  "Role": [reg_role],
                  "Age": [age],
                  "Phone": [phone],
                  "Gender": [gender],
                  "DOB": [str(dob)],
                  "Address": [address],
                  "Streak": [0],
                  "Last_Read_Date": [""],
              }

              if file_exists:
                df_existing = pd.read_csv("users.csv")
                if (
                    not df_existing.empty
                    and "Name" in df_existing.columns
                    and name in df_existing["Name"].values
                ):
                  st.error(
                      "User with this name already exists. Please choose"
                      " another or login."
                  )
                else:
                  new_user = pd.DataFrame(new_user_data)
                  new_user.to_csv(
                      "users.csv", mode="a", header=False, index=False
                  )
                  st.success(
                      f"Registered successfully as {reg_role}! Please login."
                  )
              else:
                new_user = pd.DataFrame(new_user_data)
                new_user.to_csv("users.csv", mode="a", header=True, index=False)
                st.success(
                    f"Registered successfully as {reg_role}! Please login."
                )
          else:
            st.error("Name and Password are required.")
      ui.render_card_end()

# --- MAIN DASHBOARD & ROUTING ---
else:
  # Header badge showing active role
  portal_title = (
      "👩‍🏫 Teacher Portal"
      if st.session_state.user_role == "Teacher / Educator"
      else "🎓 Student Portal"
  )

  st.sidebar.markdown(
      f"""
        <div style="padding: 0px 0px 15px 0px;">
            <h2 style="margin:0; font-size: 1.3rem; color: #FFFFFF;">{portal_title}</h2>
            <p style="color: #94A3B8; font-size: 0.8rem; margin-top: 2px;">NeuroRead AI Engine</p>
        </div>
    """,
      unsafe_allow_html=True,
  )

  # Dynamic menu options based on User Role
  if st.session_state.user_role == "Teacher / Educator":
    menu_options = [
        "Home / Welcome",
        "Educator Portal",
        "Reports & Student Analytics",
        "Edit Profile",
    ]
  else:
    menu_options = [
        "Home / Welcome",
        "Dashboard",
        "Edit Profile",
        "Start Reading",
        "Vocabulary Vault",
        "Reading Goals",
        "Reports",
        "Brain Games",
    ]

  menu = st.sidebar.radio("Platform Menu", menu_options)

  if menu == "Home / Welcome":
    landing_page.run_landing_page()

  elif menu == "Dashboard":
    ui.render_header(
        f"Welcome back, {st.session_state.user_name}!",
        "Track your reading streaks, badges, and account information.",
        "📊",
    )

    if os.path.exists("users.csv"):
      df_users = pd.read_csv("users.csv")
      user_row = df_users[df_users["Name"] == st.session_state.user_name]

      if not user_row.empty:
        info = user_row.iloc[0]
        streak_val = (
            int(info["Streak"])
            if "Streak" in df_users.columns and pd.notna(info["Streak"])
            else 0
        )
        badge_name = (
            "🔥 Elite Bookworm"
            if streak_val >= 7
            else (
                "⭐ Consistent Reader"
                if streak_val >= 3
                else "🌱 Beginner Reader"
            )
        )

        col1, col2 = st.columns(2)
        with col1:
          ui.render_stat_card(
              "Reading Streak", f"{streak_val} Days", badge_text="Active Streak"
          )
        with col2:
          ui.render_stat_card("Current Badge", badge_name, badge_text="Unlocked")

        st.markdown("<br>", unsafe_allow_html=True)

        ui.render_card_start("👤 Your Profile Details")
        st.markdown(
            f"""
                    <div class="data-row"><span class="row-label">Name</span><span class="row-value">{info['Name']}</span></div>
                    <div class="data-row"><span class="row-label">Role</span><span class="row-value">{st.session_state.user_role}</span></div>
                    <div class="data-row"><span class="row-label">Age</span><span class="row-value">{info['Age']}</span></div>
                    <div class="data-row"><span class="row-label">Gender</span><span class="row-value">{info['Gender']}</span></div>
                    <div class="data-row"><span class="row-label">Phone</span><span class="row-value">{info['Phone']}</span></div>
                    <div class="data-row"><span class="row-label">Address</span><span class="row-value">{info['Address']}</span></div>
                    <div class="data-row"><span class="row-label">Date of Birth</span><span class="row-value">{info['DOB']}</span></div>
                """,
            unsafe_allow_html=True,
        )
        ui.render_card_end()
      else:
        st.error("Profile not found.")
    else:
      st.warning("User database not found.")

  elif menu == "Edit Profile":
    profile.run_edit_profile()

  elif menu == "Start Reading":
    streaks.update_user_streak(st.session_state.user_name)
    start_reading.run_start_reading()  # UPDATED HERE: Invokes start_reading instead of app.run_app()

  elif menu == "Vocabulary Vault":
    vocabulary.run_vocab_vault()

  elif menu == "Reading Goals":
    goals.run_goals_section()

  elif menu in ["Reports", "Reports & Student Analytics"]:
    reports_export.run_advanced_reports()

  elif menu == "Brain Games":
    games_hub.run_games()

  elif menu == "Educator Portal":
    educator_portal.run_educator_portal()

  st.sidebar.markdown("<br>", unsafe_allow_html=True)
  if st.sidebar.button("Logout", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.user_role = "Student / Parent"
    st.rerun()