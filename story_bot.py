import streamlit as st
import pandas as pd
import os

def run_story_bot():
    st.title("🤖 Chatbot Reading Guide")
    st.write("Chat with your AI reading coach! Ask it to recommend a story, and it will load it for you instantly.")
    
    # Initialize chat history for the bot
    if "bot_messages" not in st.session_state:
        st.session_state.bot_messages = [
            {"role": "assistant", "content": "Hi there! 👋 I can help you pick a story. Do you want something **Beginner**, **Intermediate**, or **Advanced**, or a specific topic like space or animals?"}
        ]
        
    # Display chat messages
    for msg in st.session_state.bot_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            
    # User input
    if user_input := st.chat_input("Type your request here (e.g., 'Give me an easy space story')..."):
        st.session_state.bot_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
            
        # Generate smart bot response & pick a story from library.csv
        bot_response, selected_content = get_bot_story_response(user_input)
        
        st.session_state.bot_messages.append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.write(bot_response)
            if selected_content:
                st.success("🎉 Story loaded successfully! Go to the 'Start Reading' section to read it and get your score.")

def get_bot_story_response(user_text):
    text_lower = user_text.lower()
    
    if not os.path.exists('library.csv'):
        return "Sorry, I can't find the library database right now!", None
        
    df = pd.read_csv('library.csv')
    
    # Match based on user input keywords
    chosen_row = None
    if "beginner" in text_lower or "easy" in text_lower:
        chosen_row = df[df['Difficulty'] == 'Beginner'].iloc[0]
    elif "intermediate" in text_lower:
        chosen_row = df[df['Difficulty'] == 'Intermediate'].iloc[0]
    elif "advanced" in text_lower or "hard" in text_lower:
        chosen_row = df[df['Difficulty'] == 'Advanced'].iloc[0]
    elif "space" in text_lower:
        chosen_row = df[df['Title'].str.contains("Space", case=False, na=False)].iloc[0]
    elif "animal" in text_lower or "fox" in text_lower:
        chosen_row = df[df['Title'].str.contains("Fox|Dolphin", case=False, na=False)].iloc[0]
    else:
        # Default to the first story if no keyword matches
        chosen_row = df.iloc[0]
        
    title = chosen_row['Title']
    level = chosen_row['Difficulty']
    content = chosen_row['Content']
    
    # Save to session state so 'Start Reading' can use it
    st.session_state.selected_story = content
    
    response = f"I picked **'{title}'** ({level}) for you! Here is a sneak peek:\n\n> *\"{content}\"* \n\nI have loaded this into your reading engine. Whenever you're ready, head over to **'Start Reading'** to read it aloud, track your camera emotions, and get your final accuracy score!"
    
    return response, content