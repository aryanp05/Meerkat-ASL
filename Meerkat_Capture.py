import os
import shutil

import cv2




# Ensures there is a directory to store all image data
RAW_IMG_DATA = './RAW_IMGS'
if not os.path.exists(RAW_IMG_DATA):
    os.makedirs(RAW_IMG_DATA)

# Sets the number of images captured per training round
captureset_size = 100

current_symbol = ''

# Sets VideoCapture (using camera 0 // may need to adjust based on device)
cap = cv2.VideoCapture(0)


# Captures and stores data
while True:
    to_exit = False
    done = False

    # Collects which word that data will be for
    while True:
        ret, frame = cap.read()
        cv2.putText(frame, 'Current Word: {}'.format(current_symbol), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 255), 3, cv2.LINE_AA)
        cv2.imshow('window', frame)
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
        elif not current_key == -1:
            current_symbol += (chr(current_key))
            
    # exits the program if the user wants to
    if to_exit:
        break
    counter = 0
    while counter < captureset_size:
        ret, frame = cap.read()
        cv2.imshow('window', frame)
        flipped_frame = cv2.flip(frame, 1)
        cv2.waitKey(25)
        if not os.path.exists(os.path.join(RAW_IMG_DATA, current_symbol)):
            os.makedirs(os.path.join(RAW_IMG_DATA, current_symbol))
        cv2.imwrite(os.path.join(RAW_IMG_DATA, current_symbol, '{}.jpg'.format(counter)), frame)
        cv2.imwrite(os.path.join(RAW_IMG_DATA, current_symbol, '{}_rvs.jpg'.format(counter)), flipped_frame)
        counter += 1
        if current_key == ord('/'):
            to_exit = True
            break
    while True:
         ret, frame = cap.read()
         cv2.putText(frame, 'Save Data (Y/N)', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 255), 3, cv2.LINE_AA)
         cv2.imshow('window', frame)
         current_key = cv2.waitKey(25)
        
         if current_key == ord('Y') or current_key == ord('y'):
              current_symbol = ''
              break
         elif current_key == ord('N') or current_key == ord('n'):
              shutil.rmtree(os.path.join(RAW_IMG_DATA, current_symbol))
              current_symbol = ''
              break

       
cap.release()
cv2.destroyAllWindows


