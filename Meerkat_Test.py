import pickle
import os
import subprocess

import cv2
import mediapipe as mp
import numpy as np

model_dict = pickle.load(open('./model.pickle', 'rb'))
model = model_dict['model']

small_capture_size = 15
large_capture_size = 50
current_symbol = ''
RAW_IMG_DATA = './RAW_IMGS'
if not os.path.exists(RAW_IMG_DATA):
    os.makedirs(RAW_IMG_DATA)

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
        cv2.putText(frame, prediction, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                    cv2.LINE_AA)

    cv2.putText(frame, 'TESTING, TO CORRECT FOR: {}'.format(current_symbol), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 255), 3, cv2.LINE_AA)
    cv2.imshow('frame', frame)
    pressed_key = cv2.waitKey(25)
    if pressed_key == ord('/'):
        break
    elif pressed_key == 127:
        current_symbol = current_symbol[:-1]
    elif pressed_key == 13:
        count = 0
        if not os.path.exists(os.path.join(RAW_IMG_DATA, current_symbol)):
            os.makedirs(os.path.join(RAW_IMG_DATA, current_symbol))
        filename = len(os.listdir(os.path.join(RAW_IMG_DATA, current_symbol)))
        while count <= small_capture_size:
            ret, frame = cap.read()
            cv2.imshow('frame', frame)
            cv2.waitKey(25)
            if not os.path.exists(os.path.join(RAW_IMG_DATA, current_symbol)):
                os.makedirs(os.path.join(RAW_IMG_DATA, current_symbol))
            cv2.imwrite(os.path.join(RAW_IMG_DATA, current_symbol, '{}.jpg'.format(filename)), frame)
            count += 1
            filename += 1
        current_symbol = ''
    elif pressed_key == ord(']'):
        count = 0
        if not os.path.exists(os.path.join(RAW_IMG_DATA, current_symbol)):
            os.makedirs(os.path.join(RAW_IMG_DATA, current_symbol))
        filename = len(os.listdir(os.path.join(RAW_IMG_DATA, current_symbol)))
        while count <= large_capture_size:
            ret, frame = cap.read()
            cv2.imshow('frame', frame)
            cv2.waitKey(25)
            if not os.path.exists(os.path.join(RAW_IMG_DATA, current_symbol)):
                os.makedirs(os.path.join(RAW_IMG_DATA, current_symbol))
            cv2.imwrite(os.path.join(RAW_IMG_DATA, current_symbol, '{}.jpg'.format(filename)), frame)
            count += 1
            filename += 1
    elif pressed_key == ord(';'):
        ret, frame = cap.read()
        cv2.putText(frame, 'Proccessing, please wait', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 255), 3, cv2.LINE_AA)
        cv2.imshow('frame', frame)
        subprocess.call(['python', 'Meerkat_Process'])
        subprocess.call(['python', 'Meerkat_Train'])
        model_dict = pickle.load(open('./model.pickle', 'rb'))
        model = model_dict['model']
    elif not pressed_key == -1:
            current_symbol += (chr(pressed_key))






cap.release()
cv2.destroyAllWindows()