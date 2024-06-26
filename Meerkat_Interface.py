import pickle
import subprocess

import cv2
import mediapipe as mp
import numpy as np


model_dict = pickle.load(open('./model.pickle', 'rb'))
model = model_dict['model']

cap = cv2.VideoCapture(1)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

while True:

    data_aux = []
    x_ = []
    y_ = []

    ret, frame = cap.read()

    H, W, _ = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,  # image to draw
                hand_landmarks,  # model output
                mp_hands.HAND_CONNECTIONS,  # hand connections
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x)
                data_aux.append(y)
        if len(data_aux) != 42:
            continue
        x1 = int(min(x_) * W) - 10
        y1 = int(min(y_) * H) - 10

        x2 = int(max(x_) * W) - 10
        y2 = int(max(y_) * H) - 10

        prediction = str(model.predict([np.asarray(data_aux)]))

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
        cv2.putText(frame, prediction, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 0, 0), 3,
                    cv2.LINE_AA)

    cv2.imshow('frame', frame)
    pressed_key = cv2.waitKey(25)
    if pressed_key == ord('/'):
        break
    elif pressed_key == ord(';'):
        cv2.putText(frame, 'Switching to Testing Mode', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 0, 0), 3, cv2.LINE_AA)
        cv2.imshow('frame', frame)
        cv2.waitKey(25)
        subprocess.call(['python', 'Meerkat_Test'])
        model_dict = pickle.load(open('./model.pickle', 'rb'))
        model = model_dict['model']

    elif pressed_key == ord('.'):
        cv2.putText(frame, 'Switching to Capture Data Mode', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 0, 0), 3, cv2.LINE_AA)
        cv2.imshow('frame', frame)
        cv2.waitKey(25)
        subprocess.call(['python', 'Meerkat_Capture'])

    
print('hello')
cap.release()
cv2.destroyAllWindows()