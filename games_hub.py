import streamlit as st
import random
import time
import os
import csv
import datetime
import games_visual


def log_game_completion(game_name):
    """Helper function to log completed games into games_history.csv."""
    current_user = st.session_state.get("user_name", "Guest")
    file_name = "games_history.csv"

    log_key = f"logged_{game_name}"

    if not st.session_state.get(log_key, False):
        file_exists = os.path.exists(file_name)

        with open(file_name, "a", newline="") as f:
            writer = csv.writer(f)

            if not file_exists:
                writer.writerow(
                    ["Time", "Username", "Game_Name", "Status"]
                )

            writer.writerow([
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                current_user,
                game_name,
                "Completed"
            ])

        st.session_state[log_key] = True


def run_games():

    st.title("🎮 Brain Games & Skill Improvement")

    st.write(
        "Train with timed limits, track your speed, "
        "and watch your accuracy improve across all 6 games!"
    )

    game_choice = st.sidebar.selectbox(
        "Choose a Game",
        [
            "1. Stroop Color Match",
            "2. Catch the Target (Reaction)",
            "3. Letter Reversal Training",
            "4. Memory Sequence Flash",
            "5. Speed Word Scramble",
            "6. Visual & Picture Training"
        ]
    )

    st.divider()

    # ============================================================
    # GAME 1: STROOP COLOR MATCH
    # ============================================================

    if game_choice == "1. Stroop Color Match":

        st.subheader("🎨 Stroop Effect Challenge")
        st.write(
            "**Rule:** Select the **INK COLOR** of the word shown below as fast as you can!"
        )

        max_rounds = 10

        if "stroop_attempts" not in st.session_state:
            st.session_state.stroop_attempts = 0

        if "stroop_correct" not in st.session_state:
            st.session_state.stroop_correct = 0

        if "stroop_total_time" not in st.session_state:
            st.session_state.stroop_total_time = 0.0

        if "stroop_round_start" not in st.session_state:
            st.session_state.stroop_round_start = time.time()

        if "target_word" not in st.session_state:
            st.session_state.target_word = random.choice(
                ["Red", "Blue", "Green", "Orange", "Purple"]
            )

        if "target_color" not in st.session_state:
            st.session_state.target_color = random.choice(
                ["Red", "Blue", "Green", "Orange", "Purple"]
            )

        if st.session_state.stroop_attempts >= max_rounds:

            log_game_completion("Stroop Color Match")

            accuracy = (
                st.session_state.stroop_correct / max_rounds
            ) * 100

            avg_time = round(
                st.session_state.stroop_total_time / max_rounds,
                2
            )

            st.success("🎉 Session Complete!")

            col_a, col_b = st.columns(2)

            col_a.metric(
                "Final Accuracy",
                f"{accuracy:.1f}%"
            )

            col_b.metric(
                "Avg Time per Answer",
                f"{avg_time}s"
            )

            if st.button(
                "Play Again",
                key="restart_stroop_limit"
            ):
                st.session_state.stroop_attempts = 0
                st.session_state.stroop_correct = 0
                st.session_state.stroop_total_time = 0.0
                st.session_state.stroop_round_start = time.time()
                st.session_state.logged_Stroop_Color_Match = False
                st.rerun()

        else:

            colors = [
                "Red",
                "Blue",
                "Green",
                "Orange",
                "Purple"
            ]

            color_codes = {
                "Red": "red",
                "Blue": "blue",
                "Green": "green",
                "Orange": "orange",
                "Purple": "purple"
            }

            word_display = st.session_state.target_word
            ink_color = color_codes[
                st.session_state.target_color
            ]

            st.markdown(
                f"### Round {st.session_state.stroop_attempts + 1} of {max_rounds}"
            )

            st.markdown(
                f"""
                <h1 style="
                    color:{ink_color};
                    text-align:center;
                    font-size:60px;
                ">
                    {word_display}
                </h1>
                """,
                unsafe_allow_html=True
            )

            st.write("What is the **INK COLOR**?")

            cols = st.columns(len(colors))

            for i, col in enumerate(cols):

                with col:

                    if st.button(
                        colors[i],
                        key=f"stroop_{colors[i]}"
                    ):

                        elapsed = (
                            time.time()
                            - st.session_state.stroop_round_start
                        )

                        st.session_state.stroop_total_time += elapsed
                        st.session_state.stroop_attempts += 1

                        if (
                            colors[i]
                            == st.session_state.target_color
                        ):
                            st.session_state.stroop_correct += 1

                        st.session_state.target_word = random.choice(
                            colors
                        )

                        st.session_state.target_color = random.choice(
                            colors
                        )

                        st.session_state.stroop_round_start = time.time()

                        st.rerun()

        st.write("")

        if st.button(
            "Reset Session",
            key="rst_stroop"
        ):
            st.session_state.stroop_attempts = 0
            st.session_state.stroop_correct = 0
            st.session_state.stroop_total_time = 0.0
            st.session_state.stroop_round_start = time.time()
            st.session_state.logged_Stroop_Color_Match = False
            st.rerun()


    # ============================================================
    # GAME 2: CATCH THE TARGET
    # ============================================================

    elif game_choice == "2. Catch the Target (Reaction)":

        st.subheader("🎯 Focus & Reaction Challenge")
        st.write("Catch the target star 10 times as fast as you can!")

        max_rounds = 10

        if "reaction_attempts" not in st.session_state:
            st.session_state.reaction_attempts = 0

        if "reaction_score" not in st.session_state:
            st.session_state.reaction_score = 0

        if "react_total_time" not in st.session_state:
            st.session_state.react_total_time = 0.0

        if "react_round_start" not in st.session_state:
            st.session_state.react_round_start = time.time()

        if "target_pos" not in st.session_state:
            st.session_state.target_pos = random.randint(0, 3)

        if st.session_state.reaction_attempts >= max_rounds:

            log_game_completion("Catch the Target")

            accuracy = (
                st.session_state.reaction_score / max_rounds
            ) * 100

            avg_time = round(
                st.session_state.react_total_time / max_rounds,
                2
            )

            st.success("🎉 Reaction Challenge Complete!")

            col_a, col_b = st.columns(2)

            col_a.metric(
                "Success Rate",
                f"{accuracy:.1f}%"
            )

            col_b.metric(
                "Avg Reaction Time",
                f"{avg_time}s"
            )

            if st.button(
                "Play Again",
                key="restart_react_limit"
            ):
                st.session_state.reaction_attempts = 0
                st.session_state.reaction_score = 0
                st.session_state.react_total_time = 0.0
                st.session_state.react_round_start = time.time()
                st.session_state.logged_Catch_the_Target = False
                st.rerun()

        else:

            st.markdown(
                f"### Progress: "
                f"{st.session_state.reaction_attempts} / {max_rounds} tries"
            )

            cols = st.columns(4)

            for i in range(4):

                with cols[i]:

                    label = (
                        "⭐ CATCH ME!"
                        if i == st.session_state.target_pos
                        else "· · ·"
                    )

                    if st.button(
                        label,
                        key=f"target_{i}"
                    ):

                        elapsed = (
                            time.time()
                            - st.session_state.react_round_start
                        )

                        st.session_state.react_total_time += elapsed
                        st.session_state.reaction_attempts += 1

                        if i == st.session_state.target_pos:
                            st.session_state.reaction_score += 1

                        st.session_state.target_pos = random.randint(0, 3)
                        st.session_state.react_round_start = time.time()

                        st.rerun()

        st.write("")

        if st.button(
            "Reset Session",
            key="rst_react"
        ):
            st.session_state.reaction_attempts = 0
            st.session_state.reaction_score = 0
            st.session_state.react_total_time = 0.0
            st.session_state.react_round_start = time.time()
            st.session_state.logged_Catch_the_Target = False
            st.rerun()


    # ============================================================
    # GAME 3: LETTER REVERSAL TRAINING
    # ============================================================

    elif game_choice == "3. Letter Reversal Training":

        st.subheader("🔤 Letter Reversal & Discrimination")
        st.write("Complete 10 rapid discrimination trials.")

        max_rounds = 10

        pairs = [
            ("Find the letter: **b**", ["d", "b", "p", "d"], "b"),
            ("Find the letter: **d**", ["b", "p", "d", "q"], "d"),
            ("Find the letter: **p**", ["q", "p", "b", "d"], "p"),
            ("Find the letter: **q**", ["d", "p", "q", "b"], "q")
        ]

        if "reversal_attempts" not in st.session_state:
            st.session_state.reversal_attempts = 0

        if "reversal_score" not in st.session_state:
            st.session_state.reversal_score = 0

        if "rev_total_time" not in st.session_state:
            st.session_state.rev_total_time = 0.0

        if "rev_round_start" not in st.session_state:
            st.session_state.rev_round_start = time.time()

        if "current_round" not in st.session_state:
            st.session_state.current_round = random.choice(pairs)

        if st.session_state.reversal_attempts >= max_rounds:

            log_game_completion("Letter Reversal Training")

            accuracy = (
                st.session_state.reversal_score / max_rounds
            ) * 100

            avg_time = round(
                st.session_state.rev_total_time / max_rounds,
                2
            )

            st.success("🎉 Reversal Training Complete!")

            col_a, col_b = st.columns(2)

            col_a.metric(
                "Discrimination Accuracy",
                f"{accuracy:.1f}%"
            )

            col_b.metric(
                "Avg Time per Trial",
                f"{avg_time}s"
            )

            if st.button(
                "Play Again",
                key="restart_rev_limit"
            ):
                st.session_state.reversal_attempts = 0
                st.session_state.reversal_score = 0
                st.session_state.rev_total_time = 0.0
                st.session_state.rev_round_start = time.time()
                st.session_state.logged_Letter_Reversal_Training = False
                st.rerun()

        else:

            prompt, options, correct_answer = (
                st.session_state.current_round
            )

            st.markdown(
                f"### Trial "
                f"{st.session_state.reversal_attempts + 1} "
                f"of {max_rounds}"
            )

            st.write(f"### {prompt}")

            cols = st.columns(len(options))

            for i, col in enumerate(cols):

                with col:

                    if st.button(
                        options[i].upper(),
                        key=f"rev_{i}_{options[i]}"
                    ):

                        elapsed = (
                            time.time()
                            - st.session_state.rev_round_start
                        )

                        st.session_state.rev_total_time += elapsed
                        st.session_state.reversal_attempts += 1

                        if options[i] == correct_answer:
                            st.session_state.reversal_score += 1

                        st.session_state.current_round = random.choice(pairs)
                        st.session_state.rev_round_start = time.time()

                        st.rerun()

        st.write("")

        if st.button(
            "Reset Session",
            key="rst_rev"
        ):
            st.session_state.reversal_attempts = 0
            st.session_state.reversal_score = 0
            st.session_state.rev_total_time = 0.0
            st.session_state.rev_round_start = time.time()
            st.session_state.logged_Letter_Reversal_Training = False
            st.rerun()


    # ============================================================
    # GAME 4: MEMORY SEQUENCE FLASH
    # ============================================================

    elif game_choice == "4. Memory Sequence Flash":

        st.subheader("💡 Memory Sequence Flash")
        st.write("Complete 5 memory patterns successfully!")

        max_rounds = 5

        if "mem_attempts" not in st.session_state:
            st.session_state.mem_attempts = 0

        if "mem_score" not in st.session_state:
            st.session_state.mem_score = 0

        if "mem_total_time" not in st.session_state:
            st.session_state.mem_total_time = 0.0

        if "mem_round_start" not in st.session_state:
            st.session_state.mem_round_start = time.time()

        if "sequence" not in st.session_state:
            st.session_state.sequence = [
                random.choice([1, 2, 3])
                for _ in range(3)
            ]

        if "user_input" not in st.session_state:
            st.session_state.user_input = []

        if st.session_state.mem_score >= max_rounds:

            log_game_completion("Memory Sequence Flash")

            avg_time = round(
                st.session_state.mem_total_time / max_rounds,
                2
            )

            st.success("🎉 Memory Training Completed!")

            st.metric(
                "Avg Time per Pattern",
                f"{avg_time}s"
            )

            if st.button(
                "Play Again",
                key="restart_mem_limit"
            ):
                st.session_state.mem_attempts = 0
                st.session_state.mem_score = 0
                st.session_state.mem_total_time = 0.0
                st.session_state.mem_round_start = time.time()
                st.session_state.user_input = []
                st.session_state.sequence = [
                    random.choice([1, 2, 3])
                    for _ in range(3)
                ]
                st.session_state.logged_Memory_Sequence_Flash = False
                st.rerun()

        else:

            st.markdown(
                f"### Mastered Patterns: "
                f"{st.session_state.mem_score} / {max_rounds}"
            )

            st.info(
                f"Target Sequence Pattern: **"
                f"{' - '.join(map(str, st.session_state.sequence))}"
                f"**"
            )

            cols = st.columns(3)

            for i in range(1, 4):

                with cols[i - 1]:

                    if st.button(
                        f"Press {i}",
                        key=f"mem_btn_{i}"
                    ):

                        st.session_state.user_input.append(i)

                        current_idx = (
                            len(st.session_state.user_input) - 1
                        )

                        if (
                            st.session_state.user_input[current_idx]
                            != st.session_state.sequence[current_idx]
                        ):

                            st.session_state.mem_attempts += 1

                            st.error(
                                "Wrong sequence! Resetting pattern."
                            )

                            st.session_state.user_input = []

                            st.session_state.sequence = [
                                random.choice([1, 2, 3])
                                for _ in range(3)
                            ]

                            st.session_state.mem_round_start = time.time()

                            st.rerun()

                        elif (
                            len(st.session_state.user_input)
                            == len(st.session_state.sequence)
                        ):

                            elapsed = (
                                time.time()
                                - st.session_state.mem_round_start
                            )

                            st.session_state.mem_total_time += elapsed
                            st.session_state.mem_attempts += 1
                            st.session_state.mem_score += 1

                            st.success(
                                "Pattern Matched! ✨"
                            )

                            st.session_state.user_input = []

                            st.session_state.sequence = [
                                random.choice([1, 2, 3])
                                for _ in range(3)
                            ]

                            st.session_state.mem_round_start = time.time()

                            st.rerun()

        st.write("")

        if st.button(
            "Reset Session",
            key="rst_mem"
        ):
            st.session_state.mem_attempts = 0
            st.session_state.mem_score = 0
            st.session_state.mem_total_time = 0.0
            st.session_state.mem_round_start = time.time()
            st.session_state.user_input = []
            st.session_state.sequence = [
                random.choice([1, 2, 3])
                for _ in range(3)
            ]
            st.session_state.logged_Memory_Sequence_Flash = False
            st.rerun()


    # ============================================================
    # GAME 5: SPEED WORD SCRAMBLE
    # ============================================================

    elif game_choice == "5. Speed Word Scramble":

        st.subheader("🔤 Speed Word Scramble")

        st.write(
            "Unscramble 5 target words correctly to finish your session!"
        )

        max_rounds = 5

        word_bank = [
            "apple",
            "tiger",
            "house",
            "brain",
            "smart",
            "quick",
            "plant",
            "water"
        ]

        if "scramble_attempts" not in st.session_state:
            st.session_state.scramble_attempts = 0

        if "scramble_score" not in st.session_state:
            st.session_state.scramble_score = 0

        if "scramble_total_time" not in st.session_state:
            st.session_state.scramble_total_time = 0.0

        if "scramble_round_start" not in st.session_state:
            st.session_state.scramble_round_start = time.time()

        if "target_word_scramble" not in st.session_state:

            word = random.choice(word_bank)

            st.session_state.target_word_scramble = word

            st.session_state.scrambled_display = "".join(
                random.sample(word, len(word))
            )

        if st.session_state.scramble_score >= max_rounds:

            log_game_completion("Speed Word Scramble")

            avg_time = round(
                st.session_state.scramble_total_time / max_rounds,
                2
            )

            st.success(
                "🎉 Word Scramble Session Complete!"
            )

            st.metric(
                "Avg Time per Word",
                f"{avg_time}s"
            )

            if st.button(
                "Play Again",
                key="restart_scramble_limit"
            ):

                st.session_state.scramble_attempts = 0
                st.session_state.scramble_score = 0
                st.session_state.scramble_total_time = 0.0
                st.session_state.scramble_round_start = time.time()
                st.session_state.logged_Speed_Word_Scramble = False

                word = random.choice(word_bank)

                st.session_state.target_word_scramble = word

                st.session_state.scrambled_display = "".join(
                    random.sample(word, len(word))
                )

                st.rerun()

        else:

            st.markdown(
                f"### Words Mastered: "
                f"{st.session_state.scramble_score} / {max_rounds}"
            )

            st.markdown(
                f"### Unscramble this word: "
                f"**{st.session_state.scrambled_display.upper()}**"
            )

            user_guess = st.text_input(
                "Type your guessed word here:",
                key=f"scramble_input_{st.session_state.scramble_attempts}"
            )

            if st.button(
                "Submit Guess",
                key=f"submit_scramble_{st.session_state.scramble_attempts}"
            ):

                if (
                    user_guess.strip().lower()
                    == st.session_state.target_word_scramble
                ):

                    elapsed = (
                        time.time()
                        - st.session_state.scramble_round_start
                    )

                    st.session_state.scramble_total_time += elapsed
                    st.session_state.scramble_score += 1
                    st.session_state.scramble_attempts += 1

                    st.success("Correct! 🎉")

                    word = random.choice(word_bank)

                    st.session_state.target_word_scramble = word

                    st.session_state.scrambled_display = "".join(
                        random.sample(word, len(word))
                    )

                    st.session_state.scramble_round_start = time.time()

                    st.rerun()

                else:

                    st.session_state.scramble_attempts += 1

                    st.error("Not quite right, try again!")

        st.write("")

        if st.button(
            "Reset Session",
            key="rst_scramble"
        ):
            st.session_state.scramble_attempts = 0
            st.session_state.scramble_score = 0
            st.session_state.scramble_total_time = 0.0
            st.session_state.scramble_round_start = time.time()
            st.session_state.logged_Speed_Word_Scramble = False

            word = random.choice(word_bank)

            st.session_state.target_word_scramble = word

            st.session_state.scrambled_display = "".join(
                random.sample(word, len(word))
            )

            st.rerun()
    elif game_choice == "6. Visual & Picture Training":

        st.subheader("🖼️ Visual & Picture Training")

        games_visual.run_visual_games()
if __name__ == "__main__":
    run_games()