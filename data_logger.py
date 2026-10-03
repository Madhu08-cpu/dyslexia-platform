import csv
import os
import time

# Define the log file location
LOG_FILE = 'student_performance.csv'

def initialize_log():
    """Creates the CSV file with headers if it doesn't exist."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Timestamp', 'Emotion', 'ConfidenceScore', 'Status'])

def log_event(emotion, confidence, status):
    """Appends a new reading session event to the CSV file."""
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            time.strftime("%Y-%m-%d %H:%M:%S"), 
            emotion, 
            confidence, 
            status
        ])