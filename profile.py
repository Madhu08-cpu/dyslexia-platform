import streamlit as st
import pandas as pd
import os
import datetime

def run_edit_profile():
    st.title("✏️ Edit Your Profile")
    
    if os.path.exists('users.csv'):
        df_users = pd.read_csv('users.csv')
        user_idx = df_users.index[df_users['Name'] == st.session_state.user_name].tolist()
        
        if user_idx:
            idx = user_idx[0]
            current_info = df_users.loc[idx]
            
            gender_options = ["Male", "Female", "Other"]
            default_gender_idx = gender_options.index(current_info['Gender']) if current_info['Gender'] in gender_options else 0
            
            try:
                default_dob = datetime.datetime.strptime(str(current_info['DOB']), "%Y-%m-%d").date()
            except ValueError:
                default_dob = datetime.date(2000, 1, 1)

            with st.form("edit_profile_form"):
                new_age = st.number_input("Age", min_value=1, max_value=100, value=int(current_info['Age']))
                new_phone = st.text_input("Phone Number", value=str(current_info['Phone']))
                new_gender = st.selectbox("Gender", gender_options, index=default_gender_idx)
                
                min_date = datetime.date(1900, 1, 1)
                max_date = datetime.date.today()
                new_dob = st.date_input("Date of Birth", min_value=min_date, max_value=max_date, value=default_dob)
                
                new_address = st.text_area("Address", value=str(current_info['Address']))
                
                update_submitted = st.form_submit_button("Update Profile")
                
                if update_submitted:
                    df_users.loc[idx, 'Age'] = new_age
                    df_users.loc[idx, 'Phone'] = new_phone
                    df_users.loc[idx, 'Gender'] = new_gender
                    df_users.loc[idx, 'DOB'] = str(new_dob)
                    df_users.loc[idx, 'Address'] = new_address
                    
                    df_users.to_csv('users.csv', index=False)
                    st.success("Profile updated successfully! Go back to Dashboard to see changes.")
        else:
            st.error("User record not found.")
    else:
        st.warning("User database not found.")