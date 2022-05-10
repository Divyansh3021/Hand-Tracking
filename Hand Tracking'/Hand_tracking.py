import cv2
import mediapipe as mp
import time
import math
import pyautogui

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpdraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0


def distance(ax,ay,bx,by):
    square = ((ax-bx)**2) + ((ay-by)**2)
    Distance = math.sqrt(square)
    # print("Square is:", square)
    return int(Distance)

while True:
    thumb_cx = 0
    thumb_cy = 0
    index_cx = 0
    index_cy = 0
    prev_dist = 0
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                # print(id, cx, cy)


                if id == 4:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 100), cv2.FILLED)
                    thumb_cx = cx
                    thumb_cy = cy
                if id == 8:
                    cv2.circle(img, (cx, cy), 15, (100, 0, 100), cv2.FILLED)
                    index_cx = cx
                    index_cy = cy
                # print("thumb coordinates = ( "+str(thumb_cx)+","+str(thumb_cy)+")")
                # print("index coordinates = ( "+str(index_cx)+","+str(index_cy)+")")
                # square = ((thumb_cx-index_cx)**2) + ((index_cy-thumb_cy)**2)
                # Distance = sqrt(square)
                # print("Square is:", square)
                # # print("Distance is: ",Distance)
                dist = distance(thumb_cx, thumb_cy, index_cx, index_cy)
                print(" dist is ",dist)
                print("prev dist is ",prev_dist)

                if (dist - prev_dist) > 25:
                    print("Distance increased")
                    # for i in range((prev_dist - dist)*5):
                    pyautogui.press("volumeup")
                    # time.sleep(0.1)
                elif (prev_dist - dist) > 25:
                    print("Distance decreased")
                    # for i in range((prev_dist - dist)*5):
                    pyautogui.press("volumedown")
                    # time.sleep(0.1)
                    
                prev_dist = dist
            mpdraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    time.sleep(0.1)

    cTime = time.time()
    fps = 1/(cTime- pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

    cv2.imshow("image", img)
    cv2.waitKey(1)