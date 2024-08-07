import os
import shutil

import cv2
import mediapipe as mp
import pickle

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

RAW_IMG_DATA = './RAW_IMGS'
DATA_FILES = './DATA_FILES'
if not os.path.exists(DATA_FILES):
    os.makedirs(DATA_FILES)

for ASLsymbol in os.listdir(RAW_IMG_DATA):
    curr_data = []
    curr_symbols = []

    if ASLsymbol == '.DS_Store':
        continue
    for image_path in os.listdir(os.path.join(RAW_IMG_DATA, ASLsymbol)):
        processed_data = []
        img = cv2.imread(os.path.join(RAW_IMG_DATA, ASLsymbol, image_path))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        image_data = hands.process(img_rgb)

        if image_data.multi_hand_landmarks:
            for hand_landmarks in image_data.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    processed_data.append(x)
                    processed_data.append(y)
            curr_data.append(processed_data)
            curr_symbols.append(ASLsymbol)
    f = open(os.path.join(DATA_FILES, '{}.p'.format(ASLsymbol)), 'ab')
    pickle.dump({'data': curr_data, 'symbols': curr_symbols}, f)
    f.close()
    shutil.rmtree(os.path.join(RAW_IMG_DATA, ASLsymbol))

data = []
symbols = []

for data_files in os.listdir(DATA_FILES):
    if data_files == '.DS_Store':
        continue
    #print('{}'.format(data_files))
    dict = pickle.load(open(os.path.join(DATA_FILES, data_files), 'rb'))
    dict_data = dict['data']
    dict_symbols = dict['symbols']
    for i in range(len(dict_data)):
        if (len(dict_data[i]) != 42):
            continue
        data.append(dict_data[i])
        symbols.append(dict_symbols[i])
if os.path.exists('data_pickle'):        
    os.remove('data_pickle')
print(data)
print(symbols)
f = open('data_pickle', 'wb')
pickle.dump({'data': data, 'symbols': symbols}, f)
f.close()
