import streamlit as st
import pandas as pd
import os
import datetime

SCHOOLS_FILE = "schools.csv"
ASSIGNMENTS_FILE = "assignments.csv"
USERS_FILE = "users.csv"

def run_educator_portal():
    st.title("👩‍🏫 Educator & Parent Portal")
    st.write("Manage student progress, view detailed analytics, and assign custom reading tasks with deadlines.")

    current_user = st.session_state.get('user_name', 'Guest')
    user_role = st.session_state.get('user_role', 'Teacher')

    # --- 1. HIERARCHICAL LOCATION & SCHOOL DIRECTORY ---
    st.subheader("🏫 Institution & Student Directory")

    # Load schools data or initialize default structure
    if os.path.exists(SCHOOLS_FILE):
        df_schools = pd.read_csv(SCHOOLS_FILE)
    else:
        df_schools = pd.DataFrame(columns=["Country", "State", "District", "Taluk", "SchoolName"])

    # Cascading dropdowns: Country -> State -> District -> Taluk -> School
    countries = df_schools["Country"].unique().tolist() if not df_schools.empty else ["India", "United States"]
    selected_country = st.selectbox("Select Country", countries)

    filtered_states = df_schools[df_schools["Country"] == selected_country]["State"].unique().tolist() if not df_schools.empty else ["Karnataka", "Maharashtra"]
    selected_state = st.selectbox("Select State / Region", filtered_states)

    filtered_districts = df_schools[(df_schools["Country"] == selected_country) & (df_schools["State"] == selected_state)]["District"].unique().tolist() if not df_schools.empty else ["Bengaluru Urban", "Mysuru"]
    selected_district = st.selectbox("Select District / City", filtered_districts)

    filtered_taluks = df_schools[(df_schools["Country"] == selected_country) & (df_schools["State"] == selected_state) & (df_schools["District"] == selected_district)]["Taluk"].unique().tolist() if not df_schools.empty else ["North Taluk", "South Taluk"]
    selected_taluk = st.selectbox("Select Taluk", filtered_taluks)

    filtered_schools = df_schools[(df_schools["Country"] == selected_country) & (df_schools["State"] == selected_state) & (df_schools["District"] == selected_district) & (df_schools["Taluk"] == selected_taluk)]["SchoolName"].unique().tolist() if not df_schools.empty else ["Greenwood High School", "Sunrise Public School"]
    selected_school = st.selectbox("Select School Name", filtered_schools)

    st.divider()

    # --- 2. SELECT PARTICULAR STUDENT FOR PROGRESS ---
    st.subheader(f"📊 Student Management for: {selected_school}")

    if os.path.exists(USERS_FILE):
        df_users = pd.read_csv(USERS_FILE)
        if 'SchoolName' in df_users.columns and 'Role' in df_users.columns:
            class_students = df_users[(df_users['SchoolName'] == selected_school) & (df_users['Role'] == 'Student')]['Username'].tolist()
        else:
            class_students = df_users['Username'].tolist() if 'Username' in df_users.columns else []
    else:
        class_students = ["student_alex", "student_maya"]

    if not class_students:
        st.info("No students registered under this school yet.")
        return

    selected_student = st.selectbox("Select a Particular Student", class_students)

    if selected_student:
        st.markdown(f"### 📈 Performance Overview: **{selected_student}**")

        perf_file = 'student_performance.csv'
        if os.path.exists(perf_file):
            df_perf = pd.read_csv(perf_file)
            if 'Username' in df_perf.columns:
                student_perf = df_perf[df_perf['Username'].astype(str) == str(selected_student)]
                st.metric("Total Completed Reading Sessions", len(student_perf))
                if not student_perf.empty:
                    st.dataframe(student_perf, use_container_width=True)
                else:
                    st.info(f"No reading records found for {selected_student} yet.")

        st.divider()

        # --- 3. ASSIGN CUSTOM HOMEWORK WITH DEADLINE ---
        st.subheader(f"📝 Assign Custom Homework to {selected_student}")

        with st.form("assignment_form"):
            task_title = st.text_input("Assignment Title (e.g., Chapter 1 Practice)")
            task_content = st.text_area("Custom Reading Passage / Sentences")
            deadline_date = st.date_input("Complete Within (Due Date)", datetime.date.today() + datetime.timedelta(days=3))
            
            assign_submitted = st.form_submit_button("Send Assignment 🚀")

            if assign_submitted:
                if task_title and task_content:
                    new_assignment = pd.DataFrame({
                        'Student': [selected_student],
                        'AssignedBy': [current_user],
                        'Title': [task_title],
                        'Content': [task_content],
                        'DueDate': [str(deadline_date)],
                        'Status': ['Pending']
                    })
                    
                    assign_file_exists = os.path.exists(ASSIGNMENTS_FILE)
                    new_assignment.to_csv(ASSIGNMENTS_FILE, mode='a', header=not assign_file_exists, index=False)
                    st.success(f"Successfully assigned '{task_title}' to **{selected_student}**, due by **{deadline_date}**!")
                else:
                    st.error("Please fill in both the title and the passage content.")