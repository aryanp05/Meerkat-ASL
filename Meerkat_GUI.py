import cv2
import numpy as np

cap = cv2.VideoCapture(1)

ret, frame = cap.read()
H, W, _ = frame.shape

def point_inside_rect(x, y, rect):
    x1, y1, w, h = rect
    return x1 <= x <= x1 + w and y1 <= y <= y1 + h

def mouse_callback(event, x, y, flags, param):
    global box1_hover, box2_hover
    global gradient_frame, image
    global instruction_show
    global H, W

    if point_inside_rect(x, y, (box_x1, box_y, box_width, box_height)):
        box1_hover = True
        if event == cv2.EVENT_LBUTTONDOWN:
            from Meerkat_Main import ASL_mode
    else:
        box1_hover = False

    if point_inside_rect(x, y, (box_x2, box_y, box_width, box_height)):
        box2_hover = True
        if event == cv2.EVENT_LBUTTONDOWN:
            instruction_show = True

    else:
        box2_hover = False


gradient_frame = np.zeros((H, W, 3), dtype=np.uint8)
colour_1 = (210, 170, 109)
colour_2 = (255, 215, 0)


for y in range(H):
    for x in range(W):
        factor = (x/W * y/H)

        red = abs(int(colour_1[0] - abs(int(colour_1[0] - colour_2[0]) * factor)))
        green = abs(int(colour_1[1] - abs(int(colour_1[1] - colour_2[1]) * factor)))
        blue = abs(int(colour_1[2] - abs(int(colour_1[2] - colour_2[2]) * factor)))

 
        gradient_frame[y, x] = (blue, green, red)

font_size = 5
text_size = cv2.getTextSize("Meerkat ASL", cv2.FONT_HERSHEY_TRIPLEX, font_size, 2)[0]
text_x = (W - text_size[0]) // 2
text_y = (H - text_size[1]) // 2
cv2.putText(gradient_frame, "Meerkat ASL", (text_x, text_y), cv2.FONT_HERSHEY_TRIPLEX, font_size, (255,255,255), 2)

box_width = 500
box_height = 200
box_space = 50
box_x1 = (W - 2 * box_width - box_space) // 2
box_x2 = box_x1 + box_width + box_space
box_y = text_y + text_size[1] + 50
cv2.rectangle(gradient_frame, (box_x1, box_y), (box_x1 + box_width, box_y + box_height),(255,255,255), -1)
text1 = "Start"
text_size1 = cv2.getTextSize(text1, cv2.FONT_HERSHEY_TRIPLEX, 2, 2)[0]
text_x1 = box_x1 + (box_width - text_size1[0]) // 2
text_y1 = box_y + (box_height + text_size1[1]) // 2
cv2.putText(gradient_frame, text1, (text_x1, text_y1), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 0, 0), 2)
cv2.rectangle(gradient_frame, (box_x2, box_y), (box_x2 + box_width, box_y + box_height),(255,255,255), -1)
text2 = "Keybinds"
text_size2 = cv2.getTextSize(text2, cv2.FONT_HERSHEY_TRIPLEX, 2, 3)[0]
text_x2 = box_x2 + (box_width - text_size2[0]) // 2
text_y2 = box_y + (box_height + text_size2[1]) // 2
cv2.putText(gradient_frame, text2, (text_x2, text_y2), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 0, 0), 2)

# Create instructions overlay
instructions = gradient_frame.copy()
inst_width, inst_height = int(W - W / 3), int(H - H/8)
inst_x = (W - inst_width) // 2
inst_y = (H - inst_height) // 2
cv2.rectangle(instructions, (inst_x, inst_y), (inst_x + inst_width, inst_y + inst_height), (255, 255, 255), -1)

lines_of_text = [
    "Main ASL Mode Key Binds",
    "Press ';' to enter Testing Mode"  ,
    "Press '.' to enter Capture Mode",
    "Press '/' to return to the main screen",
    "Press '[' to change light/dark mode",
    "",
    "Capture Mode Key Binds",
    "Type the word you would like to capture for",
    "Press backspace to delete letters",
    "Press enter to begin capturing",
    "Press ';' to retrain AI with new adjustments",
    "Press '/' to return to ASL mode",
    "",
    "Testing Mode Key Binds",
    "Type the word you would like to capture for",
    "Press backspace to delete letters",
    "Press enter to capture a small adjustment",
    "Press ']' to capture a large adjustment",
    "Press ';' to retrain AI with new adjustments",
    "Press '[' to change light/dark mode"
    "",
    "Press '/' to return to main screen",
    "Press '/' in the main screen to quit"
]

inst_font = cv2.FONT_HERSHEY_SIMPLEX
inst_font_scale = 1
inst_font_thickness = 2
inst_line_height = 40
initial_y = inst_y + 30

for i, text in enumerate(lines_of_text):
    inst_text_size = cv2.getTextSize(text, inst_font, inst_font_scale, inst_font_thickness)[0]
    inst_text_x = inst_x + (inst_width - inst_text_size[0]) // 2
    inst_text_y = initial_y + i * inst_line_height
    cv2.putText(instructions, text, (inst_text_x, inst_text_y), inst_font, inst_font_scale, (0, 0, 0), inst_font_thickness)

box1_hover = False
box2_hover = False
instruction_show = False

while True:
    frame_copy = gradient_frame.copy()
    if instruction_show:
        cv2.imshow('frame', instructions)
        if cv2.waitKey(25) == ord('/'):
            instruction_show = False
    else: 
        if box1_hover:
            cv2.rectangle(frame_copy, (box_x1, box_y), (box_x1 + box_width, box_y + box_height),(255,215,0), -1)
        else:
            cv2.rectangle(frame_copy, (box_x1, box_y), (box_x1 + box_width, box_y + box_height),(255,255,255), -1)
        if box2_hover:
            cv2.rectangle(frame_copy, (box_x2, box_y), (box_x2 + box_width, box_y + box_height),(255,215,0), -1)
        else:
            cv2.rectangle(frame_copy, (box_x2, box_y), (box_x2 + box_width, box_y + box_height),(255,255,255), -1)
        cv2.putText(frame_copy, text1, (text_x1, text_y1), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 0, 0), 2)
        cv2.putText(frame_copy, text2, (text_x2, text_y2), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 0, 0), 2)

        cv2.imshow('frame', frame_copy)
        if cv2.waitKey(25) == ord('/'):
            break
    cv2.setMouseCallback('frame', mouse_callback)

cv2.destroyAllWindows()