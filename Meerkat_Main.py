import os
import subprocess
import shutil
import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import pickle

# Ensures there is a directory to store all image data
RAW_IMG_DATA = './RAW_IMGS'
if not os.path.exists(RAW_IMG_DATA):
    os.makedirs(RAW_IMG_DATA)

# Set data sizes
captureset_size = 250
small_capture_size = 15
large_capture_size = 50

mode = 0

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

def capture_mode():
    global cap
    global model
    global label_encoder
    current_symbol = ''

    while True:
        to_exit = False

        # Collects which word that data will be for
        while True:
            ret, frame = cap.read()
            H, W, _ = frame.shape
            cv2.putText(frame, '(CAPTURE MODE) Current Word: {}'.format(current_symbol), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 255), 3, cv2.LINE_AA)
            cv2.imshow('frame', frame)
            current_key = cv2.waitKey(25)
            if current_key == ord('/'):
                to_exit = True
                break
            elif current_key == 127:
                current_symbol = current_symbol[:-1]
            elif current_key == 13 and not current_symbol == '':
                current_symbol = current_symbol.strip()
                current_symbol = current_symbol.replace(" ", "_")
                break
            elif current_key == ord(';'):
                ret, frame = cap.read()
                black_image = np.zeros((H, W, 3), dtype=np.uint8)
                cv2.putText(black_image, 'Processing, please wait', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 255), 3, cv2.LINE_AA)
                cv2.imshow('frame', black_image)
                cv2.waitKey(1)
                # Call the training script
                subprocess.call(['python', 'Meerkat_Process.py'])
                subprocess.call(['python', 'Meerkat_Train.py'])
                model = tf.keras.models.load_model('model.h5')
                with open('label_encoder.pkl', 'rb') as f:
                    label_encoder = pickle.load(f)
            elif not current_key == -1:
                current_symbol += (chr(current_key))

        # Exits the program if the user wants to
        if to_exit:
            break
        counter = 0
        while counter < captureset_size:
            ret, frame = cap.read()
            cv2.imshow('frame', frame)
            cv2.waitKey(25)
            if not os.path.exists(os.path.join(RAW_IMG_DATA, current_symbol)):
                os.makedirs(os.path.join(RAW_IMG_DATA, current_symbol))
            cv2.imwrite(os.path.join(RAW_IMG_DATA, current_symbol, '{}.jpg'.format(counter)), frame)
            counter += 1
            if current_key == ord('/'):
                to_exit = True
                break
        while True:
            ret, frame = cap.read()
            cv2.putText(frame, 'Save Data (Y/N)', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 255), 3, cv2.LINE_AA)
            cv2.imshow('frame', frame)
            current_key = cv2.waitKey(25)

            if current_key == ord('Y') or current_key == ord('y'):
                current_symbol = ''
                break
            elif current_key == ord('N') or current_key == ord('n'):
                shutil.rmtree(os.path.join(RAW_IMG_DATA, current_symbol))
                current_symbol = ''
                break

def testing_mode():
    global cap
    global model
    global label_encoder
    global mode
    current_symbol = ''
    model = tf.keras.models.load_model('model.h5')
    with open('label_encoder.pkl', 'rb') as f:
        label_encoder = pickle.load(f)
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
                    frame,  # Image to draw
                    hand_landmarks,  # Model output
                    mp_hands.HAND_CONNECTIONS,  # Hand connections
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

            prediction = model.predict(np.asarray([data_aux]))
            prediction_class = np.argmax(prediction)
            prediction_symbol = label_encoder.inverse_transform([prediction_class])[0]

            cv2.rectangle(frame, (x1, y1), (x2, y2), (mode, mode, mode), 4)
            cv2.putText(frame, str(prediction_symbol), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (mode, mode, mode), 3,
                        cv2.LINE_AA)

        cv2.putText(frame, 'TESTING, TO CORRECT FOR: {}'.format(current_symbol), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 255), 3, cv2.LINE_AA)
        cv2.imshow('frame', frame)
        pressed_key = cv2.waitKey(25)
        if pressed_key == ord('/'):
            break
        elif pressed_key == 127:
            current_symbol = current_symbol[:-1]
        elif pressed_key == 13:
            if current_symbol == '':
                continue
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
            if current_symbol == '':
                continue
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
            black_image = np.zeros((H, W, 3), dtype=np.uint8)
            cv2.putText(black_image, 'Processing, please wait', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 255), 3, cv2.LINE_AA)
            cv2.imshow('frame', black_image)
            cv2.waitKey(1)
            # Call the training script
            subprocess.call(['python', 'Meerkat_Process.py'])
            subprocess.call(['python', 'Meerkat_Train.py'])
            model = tf.keras.models.load_model('model.h5')
            with open('label_encoder.pkl', 'rb') as f:
                label_encoder = pickle.load(f)
        elif pressed_key == ord('['):
            if mode == 0:
                mode = 255
            else:
                mode = 0
        elif not pressed_key == -1:
            current_symbol += (chr(pressed_key))

def ASL_mode():
    global cap
    global model
    global label_encoder
    while True:
        global mode
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
                    frame,  # Image to draw
                    hand_landmarks,  # Model output
                    mp_hands.HAND_CONNECTIONS,  # Hand connections
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

            prediction = model.predict(np.asarray([data_aux]))
            prediction_class = np.argmax(prediction)
            prediction_symbol = label_encoder.inverse_transform([prediction_class])[0]

            cv2.rectangle(frame, (x1, y1), (x2, y2), (mode, mode, mode), 4)
            cv2.putText(frame, str(prediction_symbol), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (mode, mode, mode), 3,
                        cv2.LINE_AA)

        cv2.imshow('frame', frame)
        pressed_key = cv2.waitKey(25)
        if pressed_key == ord('/'):
            break
        elif pressed_key == ord(';'):
            testing_mode()
            model = tf.keras.models.load_model('model.h5')
            with open('label_encoder.pkl', 'rb') as f:
                label_encoder = pickle.load(f)
        elif pressed_key == ord('.'):
            capture_mode()
        elif pressed_key == ord('['):
            if mode == 0:
                mode = 255
            else:
                mode = 0

# Load model and label encoder
if not os.path.exists("./model.h5"):
    capture_mode()
model = tf.keras.models.load_model('model.h5')
with open('label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

ASL_mode()

cap.release()
cv2.destroyAllWindows()
