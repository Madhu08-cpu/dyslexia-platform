import cv2
import mediapipe as mp
import time
from collections import Counter

# Confidence scores
confidence_map = {
    "HAPPY": 9, "SURPRISED": 7, "NEUTRAL": 5, 
    "CONFUSED": 3, "SAD": 2, "ANGRY": 1, "FRUSTRATED": 3, "FEARFUL": 4, "DISGUSTED": 3
}

class EmotionEngine:
    def __init__(self, stabilization_frames=15):
        self.stabilization_frames = stabilization_frames
        self.frame_buffer = []
        self.stable_emotion = "NEUTRAL"

    def process_frame(self, frame, landmarker):
        """
        Processes frame, calculates landmarks, stabilizes emotion via buffer,
        and logs to CSV when a transition occurs.
        """
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        results = landmarker.detect_for_video(mp_image, int(time.time() * 1000))
        
        detected = "NEUTRAL"
        
        if results.face_landmarks:
            landmarks = results.face_landmarks[0]
            
            # Calculate Reference Width (Temple-to-temple)
            face_width = abs(landmarks[454].x - landmarks[234].x)
            if face_width > 0:
                # Calculate Normalized Ratios
                smile_ratio = abs(landmarks[61].x - landmarks[291].x) / face_width
                mouth_ratio = abs(landmarks[13].y - landmarks[14].y) / face_width
                brow_ratio = abs(landmarks[70].x - landmarks[300].x) / face_width

                # --- CLEANED EMOTION MAPPING (No undefined variables) ---
                if mouth_ratio > 0.15: 
                    detected = "SURPRISED"
                elif smile_ratio > 0.22: 
                    detected = "HAPPY"
                elif mouth_ratio < 0.025 and smile_ratio < 0.15: 
                    detected = "SAD"
                elif brow_ratio < 0.07: 
                    detected = "FRUSTRATED"
                elif brow_ratio > 0.24: 
                    detected = "CONFUSED"
                else:
                    detected = "NEUTRAL"
            
            # --- BUFFER STABILITY LOGIC ---
            self.frame_buffer.append(detected)
            if len(self.frame_buffer) > self.stabilization_frames:
                self.frame_buffer.pop(0)
            
            # Use Counter for stable smoothing
            if len(self.frame_buffer) > 0:
                most_common_emotion = Counter(self.frame_buffer).most_common(1)[0][0]
                if most_common_emotion != self.stable_emotion:
                    self.stable_emotion = most_common_emotion
                    # Uncomment if data_logger is linked: log_to_csv(self.stable_emotion, confidence_map.get(self.stable_emotion, 5), "Reading")

        return self.stable_emotion, confidence_map.get(detected, 5)