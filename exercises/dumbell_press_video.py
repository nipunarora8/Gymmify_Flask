import cv2
import mediapipe as mp
import numpy as np
import os
from .angle_calculation import angle_cal

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def left(landmarks):
    
    # Get coordinates_
    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

    shoulder_angle = angle_cal(hip, shoulder, elbow)
    elbow_angle = angle_cal(shoulder, elbow, wrist)
        
    return [[shoulder,shoulder_angle],[elbow,elbow_angle]]
#     return shoulder_angle, elbow_angle

def right(landmarks):
    
    # Get coordinates_
    shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
    wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
    hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

    shoulder_angle = angle_cal(hip, shoulder, elbow)
    elbow_angle = angle_cal(shoulder, elbow, wrist)
        
    return [[shoulder,shoulder_angle],[elbow,elbow_angle]]
#     return shoulder_angle, elbow_angle

def visualize(arr,frame):
    for i in arr:
        cv2.putText(frame[0], str(i[1]), 
                           tuple(np.multiply(i[0], [frame[1],frame[2]]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (20,255,57), 2, cv2.LINE_AA)
    
def dumbell_press(file_path):

    cap = cv2.VideoCapture(file_path)
    
    vid_name=file_path.split('/')[-1]
    vid_name = '/uploads/'+ vid_name[:-3] + '_out.mp4'

    frame_height = int(cap.get(4))
    frame_width = int(cap.get(3))
    fps = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter(vid_name,cv2.VideoWriter_fourcc('h', '2', '6', '4'), fps, (frame_width,frame_height))

    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()

            if ret == True:
                # Make detection
                results = pose.process(frame)
                
                # Extract landmarks
                try:
                    landmarks = results.pose_landmarks.landmark
                    
                    visualize(left(landmarks),[frame,frame_width,frame_height])
                    visualize(right(landmarks),[frame,frame_width,frame_height])
                    
                except:
                    pass
                
                # Render detections
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(41,255,249), thickness=1, circle_radius=3), 
                                        mp_drawing.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=2) 
                                        ) 
                out.write(frame)
            else:
                pass
    cap.release()
    out.release()
    print("video saved at",vid_name)
    print(os.listdir('uploads'))
    return vid_name             

