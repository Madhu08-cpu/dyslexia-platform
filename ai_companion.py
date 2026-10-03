import streamlit as st

def run_ai_companion():
    st.title("🤖 AI Reading Companion")
    st.write("Have questions about what you read? Ask your AI companion for summaries, explanations, or definitions!")
    
    # Retrieve the active story or fallback
    current_story = st.session_state.get('selected_story', "No active story selected yet. Choose one from the Library!")
    
    with st.expander("📖 View Current Story Context"):
        st.write(current_story)
        
    # Initialize chat history in session state if not present
    if "ai_messages" not in st.session_state:
        st.session_state.ai_messages = [
            {"role": "assistant", "content": "Hello! I'm your reading buddy. Ask me anything about your current story or vocabulary!"}
        ]
        
    # Display previous chat messages
    for message in st.session_state.ai_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
    # User input chat box
    if user_prompt := st.chat_input("Ask a question about the story..."):
        # Append user message
        st.session_state.ai_messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.write(user_prompt)
            
        # Generate smart simulated or context-aware response
        response = generate_ai_response(user_prompt, current_story)
        
        # Append assistant response
        st.session_state.ai_messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

def generate_ai_response(prompt, story):
    prompt_lower = prompt.lower()
    
    if "summary" in prompt_lower or "summarize" in prompt_lower:
        return f"Here is a quick summary of your current text: This passage focuses on exploring key concepts and actions described as: '{story[:100]}...'"
    elif "mean" in prompt_lower or "definition" in prompt_lower:
        return f"In the context of your reading passage ('{story[:60]}...'), words are used to convey specific actions or descriptions. If there's a specific difficult word you're wondering about, let me know!"
    elif "hello" in prompt_lower or "hi" in prompt_lower:
        return "Hello there! Ready to explore more of your reading session?"
    else:
        return f"That's a great question about the text! Based on what you're reading ('{story[:50]}...'), keeping context in mind helps build stronger reading comprehension skills. Try breaking down the sentences word by word!"