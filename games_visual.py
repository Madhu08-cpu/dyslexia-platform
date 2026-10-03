import streamlit as st
import random

def run_visual_games():
    st.subheader("🖼️ Visual & Picture Training Suite")
    sub_choice = st.selectbox("Choose a Visual Challenge", ["Object & Silhouette Match", "Emotion & Scene Picture Guess"])
    st.divider()

    if sub_choice == "Object & Silhouette Match":
        st.write("Look at the target clue and select the matching picture category to build visual perception skills!")

        visual_challenges = [
            {"clue": "🦁 Wild Animal / King of Jungle", "options": ["🦁 Lion", "🚗 Car", "🍕 Pizza", "⌚ Watch"], "correct": "🦁 Lion"},
            {"clue": "🚀 Outer Space Vehicle", "options": ["🍎 Apple", "🚀 Rocket", "🌲 Tree", "⚽ Ball"], "correct": "🚀 Rocket"},
            {"clue": "🎸 Musical Instrument with Strings", "options": ["🎸 Guitar", "💻 Laptop", "👟 Shoe", "📚 Book"], "correct": "🎸 Guitar"},
            {"clue": "🌻 Bright Yellow Garden Flower", "options": ["🐟 Fish", "🌻 Sunflower", "☕ Cup", "🔑 Key"], "correct": "🌻 Sunflower"},
        ]

        if 'visual_score' not in st.session_state: st.session_state.visual_score = 0
        if 'current_visual' not in st.session_state: st.session_state.current_visual = random.choice(visual_challenges)

        challenge = st.session_state.current_visual

        st.write(f"**Score:** {st.session_state.visual_score}")
        st.markdown(f"### Clue: {challenge['clue']}")
        st.write("Choose the correct picture match:")

        cols = st.columns(len(challenge['options']))
        for i, opt in enumerate(challenge['options']):
            with cols[i]:
                if st.button(opt, key=f"vis_opt_{i}"):
                    if opt == challenge['correct']:
                        st.session_state.visual_score += 1
                        st.success("Correct picture match! 🎉")
                    else:
                        st.error("Incorrect! Try the next clue.")
                    
                    st.session_state.current_visual = random.choice(visual_challenges)
                    st.rerun()

        if st.button("Reset Score", key="rst_visual"):
            st.session_state.visual_score = 0
            st.rerun()

    elif sub_choice == "Emotion & Scene Picture Guess":
        st.write("Read the facial emotion or scene description and identify the matching emotional state or setting.")

        scenarios = [
            {"desc": "A student just scored 100% on a hard reading test and is smiling widely.", "options": ["😀 Happy / Excited", "😢 Sad", "😡 Angry", "😴 Tired"], "correct": "😀 Happy / Excited"},
            {"desc": "Someone is sitting quietly with wide eyes, looking at a sudden loud noise.", "options": ["😎 Cool", "😱 Surprised / Shocked", "🥳 Partying", "🤔 Confused"], "correct": "😱 Surprised / Shocked"},
            {"desc": "A child is frowning with closed eyes because they dropped their ice cream.", "options": ["😄 Joyful", "😢 Disappointed / Sad", "🤩 Amazed", "😌 Peaceful"], "correct": "😢 Disappointed / Sad"},
            {"desc": "A person has crossed arms, furrowed brows, and a tight mouth after a frustrating event.", "options": ["😡 Frustrated / Angry", "😴 Sleepy", "🥳 Excited", "🥰 Loving"], "correct": "😡 Frustrated / Angry"},
        ]

        if 'emotion_game_score' not in st.session_state: st.session_state.emotion_game_score = 0
        if 'current_scene' not in st.session_state: st.session_state.current_scene = random.choice(scenarios)

        scene = st.session_state.current_scene

        st.write(f"**Score:** {st.session_state.emotion_game_score}")
        st.info(f"**Scenario / Expression Clue:**\n\n_{scene['desc']}_")
        st.write("What emotion or reaction best describes this picture/scene?")

        cols = st.columns(2)
        for i, opt in enumerate(scene['options']):
            with cols[i % 2]:
                if st.button(opt, key=f"emo_opt_{i}", use_container_width=True):
                    if opt == scene['correct']:
                        st.session_state.emotion_game_score += 1
                        st.success("Spot on! Great emotional recognition! 🎉")
                    else:
                        st.error("Not quite! Look closer at the clues.")
                    
                    st.session_state.current_scene = random.choice(scenarios)
                    st.rerun()

        if st.button("Reset Score", key="rst_emotion_game"):
            st.session_state.emotion_game_score = 0
            st.rerun()