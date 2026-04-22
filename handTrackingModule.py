import cv2
import mediapipe as mp
import time

#########################################################################
#A class to detect hands and extract landmark positions using MediaPipe.
#########################################################################

class HandDetector:
    def __init__(self,mode=False,maxHands=2,detectionCon=0.7,trackCon=0.7 ):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        # create a module for the hand model map
        self.mpHands = mp.solutions.hands

        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):

        #visuals of the Hand
        #MediaPipe requires RGB, but OpenCV uses BGR
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)


        #When hand is detected it results in the landmarks being triggered and a visual indication is drawn
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    #draw hand landmarks that are detected with connection lines
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    #finds pixel coordinates of landmarks for a specific hand and either if its left or right hand.
    def findPosition(self,img,handNo=0, draw = True, zAxis = False, color = (255, 0, 0)):
        lmList = []
        handType = None

        if self.results.multi_hand_landmarks:
            handType = self.results.multi_handedness[handNo].classification[0].label
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                #converts normalised coordinated to pixel coordinates
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

             # find the ID located landmarks positions
                if zAxis:
                    cz = round(lm.z, 3)
                    lmList.append([id, cx, cy, cz])
                else:
                    lmList.append([id, cx, cy])

                if draw:
                    cv2.circle(img, (cx,cy), 6, color, cv2.FILLED)

        return lmList, handType

def main() :
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = HandDetector()

    while True:
        success, img = cap.read()
        #flips the camera image horizontally - this is due to the fact that the image gets mirrored giving the perspective of the individual.
        #It gives a mirrored image.
        img = cv2.flip(img, 1)
        #detects hand
        img = detector.findHands(img)
        #Gets landmarks associated
        lmList, handType = detector.findPosition(img)


        if len(lmList) !=0:
            print(f"Hand: {handType}")

        # FPS Calculation
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if  __name__ == '__main__':
    main()