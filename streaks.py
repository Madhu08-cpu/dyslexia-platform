import streamlit as st
import pandas as pd
import os
import datetime

def update_user_streak(username):
    """
    Checks and updates the user's reading streak based on the current date.
    """
    if not os.path.exists('users.csv'):
        return 0
    
    df = pd.read_csv('users.csv')
    if username not in df['Name'].values:
        return 0
        
    idx = df.index[df['Name'] == username][0]
    
    if 'Streak' not in df.columns:
        df['Streak'] = 0
    if 'Last_Read_Date' not in df.columns:
        df['Last_Read_Date'] = ""
        
    current_streak = int(df.loc[idx, 'Streak']) if pd.notna(df.loc[idx, 'Streak']) else 0
    last_date_str = str(df.loc[idx, 'Last_Read_Date']) if pd.notna(df.loc[idx, 'Last_Read_Date']) else ""
    today = datetime.date.today()
    
    if last_date_str == "":
        current_streak = 1
        df.loc[idx, 'Streak'] = current_streak
        df.loc[idx, 'Last_Read_Date'] = str(today)
        df.to_csv('users.csv', index=False)
    else:
        try:
            last_date = datetime.datetime.strptime(last_date_str, "%Y-%m-%d").date()
            diff = (today - last_date).days
            if diff == 1:
                current_streak += 1
                df.loc[idx, 'Streak'] = current_streak
                df.loc[idx, 'Last_Read_Date'] = str(today)
                df.to_csv('users.csv', index=False)
            elif diff > 1:
                current_streak = 1
                df.loc[idx, 'Streak'] = current_streak
                df.loc[idx, 'Last_Read_Date'] = str(today)
                df.to_csv('users.csv', index=False)
        except ValueError:
            pass
            
    return current_streak