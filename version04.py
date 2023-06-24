import cv2
import mediapipe as mp
import pyautogui
import serial
import time
from google.protobuf.json_format import MessageToDict




mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


tipIds = [4, 8, 12, 16, 20]
state = None
Gesture = None
wCam, hCam = 720, 640

#
# ArduinoSerial = serial.Serial('com30',9600)
# time.sleep(3)
#

def fingerPosition(image, handNo=0):
    lmList = []
    if results.multi_hand_landmarks:
        myHand = results.multi_hand_landmarks[handNo]
        for id, lm in enumerate(myHand.landmark):

            h, w, c = image.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])
    return lmList
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)


with mp_hands.Hands(min_detection_confidence=0.8,min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
          for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        lmList = fingerPosition(image)
        if len(lmList) != 0:
            fingers = []
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:

                    fingers.append(1)
                if (lmList[tipIds[id]][2] > lmList[tipIds[id] - 2][2] ):

                    fingers.append(0)
            totalFingers = fingers.count(1)
            # print(totalFingers)


            if totalFingers == 4:
                # print(lmList[9][1])
                if lmList[9][1]<300:
                    for i in results.multi_handedness:


                        label = MessageToDict(i)['classification'][0]['label']

                        if label == 'Left':
                            print("1")
                            # ArduinoSerial.write(b'1')
                            # pyautogui.press('1')


                if lmList[9][1]>400:
                    for i in results.multi_handedness:

                        label = MessageToDict(i)['classification'][0]['label']

                        if label == 'Left':
                            print("0")
                            # ArduinoSerial.write(b'0')
                            # pyautogui.press('0')

            if totalFingers == 2:
                # print(lmList[9][2])
                if lmList[9][2] < 210:
                    print("Up")
                    # pyautogui.press('Up')
                if lmList[9][2] > 230:
                    print("Down")
                    # pyautogui.press('Down')

        cv2.imshow("Media Controller", image)
        key = cv2.waitKey(1) & 0xFF
        # если нажата клавиша `q`, то осуществляем выход из цикла
        if key == ord("q") or key == ord("Q"):
            break
    cv2.destroyAllWindows()