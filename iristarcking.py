import cv2
import mediapipe as mp
import numpy as np

#  Initialize MediaPipe
mp_face_mesh = mp.solutions.face_mesh
cap = cv2.VideoCapture(0)

with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True, 
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as face_mesh:

    while cap.isOpened():
        success, frame = cap.read()
        if not success: break

        frame = cv2.flip(frame, 1) 
        img_h, img_w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            mesh_points = results.multi_face_landmarks[0].landmark
            
            #  EXTRACT POINTS (Left Eye) 
            p_iris = np.array([mesh_points[468].x * img_w, mesh_points[468].y * img_h])
            p_left = np.array([mesh_points[33].x * img_w, mesh_points[33].y * img_h])
            p_right = np.array([mesh_points[133].x * img_w, mesh_points[133].y * img_h])
            p_top = np.array([mesh_points[159].x * img_w, mesh_points[159].y * img_h])
            p_bot = np.array([mesh_points[145].x * img_w, mesh_points[145].y * img_h])

            #  GAZE RATIO MATH 
            # Horizontal: 0 = Right, 1 = Left
            eye_width = np.linalg.norm(p_left - p_right)
            h_ratio = np.linalg.norm(p_iris - p_right) / eye_width

            # Vertical: 0 = Up, 1 = Down
            eye_height = np.linalg.norm(p_bot - p_top)
            v_ratio = np.linalg.norm(p_iris - p_top) / eye_height

            # FIXED DIRECTION LOGIC 
            command = "STOP"
            
            if h_ratio < 0.42: 
                command = "ROBOT: RIGHT"
            elif h_ratio > 0.58:
                command = "ROBOT: LEFT"
            # Logic Swapped: Lower ratio means closer to the top lid (UP)
            elif v_ratio < 0.48: 
                command = "ROBOT: UP"
            elif v_ratio > 0.65: 
                command = "ROBOT: DOWN"

            # Visual Feedback
            cv2.putText(frame, f"{command}", (30, 80), cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 255, 0), 2)
            cv2.circle(frame, tuple(p_iris.astype(int)), 3, (255, 0, 255), -1)

        cv2.imshow('Eye Robot Brain', frame)
        if cv2.waitKey(1) & 0xFF == 27: break

cap.release()
cv2.destroyAllWindows()