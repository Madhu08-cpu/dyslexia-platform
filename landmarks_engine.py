import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

def initialize_landmarker(model_path='face_landmarker.task'):
    """
    Initializes the MediaPipe FaceLandmarker.
    """
    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.FaceLandmarkerOptions(
        base_options=base_options, 
        running_mode=vision.RunningMode.VIDEO
    )
    return vision.FaceLandmarker.create_from_options(options)

def get_landmarks(frame, landmarker, timestamp_ms):
    """
    Converts frame to MediaPipe image and extracts landmarks.
    """
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB, 
        data=frame
    )
    # Detect landmarks
    results = landmarker.detect_for_video(mp_image, timestamp_ms)
    return results

def extract_landmark_coords(face_landmarks):
    """
    Helper to extract specific indices for emotion calculation.
    """
    if not face_landmarks:
        return None
        
    # Example: returning a dictionary of points used in your emotion logic
    return {
        "smile_left": face_landmarks[61],
        "smile_right": face_landmarks[291],
        "brow_left": face_landmarks[70],
        "brow_right": face_landmarks[300],
        "mouth_top": face_landmarks[13],
        "mouth_bottom": face_landmarks[14]
    }