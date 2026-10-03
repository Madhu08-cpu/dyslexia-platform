import streamlit as st
import cv2
import mediapipe as mp
import time
import os
import csv
import pandas as pd
import plotly.express as px
import speech_recognition as sr
from collections import deque
from difflib import SequenceMatcher
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from gtts import gTTS
import tempfile


# ============================================================
# 1. EMOTION ENGINE
# ============================================================

class EmotionEngine:
    def __init__(self):
        self.last_emotions = deque(maxlen=15)

    def process_frame(self, landmarks):
        face_width = abs(landmarks[234].x - landmarks[454].x)

        if face_width == 0:
            return "NEUTRAL"

        mouth_h = abs(landmarks[13].y - landmarks[14].y) / face_width
        brow_dist = abs(landmarks[70].y - landmarks[105].y) / face_width

        if mouth_h > 0.15:
            emotion = "HAPPY"
        elif brow_dist > 0.08:
            emotion = "SURPRISED"
        elif mouth_h < 0.02:
            emotion = "SAD"
        else:
            emotion = "NEUTRAL"

        self.last_emotions.append(emotion)

        return max(
            set(self.last_emotions),
            key=self.last_emotions.count
        )


# ============================================================
# 2. FILE CONFIGURATION
# ============================================================

FILE_NAME = "student_performance.csv"


# ============================================================
# 3. SPEECH INPUT
# ============================================================

def get_speech_input():
    """
    Captures audio from the microphone and returns
    the transcribed text.
    """

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:

            st.info("Adjusting microphone for background noise...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            st.info("🎤 Listening... Please read the sentence.")

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

            text = recognizer.recognize_google(audio)

            return text.lower()

    except sr.WaitTimeoutError:
        return "Error: Listening timed out."

    except sr.UnknownValueError:
        return "Error: Could not understand audio."

    except sr.RequestError:
        return "Error: Could not request results from Google Speech Recognition API."

    except Exception as e:
        return f"Error: {str(e)}"


# ============================================================
# 4. SAVE PERFORMANCE TO CSV
# ============================================================

def log_to_csv(username, emotion, duration, accuracy):

    file_exists = os.path.exists(FILE_NAME)

    with open(
        FILE_NAME,
        "a",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "Time",
                "Username",
                "Emotion",
                "Duration",
                "Accuracy"
            ])

        writer.writerow([
            time.strftime("%H:%M:%S"),
            username,
            emotion,
            f"{duration:.2f}",
            f"{accuracy:.2f}"
        ])


# ============================================================
# 5. TEXT-TO-SPEECH
# ============================================================

def generate_speech(text):

    try:

        tts = gTTS(
            text=text,
            lang="en"
        )

        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        )

        tts.save(temp_file.name)

        return temp_file.name

    except Exception as e:
        st.error(f"Audio generation failed: {e}")
        return None


# ============================================================
# 6. INITIALIZE SESSION STATE
# ============================================================

def initialize_session():

    if "engine" not in st.session_state:
        st.session_state.engine = EmotionEngine()

    if "status" not in st.session_state:
        st.session_state.status = "IDLE"

    if "last_emotion" not in st.session_state:
        st.session_state.last_emotion = "NEUTRAL"

    if "last_session_report" not in st.session_state:
        st.session_state.last_session_report = None

    if "start_time" not in st.session_state:
        st.session_state.start_time = None


# ============================================================
# 7. MAIN APPLICATION
# ============================================================

def run_app():

    initialize_session()

    st.title(
        "🧠 NeuroRead AI Platform - Reading Session & Analytics"
    )

    current_user = st.session_state.get(
        "user_name",
        "Guest"
    )

    st.info(
        f"Active Session User: **{current_user}**"
    )

    current_sentence = st.session_state.get(
        "selected_story",
        "The quick brown fox jumps over the lazy dog."
    )

    # --------------------------------------------------------
    # MAIN COLUMNS
    # --------------------------------------------------------

    col_ctrl, col_cam = st.columns([1, 2])

    # ========================================================
    # LEFT SIDE - SESSION CONTROLS
    # ========================================================

    with col_ctrl:

        st.subheader("🎛️ Session Controls")

        # ----------------------------------------------------
        # DYSLEXIA MODE
        # ----------------------------------------------------

        dyslexia_mode = st.checkbox(
            "🔤 Dyslexia-Friendly View",
            value=True
        )

        if dyslexia_mode:

            st.markdown(
                """
                <style>
                .dyslexia-text {
                    font-family: Arial, sans-serif;
                    font-size: 26px;
                    line-height: 1.8;
                    letter-spacing: 1.5px;
                    word-spacing: 4px;
                    background-color: #fffbea;
                    padding: 20px;
                    border-radius: 12px;
                    border: 2px solid #dddddd;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

        # ----------------------------------------------------
        # START READING
        # ----------------------------------------------------

        if st.button(
            "▶️ Start Reading",
            use_container_width=True
        ):

            st.session_state.status = "READING"
            st.session_state.start_time = time.time()

            st.session_state.last_emotion = "NEUTRAL"

            st.session_state.engine = EmotionEngine()

            st.session_state.pop(
                "last_session_report",
                None
            )

            st.rerun()

        # ----------------------------------------------------
        # TEXT TO SPEECH
        # ----------------------------------------------------

        if st.button(
            "🔊 Listen to Target Sentence",
            use_container_width=True
        ):

            audio_file = generate_speech(
                current_sentence
            )

            if audio_file:
                st.audio(
                    audio_file,
                    format="audio/mp3"
                )

        # ----------------------------------------------------
        # FINISH AND SAVE
        # ----------------------------------------------------

        if st.button(
            "⏹️ Finish & Save",
            use_container_width=True
        ):

            if st.session_state.get("start_time"):

                duration = (
                    time.time()
                    - st.session_state.start_time
                )

            else:

                duration = 0.0

            st.session_state.status = "PROCESSING"

            st.info(
                "🎤 Listening for your reading..."
            )

            spoken = get_speech_input()

            # ------------------------------------------------
            # CALCULATE ACCURACY
            # ------------------------------------------------

            if spoken.startswith("Error:"):

                st.error(spoken)

                accuracy = 0.0

            else:

                accuracy = (
                    SequenceMatcher(
                        None,
                        current_sentence.lower().strip(),
                        spoken.lower().strip()
                    ).ratio()
                    * 100
                )

            # ------------------------------------------------
            # GET EMOTION
            # ------------------------------------------------

            emotion = st.session_state.get(
                "last_emotion",
                "NEUTRAL"
            )

            # ------------------------------------------------
            # SAVE TO CSV
            # ------------------------------------------------

            log_to_csv(
                current_user,
                emotion,
                duration,
                accuracy
            )

            # ------------------------------------------------
            # CREATE REPORT
            # ------------------------------------------------

            st.session_state.last_session_report = {

                "story": current_sentence,

                "spoken": spoken,

                "duration": f"{duration:.2f}s",

                "accuracy": f"{accuracy:.2f}%",

                "emotion": emotion
            }

            st.session_state.status = "IDLE"

            st.session_state.start_time = None

            st.rerun()

    # ========================================================
    # RIGHT SIDE - CAMERA
    # ========================================================

    with col_cam:

        if st.session_state.status == "READING":

            st.markdown(
                "### 📖 Please read aloud:"
            )

            # ------------------------------------------------
            # DISPLAY TARGET SENTENCE
            # ------------------------------------------------

            if dyslexia_mode:

                st.markdown(
                    f"""
                    <div class="dyslexia-text">
                        {current_sentence}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.success(
                    f"**{current_sentence}**"
                )

            st.markdown("---")

            st.markdown(
                "### 📷 Live Emotion Detection"
            )

            FRAME_WINDOW = st.image([])

            cap = cv2.VideoCapture(0)

            # ------------------------------------------------
            # CHECK CAMERA
            # ------------------------------------------------

            if not cap.isOpened():

                st.error(
                    "❌ Could not open camera. "
                    "Please check your webcam."
                )

                st.session_state.status = "IDLE"

                return

            # ------------------------------------------------
            # MEDIAPIPE MODEL
            # ------------------------------------------------

            model_path = os.path.join(
                os.getcwd(),
                "face_landmarker.task"
            )

            if not os.path.exists(model_path):

                st.error(
                    "❌ Error: 'face_landmarker.task' "
                    "file is missing from the project directory."
                )

                cap.release()

                st.session_state.status = "IDLE"

                return

            base_options = python.BaseOptions(
                model_asset_path=model_path
            )

            options = vision.FaceLandmarkerOptions(
                base_options=base_options,
                running_mode=vision.RunningMode.VIDEO,
                num_faces=1
            )

            # ------------------------------------------------
            # CREATE LANDMARKER
            # ------------------------------------------------

            try:

                with vision.FaceLandmarker.create_from_options(
                    options
                ) as landmarker:

                    previous_timestamp = 0

                    while (
                        st.session_state.status
                        == "READING"
                    ):

                        ret, frame = cap.read()

                        if not ret:

                            st.error(
                                "❌ Failed to grab frame "
                                "from camera."
                            )

                            break

                        # ------------------------------------
                        # FLIP CAMERA
                        # ------------------------------------

                        frame = cv2.flip(
                            frame,
                            1
                        )

                        # ------------------------------------
                        # CONVERT BGR TO RGB
                        # ------------------------------------

                        rgb_frame = cv2.cvtColor(
                            frame,
                            cv2.COLOR_BGR2RGB
                        )

                        mp_img = mp.Image(
                            image_format=mp.ImageFormat.SRGB,
                            data=rgb_frame
                        )
                        timestamp = int(
                            time.time() * 1000
                        )

                        if timestamp <= previous_timestamp:
                            timestamp = (
                                previous_timestamp + 1
                            )

                        previous_timestamp = timestamp
                        results = (
                            landmarker.detect_for_video(
                                mp_img,
                                timestamp
                            )
                        )

                        emotion = "NEUTRAL"
                        if results.face_landmarks:

                            landmarks = (
                                results.face_landmarks[0]
                            )

                            for lm in landmarks:

                                x = int(
                                    lm.x
                                    * frame.shape[1]
                                )

                                y = int(
                                    lm.y
                                    * frame.shape[0]
                                )

                                cv2.circle(
                                    frame,
                                    (x, y),
                                    1,
                                    (0, 255, 0),
                                    -1
                                )
                            emotion = (
                                st.session_state.engine
                                .process_frame(
                                    landmarks
                                )
                            )
                        st.session_state.last_emotion = (
                            emotion
                        )
                        cv2.rectangle(
                            frame,
                            (15, 15),
                            (320, 75),
                            (0, 0, 0),
                            -1
                        )

                        cv2.putText(
                            frame,
                            f"Emotion: {emotion}",
                            (30, 55),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 255, 0),
                            2
                        )
                        FRAME_WINDOW.image(
                            cv2.cvtColor(
                                frame,
                                cv2.COLOR_BGR2RGB
                            ),
                            channels="RGB"
                        )

                        time.sleep(0.01)

            except Exception as e:

                st.error(
                    f"Emotion detection error: {e}"
                )

            finally:

                cap.release()

        else:

            st.info(
                "📷 Camera is idle. "
                "Click **Start Reading** on the left "
                "to begin your session."
            )
def display_session_report():

    if (
        "last_session_report"
        not in st.session_state
    ):
        return

    report = (
        st.session_state.last_session_report
    )

    if not report:
        return

    st.divider()

    st.success(
        "✅ Session Saved Successfully!"
    )

    st.subheader(
        "📋 Latest Completed Session Report"
    )

    report_df = pd.DataFrame({

        "Metric": [

            "Target Story Text",

            "Detected Speech",

            "Duration",

            "Accuracy",

            "Emotion Detected"

        ],

        "Value": [

            report["story"],

            report["spoken"],

            report["duration"],

            report["accuracy"],

            report["emotion"]

        ]

    })

    st.table(report_df)

def display_analytics(current_user):

    st.divider()

    st.subheader(
        f"📈 Performance History for {current_user}"
    )

    if not os.path.exists(FILE_NAME):

        st.info(
            "Performance log file has not been "
            "initialized yet."
        )

        return

    try:

        df = pd.read_csv(
            FILE_NAME,
            on_bad_lines="skip"
        )

    except Exception as e:

        st.error(
            f"Could not read performance file: {e}"
        )

        return

    required_columns = [
        "Time",
        "Username",
        "Emotion",
        "Duration",
        "Accuracy"
    ]

    for column in required_columns:

        if column not in df.columns:

            df[column] = None

    df = df[
        df["Username"].astype(str)
        == str(current_user)
    ]
    if not df.empty:

        df["Accuracy"] = pd.to_numeric(
            df["Accuracy"],
            errors="coerce"
        )

        df["Duration"] = pd.to_numeric(
            df["Duration"],
            errors="coerce"
        )
    if df.empty:

        st.info(
            f"No prior records found for "
            f"**{current_user}**. "
            "Complete a session above to build "
            "your individual history!"
        )

        return

    col_m1, col_m2, col_m3 = st.columns(3)

    col_m1.metric(
        label="📚 Total Sessions",
        value=len(df)
    )
    latest_accuracy = float(
        df.iloc[-1]["Accuracy"]
    )

    col_m2.metric(
        label="🎯 Latest Accuracy",
        value=f"{latest_accuracy:.2f}%"
    )

    if len(df) > 1:

        first_accuracy = float(
            df.iloc[0]["Accuracy"]
        )

        improvement = (
            latest_accuracy
            - first_accuracy
        )

        col_m3.metric(
            label="📈 Accuracy Improvement",
            value=f"{improvement:+.2f}%",
            delta=f"{improvement:+.2f}%"
        )

    else:

        col_m3.metric(
            label="📈 Accuracy Improvement",
            value="0.00%"
        )
    if "Accuracy" in df.columns:

        chart_df = df.copy()

        chart_df["Session"] = range(
            1,
            len(chart_df) + 1
        )

        fig = px.line(
            chart_df,
            x="Session",
            y="Accuracy",
            markers=True,
            title=(
                f"📊 Accuracy Trend for "
                f"{current_user}"
            ),
            labels={
                "Accuracy": "Accuracy (%)",
                "Session": "Session Number"
            }
        )

        fig.update_yaxes(
            range=[0, 100]
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
    if "Emotion" in df.columns:

        emotion_counts = (
            df["Emotion"]
            .value_counts()
            .reset_index()
        )

        emotion_counts.columns = [
            "Emotion",
            "Count"
        ]

        if not emotion_counts.empty:

            fig_emotion = px.bar(
                emotion_counts,
                x="Emotion",
                y="Count",
                title=(
                    f"😊 Emotion Detection "
                    f"History for {current_user}"
                )
            )

            st.plotly_chart(
                fig_emotion,
                use_container_width=True
            )
    st.write(
        "### 📋 Your Past Sessions"
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    csv_data = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        label="📥 Download Your Personal Report (CSV)",

        data=csv_data,

        file_name=(
            f"{current_user}"
            "_performance_report.csv"
        ),

        mime="text/csv",

        use_container_width=True
    )

def main():

    initialize_session()

    current_user = st.session_state.get(
        "user_name",
        "Guest"
    )

    run_app()

    display_session_report()

    display_analytics(
        current_user
    )

if __name__ == "__main__":
    main()