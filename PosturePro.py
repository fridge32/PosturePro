import cv2
import mediapipe as mp
import numpy as np
import math
import time
import pygame

# Initialize Pygame and load a sound file ('sound.wav') for the posture alert
pygame.mixer.init()
sound = pygame.mixer.Sound('sound.wav')
played = False  

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose

# Initialize webcam
cap = cv2.VideoCapture(0)

cv2.namedWindow('PosturePro', cv2.WINDOW_NORMAL)

# Initialize variables for posture monitoring
perfect_posture = None
bad_posture_timer = None  # Timer for bad posture duration
bad_posture_alert = False  # Flag to indicate if bad posture alert is displayed
good_posture_start_time = None  # Timer for good posture duration
video_paused = False  # Flag to track if the video is paused

# Default deviation angle and time threshold
deviation_angle_threshold = 5
time_threshold = 5.0

# Function to calculate the angle between three points
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = round(np.abs(radians * 180.0 / np.pi), 1)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle

# Function to display the perfect posture angle in the top right corner
def display_perfect_posture_angle(image, perfect_posture, deviation_angle_threshold, time_threshold):
    if perfect_posture is not None:
        # Display perfect posture angle
        cv2.putText(image, f'Perfect Angle: {max(0, perfect_posture)}', 
                    (int(frame.shape[1] * 0.70), 25),  # Shifted to the right
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        
        # Display current angle and time thresholds
        cv2.putText(image, f'Current Angle: {max(0, deviation_angle_threshold)}', 
                    (int(frame.shape[1] * 0.70), 50),  # Shifted to the right
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        
        cv2.putText(image, f'Current Time: {max(0, time_threshold)}', 
                    (int(frame.shape[1] * 0.70), 75),  # Shifted to the right
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

# Main posture monitoring loop
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        if not video_paused:
            ret, frame = cap.read()

        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Make detection
        results = pose.process(image)
    
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x, landmarks[mp_pose.PoseLandmark.NOSE.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            
            # Calculate angle
            angle = calculate_angle(shoulder, nose, wrist)
            
            # Visualize angle
            cv2.putText(image, str(max(0, angle)),  # Ensure angle doesn't go below zero
                        tuple(np.multiply(nose, [700, 480]).astype(int)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            
            # Visualize nose and shoulder landmarks
            for landmark in [mp_pose.PoseLandmark.NOSE, mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.RIGHT_SHOULDER]:
                lm_coord = (int(landmarks[landmark.value].x * frame.shape[1]), int(landmarks[landmark.value].y * frame.shape[0]))
                cv2.circle(image, lm_coord, 5, (0, 255, 0), -1)
            
            # Connect landmarks with green lines
            cv2.line(image, (int(shoulder[0] * frame.shape[1]), int(shoulder[1] * frame.shape[0])), 
                     (int(nose[0] * frame.shape[1]), int(nose[1] * frame.shape[0])), (0, 255, 0), 2)
            cv2.line(image, (int(nose[0] * frame.shape[1]), int(nose[1] * frame.shape[0])), 
                     (int(wrist[0] * frame.shape[1]), int(wrist[1] * frame.shape[0])), (0, 255, 0), 2)
            # Connect landmarks of the two shoulders with green line
            cv2.line(image, (int(shoulder[0] * frame.shape[1]), int(shoulder[1] * frame.shape[0])),
                    (int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * frame.shape[1]),
                    int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * frame.shape[0])),
                    (0, 255, 0), 2)

            # Record angle when perfect posture is indicated or re-record on 'P' press
            if perfect_posture is None:
                cv2.putText(image, 'Assume perfect posture', (15, 12), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, 'Press "P" when ready', (10, 60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                # Check for key press to indicate readiness for perfect posture
                key = cv2.waitKey(1) & 0xFF  # Check for the 'q' key immediately
                if key == ord('p'):
                    perfect_posture = angle
                    bad_posture_timer = None  # Reset bad posture timer when perfect posture is set
                    good_posture_start_time = None  # Reset good posture timer when perfect posture is set
                    played = False  # Reset the played flag when reselecting the perfect angle

            else:
                if angle > (perfect_posture + deviation_angle_threshold):
                    counter = "Bad"
                    if bad_posture_timer is None:
                        bad_posture_timer = time.time()  # Start the timer for bad posture
                        good_posture_start_time = None  # Reset good posture timer
                        played = False  # Reset the played flag when entering the bad posture state
                    else:
                        bad_posture_duration = time.time() - bad_posture_timer
                        if bad_posture_duration >= time_threshold:  # Check if bad posture is maintained for the specified time
                            bad_posture_alert = True
                            good_posture_start_time = None  # Reset good posture timer when bad posture is detected
                            if not played:  # Play the sound only if it hasn't been played before
                                sound.play()
                                played = True  # Set the flag to True after playing the sound
                else:
                    counter = "Good"
                    if good_posture_start_time is None:
                        good_posture_start_time = time.time()  # Start the timer for good posture
                        bad_posture_timer = None  # Reset bad posture timer when good posture is attained
                        if bad_posture_alert:
                            # Reset the played flag when transitioning from bad to good posture
                            played = False
                    else:
                        good_posture_duration = time.time() - good_posture_start_time
                        if good_posture_duration >= 2.0:  # Check if good posture is maintained for 3 seconds
                            bad_posture_alert = False  # Clear bad posture alert
                            played = False  # Reset played flag when entering good posture state
                cv2.putText(image, 'Posture', (15, 12), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, str(counter), 
                            (10, 60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

                if bad_posture_alert:
                    cv2.putText(image, 'Bad Posture Alert!', (150, 240), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        except:
            pass
        
        # Display perfect posture angle in the top right corner
        display_perfect_posture_angle(image, perfect_posture, deviation_angle_threshold, time_threshold)
        
        cv2.imshow('PosturePro', image)

        key = cv2.waitKey(10)

        if cv2.getWindowProperty('PosturePro', cv2.WND_PROP_VISIBLE) < 1:
            break

        # Toggle video pause on 'Esc' key press
        if key == 27:  # 'Esc' key
            video_paused = not video_paused

        # Update angle and time thresholds on key press
        if key == ord('i'):
            deviation_angle_threshold = max(0, deviation_angle_threshold - 1)
        elif key == ord('o'):
            deviation_angle_threshold += 1
        elif key == ord('k'):
            time_threshold = max(0, time_threshold - 1)
        elif key == ord('l'):
            time_threshold += 1

        # Reset perfect posture on 'P' press
        if key == ord('p'):
            if bad_posture_alert:
                # If in bad posture state, reset to good posture state and re-record perfect posture
                perfect_posture = None
                bad_posture_alert = False
            else:
                perfect_posture = None

        # Exit when 'q' is pressed
        if key == ord('q'):
            break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

# Print the recorded angle after exiting the loop
if perfect_posture is not None:
    print(f"Perfect Posture Angle: {max(0, perfect_posture)}")
