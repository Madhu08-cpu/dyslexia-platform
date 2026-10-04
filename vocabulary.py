import datetime
import os
import pandas as pd
import streamlit as st
import ui


def run_vocab_vault():
  # --- UI HEADER ---
  ui.render_header(
      "Vocabulary Vault & Notes",
      "Save difficult words, meanings, or quick reading reflections here to"
      " review later.",
      "📚",
  )

  VOCAB_FILE = "vocabulary.csv"

  # --- INPUT CARD CONTAINER ---
  ui.render_card_start("Add New Word / Note")

  with st.form("vocab_form", clear_on_submit=True):
    new_word = st.text_input("Difficult Word / Topic")
    new_note = st.text_area("Definition / Reflection Notes")

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("Save to Vault")

    if submitted:
      if new_word and new_note:
        vocab_df = pd.DataFrame({
            "Username": [st.session_state.user_name],
            "Word": [new_word.strip()],
            "Note": [new_note.strip()],
            "Date": [str(datetime.date.today())],
        })
        file_exists = os.path.exists(VOCAB_FILE)
        vocab_df.to_csv(
            VOCAB_FILE, mode="a", header=not file_exists, index=False
        )
        st.success(f"Saved '{new_word}' to your vault!")
      else:
        st.error("Please fill in both fields.")

  ui.render_card_end()

  st.markdown("<br>", unsafe_allow_html=True)

  # --- SAVED WORDS & NOTES CARD CONTAINER ---
  ui.render_card_start("📖 Your Saved Words & Notes")

  if os.path.exists(VOCAB_FILE):
    df_vocab = pd.read_csv(VOCAB_FILE)

    if "Username" in df_vocab.columns:
      user_vocab = df_vocab[
          df_vocab["Username"].astype(str) == str(st.session_state.user_name)
      ]
    else:
      user_vocab = pd.DataFrame()

    if not user_vocab.empty:
      # Render stat widget inside card
      ui.render_stat_card(
          "Vault Collection",
          f"{len(user_vocab)} Words",
          badge_text="Saved Items",
      )
      st.markdown("<br>", unsafe_allow_html=True)

      st.dataframe(
          user_vocab[["Word", "Note", "Date"]], use_container_width=True
      )

      st.markdown("<br>", unsafe_allow_html=True)

      # Quick delete feature inside styled area
      words_list = user_vocab["Word"].tolist()
      word_to_delete = st.selectbox(
          "Select a word to remove if mastered:",
          ["-- Select word --"] + words_list,
      )

      if word_to_delete != "-- Select word --":
        if st.button("Remove Selected Word"):
          df_vocab = df_vocab[
              ~(
                  (
                      df_vocab["Username"].astype(str)
                      == str(st.session_state.user_name)
                  )
                  & (df_vocab["Word"] == word_to_delete)
              )
          ]
          df_vocab.to_csv(VOCAB_FILE, index=False)
          st.success(f"Removed '{word_to_delete}' from your vault.")
          st.rerun()
    else:
      st.info("Your vault is currently empty. Add your first word above!")
  else:
    st.info("No vocabulary records found yet.")

  ui.render_card_end()