# virtual_full_keyboard_mouse_fixed.py
# Tested logic structure — requires Python 3.10, opencv-python, mediapipe, pyautogui, numpy

import cv2
import mediapipe as mp
import pyautogui
import math
import time
import numpy as np

# ---------- SETTINGS ----------
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

CAM_WIDTH = 1280
CAM_HEIGHT = 720

KEY_ROWS = [
    ["Q","W","E","R","T","Y","U","I","O","P"],
    ["A","S","D","F","G","H","J","K","L"],
    ["Z","X","C","V","B","N","M"],
    ["SPACE","ENTER","BACK"]
]

KEY_SIZE = 70
KEY_SPACING = 10
KEYBOARD_X = 40
KEYBOARD_Y = 40

PINCH_THRESHOLD = 0.04
RIGHTCLICK_THRESHOLD = 0.05
SMOOTHING = 5
SCROLL_SENSITIVITY = 300

# ---------- INIT ----------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(3, CAM_WIDTH)
cap.set(4, CAM_HEIGHT)

last_key_time = {}
last_key_sent = ""
mode = "KEYBOARD"
caps_on = False
mouse_buffer_x = []
mouse_buffer_y = []
dragging = False

# ---------- HELPERS ----------
def draw_keyboard_overlay(img):
    """Draw keyboard and return dict key -> (x1,y1,x2,y2)"""
    key_pos = {}
    y_off = KEYBOARD_Y
    for r, row in enumerate(KEY_ROWS):
        x_off = KEYBOARD_X
        for k in row:
            x1 = x_off
            y1 = y_off + r * (KEY_SIZE + KEY_SPACING)
            x2 = x1 + KEY_SIZE
            y2 = y1 + KEY_SIZE

            # draw rect and text
            cv2.rectangle(img, (x1,y1), (x2,y2), (200,200,200), 2)
            if k in ["SPACE","ENTER","BACK"]:
                txt = k
                scale = 0.6
                tx = x1 + 8
                ty = y1 + int(KEY_SIZE/2) + 8
            else:
                txt = k
                scale = 1
                tx = x1 + 18
                ty = y1 + int(KEY_SIZE/2) + 8

            cv2.putText(img, txt, (tx, ty),
                        cv2.FONT_HERSHEY_SIMPLEX, scale, (230,230,230), 2)
            key_pos[k] = (x1,y1,x2,y2)
            x_off += KEY_SIZE + KEY_SPACING
    return key_pos

def is_point_in_rect(px,py,rect):
    x1,y1,x2,y2 = rect
    return x1 < px < x2 and y1 < py < y2

def normalized_dist(a,b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

print("Screen:", SCREEN_WIDTH, SCREEN_HEIGHT)
print("Jalankan script. Tekan ESC untuk keluar. Tekan 'c' untuk toggle CAPS.")

# ---------- MAIN LOOP ----------
while True:
    success, frame = cap.read()
    if not success:
        print("Tidak bisa membuka kamera")
        break

    frame = cv2.flip(frame, 1)
    img_h, img_w = frame.shape[:2]
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    key_positions = draw_keyboard_overlay(frame)

    cv2.putText(frame, f"Mode: {mode}", (10, img_h - 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,255), 2)
    cv2.putText(frame, f"Caps: {'ON' if caps_on else 'OFF'}", (10, img_h - 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,200,0), 2)

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        # normalized landmarks
        lm_thumb = (hand.landmark[4].x, hand.landmark[4].y)
        lm_index = (hand.landmark[8].x, hand.landmark[8].y)
        lm_middle = (hand.landmark[12].x, hand.landmark[12].y)

        # count extended fingers (index, middle, ring, pinky)
        fingers_extended = 0
        tips = [8,12,16,20]
        for tip in tips:
            tip_y = hand.landmark[tip].y
            pip_y = hand.landmark[tip-2].y
            if tip_y < pip_y - 0.015:
                fingers_extended += 1

        # mode switch
        if fingers_extended >= 4:
            mode = "KEYBOARD"
        elif fingers_extended <= 1:
            mode = "MOUSE"

        # pixel coords of index tip
        index_x = int(lm_index[0] * img_w)
        index_y = int(lm_index[1] * img_h)
        cv2.circle(frame, (index_x, index_y), 8, (0,255,0), cv2.FILLED)

        pinch_dist = normalized_dist(lm_thumb, lm_index)

        # KEYBOARD MODE
        if mode == "KEYBOARD":
            for k, rect in key_positions.items():
                if is_point_in_rect(index_x, index_y, rect):
                    x1,y1,x2,y2 = rect
                    cv2.rectangle(frame, (x1,y1), (x2,y2), (0,200,0), -1)
                    cv2.putText(frame, k, (x1+18, y1 + int(KEY_SIZE/2)+8),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)

                    now = time.time()
                    last = last_key_time.get(k, 0)
                    # debounce per-key
                    if (now - last) > 0.45:
                        # optional: require pinch to confirm (commented to allow hover press)
                        # if pinch_dist < PINCH_THRESHOLD:
                        if k == "SPACE":
                            pyautogui.press("space")
                        elif k == "ENTER":
                            pyautogui.press("enter")
                        elif k == "BACK":
                            pyautogui.press("backspace")
                        else:
                            ch = k.lower() if not caps_on else k.upper()
                            pyautogui.press(ch.lower())
                        last_key_time[k] = now
                        last_key_sent = k

        # MOUSE MODE
        else:
            # map index to screen coords
            screen_x = np.interp(lm_index[0], [0,1], [0, SCREEN_WIDTH])
            screen_y = np.interp(lm_index[1], [0,1], [0, SCREEN_HEIGHT])

            mouse_buffer_x.append(screen_x)
            mouse_buffer_y.append(screen_y)
            if len(mouse_buffer_x) > SMOOTHING:
                mouse_buffer_x.pop(0)
                mouse_buffer_y.pop(0)
            smooth_x = int(sum(mouse_buffer_x)/len(mouse_buffer_x))
            smooth_y = int(sum(mouse_buffer_y)/len(mouse_buffer_y))

            try:
                pyautogui.moveTo(smooth_x, smooth_y, duration=0.01)
            except Exception:
                pass

            cv2.circle(frame, (index_x, index_y), 12, (255,0,0), 3)

            # drag with pinch
            if pinch_dist < PINCH_THRESHOLD:
                if not dragging:
                    pyautogui.mouseDown()
                    dragging = True
            else:
                if dragging:
                    pyautogui.mouseUp()
                    dragging = False

            # right click with index+middle close
            idx_mid_dist = normalized_dist(lm_index, lm_middle)
            if idx_mid_dist < RIGHTCLICK_THRESHOLD:
                pyautogui.click(button='right')
                time.sleep(0.3)

            # simple scroll: middle above index -> scroll up, middle below -> scroll down
            if lm_middle[1] < lm_index[1] - 0.08:
                pyautogui.scroll(int(SCROLL_SENSITIVITY))
            elif lm_middle[1] > lm_index[1] + 0.08:
                pyautogui.scroll(int(-SCROLL_SENSITIVITY))

    # UI info
    cv2.putText(frame, f"LastSend: {last_key_sent}", (300, img_h - 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200,200,255), 2)

    cv2.imshow("Virtual Touch Keyboard & Mouse (fixed)", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC
        break
    if key == ord('c'):
        caps_on = not caps_on

cap.release()
cv2.destroyAllWindows()