import streamlit as st
import cv2

st.title("Camera Test")
run = st.checkbox('Run Camera')
FRAME_WINDOW = st.image([])

if run:
    cap = cv2.VideoCapture(0)
    while run:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture frame.")
            break
        # Convert BGR (OpenCV format) to RGB (Streamlit format)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(frame)
    cap.release()