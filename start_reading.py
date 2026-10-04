import json
import os
import app  # Live reading engine with OpenCV / MediaPipe camera emotion detection
import streamlit as st
import ui


def load_school_tasks(school_name):
  """Loads tasks assigned to a specific school from app_data.json."""
  if not os.path.exists("app_data.json"):
    return []
  try:
    with open("app_data.json", "r") as f:
      data = json.load(f)
      return [
          t
          for t in data.get("tasks", [])
          if t.get("school", "").strip().lower() == school_name.strip().lower()
      ]
  except Exception:
    return []


def run_start_reading():
  ui.render_header(
      "Student Practice & Reading Portal",
      "Select your school to load assigned tasks or practice independently.",
      "📖",
  )

  # --- STEP 1: SCHOOL & ASSIGNMENT SELECTION ---
  ui.render_card_start("🏫 Select Your School")
  student_school = st.text_input(
      "Enter Your School Name", placeholder="e.g., VD HEGADE"
  )
  ui.render_card_end()

  st.markdown("<br>", unsafe_allow_html=True)

  # --- STEP 2: RENDER ASSIGNED TASKS ---
  if student_school.strip():
    tasks = load_school_tasks(student_school)

    ui.render_card_start(f"📋 Teacher Assignments for '{student_school}'")

    if not tasks:
      st.info(
          f"No active tasks assigned for '{student_school}' yet. You can"
          " practice general reading below!"
      )
    else:
      for idx, task in enumerate(tasks, 1):
        title = task.get("title", f"Assignment #{idx}")
        grade = task.get("grade", "General")
        passage_content = task.get("passage") or task.get("text", "")

        with st.expander(f"📌 Assignment #{idx}: {title} ({grade})"):
          st.write(f"**Instructions / Passage:** {passage_content}")

          if st.button(f"Start Reading Task #{idx}", key=f"start_btn_{idx}"):
            # Sync target passage text with app.py reading engine state
            st.session_state["target_text"] = passage_content
            st.session_state["active_passage"] = passage_content
            st.session_state["active_title"] = title
            st.success(
                f"Loaded '{title}' into the Live Reader below! Scroll down to"
                " begin."
            )

    ui.render_card_end()

  # --- STEP 3: GENERAL PRACTICE FALLBACK ---
  st.markdown("<br>", unsafe_allow_html=True)
  ui.render_card_start("📚 General Practice Mode")
  st.write("Or choose a pre-loaded passage to practice on your own:")

  sample_passages = {
      "The Clever Fox": "The quick brown fox jumps over the lazy dog.",
      "Space Exploration": (
          "Astronauts travel into space to explore distant stars and planets."
      ),
      "The Ocean World": (
          "Dolphins and whales swim gracefully across the deep blue sea."
      ),
  }

  selected_sample = st.selectbox(
      "Select Sample Passage", list(sample_passages.keys())
  )

  if st.button("Load Practice Passage"):
    passage_text = sample_passages[selected_sample]
    st.session_state["target_text"] = passage_text
    st.session_state["active_passage"] = passage_text
    st.session_state["active_title"] = selected_sample
    st.success(f"Loaded '{selected_sample}' into the reading engine!")

  ui.render_card_end()

  st.markdown("<br><hr>", unsafe_allow_html=True)

  # --- STEP 4: WEBCAM & LIVE EMOTION READING ENGINE ---
  # Invokes the full OpenCV camera and speech detection logic in app.py
  app.run_app()


if __name__ == "__main__":
  run_start_reading()