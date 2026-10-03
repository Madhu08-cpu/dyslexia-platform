import cv2
import mediapipe as mp
import time
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from data_logger import log_to_csv # Assuming this is your existing logger

# Mapping
confidence_map = {"HAPPY": 9, "SURPRISED": 7, "NEUTRAL": 5, "CONFUSED": 3, "SAD": 2, "ANGRY": 1, "FRUSTRATED": 3}

def process_emotion(frame, landmarker, session_state):
    """
    Processes a frame and returns the detected emotion and confidence score.
    """
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    results = landmarker.detect_for_video(mp_image, int(time.time() * 1000))
    
    detected = "NEUTRAL"
    
    if results.face_landmarks:
        face_landmarks = results.face_landmarks[0]
        # Landmarks
        smile_w = abs(face_landmarks[61].x - face_landmarks[291].x)
        brow_d = abs(face_landmarks[70].x - face_landmarks[300].x)
        mouth_h = abs(face_landmarks[13].y - face_landmarks[14].y)
        
        # Logic
        if mouth_h > 0.10: detected = "SURPRISED"
        elif smile_w > 0.20: detected = "HAPPY"
        elif smile_w < 0.14 and mouth_h > 0.03: detected = "SAD"
        elif brow_d < 0.07: detected = "FRUSTRATED"
        elif brow_d > 0.17: detected = "CONFUSED"
        
        # Stability
        if detected == session_state.get('current_emotion'):
            if time.time() - session_state.get('emotion_start_time', time.time()) >= 3.0:
                session_state['display_emotion'] = detected
        else:
            session_state['current_emotion'] = detected
            session_state['emotion_start_time'] = time.time()

    return session_state.get('display_emotion', 'NEUTRAL'), confidence_map.get(detected, 5)