import datetime
import json  # EDIT 1: Imported json module
import os
import requests
import streamlit as st
import ui

# Fallback offline dictionary for instant testing if API is unreachable
LOCAL_PINCODE_DB = {
    "641001": {
        "state": "Tamil Nadu",
        "district": "Coimbatore",
        "taluks": [
            "Coimbatore Central",
            "Coimbatore Bazaar",
            "R.S. Puram",
            "Town Hall",
        ],
    },
    "560001": {
        "state": "Karnataka",
        "district": "Bengaluru",
        "taluks": [
            "Bangalore G.O.O.",
            "Vidhana Soudha",
            "High Court",
            "Cubbon Park",
        ],
    },
    "400001": {
        "state": "Maharashtra",
        "district": "Mumbai",
        "taluks": ["Mumbai G.P.O.", "Fort", "Stock Exchange"],
    },
}


# EDIT 2: Helper function to save broadcasted tasks to JSON
def save_task_to_db(new_task):
  """Saves a new task to the shared data file."""
  data = {"tasks": [], "students": []}
  if os.path.exists("app_data.json"):
    with open("app_data.json", "r") as f:
      try:
        data = json.load(f)
      except Exception:
        pass

  data["tasks"].append(new_task)

  with open("app_data.json", "w") as f:
    json.dump(data, f, indent=4)


@st.cache_data(ttl=3600)
def fetch_location_by_pincode(pincode):
  """Calls India Post API with browser headers, with local fallback if offline."""
  url = f"https://api.postalpincode.in/pincode/{pincode}"

  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
          " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
      )
  }

  try:
    response = requests.get(url, headers=headers, timeout=5)
    if response.status_code == 200:
      data = response.json()
      if data and data[0].get("Status") == "Success":
        post_offices = data[0]["PostOffice"]
        state = post_offices[0]["State"]
        district = post_offices[0]["District"]
        taluks = sorted(list({po["Name"] for po in post_offices}))
        return {
            "success": True,
            "state": state,
            "district": district,
            "taluks": taluks,
        }
  except Exception:
    pass

  if pincode in LOCAL_PINCODE_DB:
    return {"success": True, **LOCAL_PINCODE_DB[pincode]}

  return {"success": False}


def run_educator_portal():
  ui.render_header(
      "Educator & Parent Portal",
      "Search and auto-detect institution details via PIN Code API.",
      "🏫",
  )

  # --- PIN CODE INPUT ---
  ui.render_card_start("⚡ Auto-Detect Location via PIN Code")

  pincode_input = st.text_input(
      "Enter 6-Digit PIN Code (e.g., 560001, 641001, 400001)",
      max_chars=6,
      placeholder="Type 6-digit PIN code...",
  )

  # Defaults
  state_val = "Enter PIN Code First"
  district_val = "Enter PIN Code First"
  taluk_options = ["Enter PIN Code First"]

  if len(pincode_input) == 6 and pincode_input.isdigit():
    with st.spinner("Fetching location data..."):
      result = fetch_location_by_pincode(pincode_input)
      if result["success"]:
        state_val = result["state"]
        district_val = result["district"]
        taluk_options = result["taluks"]
        st.success(f"Location loaded for PIN Code {pincode_input}!")
      else:
        st.error(
            "PIN Code not found. Please verify the 6-digit code or enter details"
            " manually."
        )

  ui.render_card_end()

  st.markdown("<br>", unsafe_allow_html=True)

  # --- AUTO-FILLED DETAILS ---
  ui.render_card_start("🏫 Institution Details")

  col1, col2 = st.columns(2)

  with col1:
    st.text_input("State / Region", value=state_val, disabled=True)
    selected_taluk = st.selectbox("Select Area / Taluk", taluk_options)

  with col2:
    st.text_input("District / City", value=district_val, disabled=True)
    school_name = st.text_input(
        "School / Institution Name",
        placeholder="Type school or college name here...",
    )

  ui.render_card_end()

  # Active Selection Display
  if school_name and state_val != "Enter PIN Code First":
    st.markdown("<br>", unsafe_allow_html=True)
    ui.render_card_start("🎯 Active Selection Details")
    st.markdown(
        f"""
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px;">
                <div><span style="color:#94A3B8; font-size:0.8rem; font-weight:700;">STATE</span><br><strong>{state_val}</strong></div>
                <div><span style="color:#94A3B8; font-size:0.8rem; font-weight:700;">DISTRICT</span><br><strong>{district_val}</strong></div>
                <div><span style="color:#94A3B8; font-size:0.8rem; font-weight:700;">AREA/TALUK</span><br><strong>{selected_taluk}</strong></div>
                <div><span style="color:#94A3B8; font-size:0.8rem; font-weight:700;">SCHOOL</span><br><strong style="color:#2563EB;">{school_name}</strong></div>
            </div>
        """,
        unsafe_allow_html=True,
    )
    ui.render_card_end()

    # EDIT 3: Added Broadcast Assignment Form at the end of the page
    st.markdown("<br>", unsafe_allow_html=True)
    ui.render_card_start("👩‍🏫 Broadcast Reading Assignment")

    with st.form("assign_task_form"):
      task_title = st.text_input("Task Title", "Weekly Comprehension Exercise")
      target_grade = st.selectbox(
          "Target Grade",
          ["Grade 1-3", "Grade 4-6", "Grade 7-9", "Grade 10-12"],
      )
      reading_passage = st.text_area(
          "Passage / Instructions",
          "Read Chapter 2 and complete the vocabulary quiz.",
      )

      if st.form_submit_button("Broadcast Task to Students"):
        task_data = {
            "school": school_name.strip(),
            "state": state_val,
            "district": district_val,
            "taluk": selected_taluk,
            "title": task_title,
            "grade": target_grade,
            "passage": reading_passage,
            "date_created": str(datetime.date.today()),
        }
        save_task_to_db(task_data)
        st.success(f"Task broadcasted to all students at '{school_name}'!")

    ui.render_card_end()