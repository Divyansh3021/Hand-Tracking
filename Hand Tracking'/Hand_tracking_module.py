import cv2
import mediapipe as mp
import time
import pyautogui
import math


class handDetector():
    def __init__(self, mode = False, max_hands = 4, detection_confidence = 0.5, track_confidence = 0.5):
        # self.thumb_cx = 0
        # self.thumb_cy = 0
        # self.index_cx = 0
        # self.index_cy = 0
        # self.prev_dist = 0
        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.track_confidence = track_confidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.max_hands,1 , self.detection_confidence, self.track_confidence)
        self.mpdraw = mp.solutions.drawing_utils


    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
 
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    # def distance(self, ax,ay,bx,by):
    #     self.square = ((ax-bx)**2) + ((ay-by)**2)
    #     self.Distance = math.sqrt(self.square)
    #     # print("Square is:", square)
    #     return int(self.Distance)
    # def volume_control(self, prev_dist, dist):
    #     if (dist - prev_dist) > 25:
    #         print("Distance increased")
    #         # for i in range((prev_dist - dist)*5):
    #         pyautogui.press("volumeup")
    #         # time.sleep(0.1)
    #     elif (prev_dist - dist) > 25:
    #         print("Distance decreased")
    #         # for i in range((prev_dist - dist)*5):
    #         pyautogui.press("volumedown")
    #         # time.sleep(0.1)

    def findPositions(self, img, handNo = 0, draw = True):

        lmList = []
        if self.results.multi_hand_landmarks:

            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                # if id == 4:
                    # cv2.circle(img, (cx, cy), 8, (255, 0, 100), cv2.FILLED)
                    # self.thumb_cx = cx
                    # self.thumb_cy = cy
                # if id == 8:
                    # cv2.circle(img, (cx, cy), 8, (100, 0, 100), cv2.FILLED)
                    # self.index_cx = cx
                    # self.index_cy = cy

                # self.dist = self.distance(self.thumb_cx, self.thumb_cy, self.index_cx, self.index_cy)
                # self.volume_control(self.prev_dist, self.dist)
                # if draw:
                    # cv2.circle(img, (cx, cy), 7, (255, 0, 10), cv2.FILLED)
        return lmList

    

def main():
    
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPositions(img)
        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1/(cTime- pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

        cv2.imshow("image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()