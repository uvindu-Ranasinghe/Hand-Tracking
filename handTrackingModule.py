import cv2   #import all the important libraries cv2 and mediapipe
import mediapipe as mp
import time

class handDetector():
    def __init__(self,mode=False,maxHands=2,detectionCon=0.5,trackCon=0.5 ):
        self.mode = mode #object created and its the variable of this object
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        # create a module for the hand model map
        self.mpHands = mp.solutions.hands  # why is this a formality?

        # create an object called Hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        # creates a module which calls a builtin function that helps us draw the hand landmarks
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):

        #sends an RGB image for the tracking
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #call the object hands and process it as an image this results in the overlay
        self.results = self.hands.process(imgRGB)

        #prints a results of the processing to show if a hand is detected or not
        #print(results.multi_hand_landmarks)

        #if a hand is detected
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    #draw hand landmarks that are detected with connections
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self,img,handNo=0, draw = True):
         # we get the landmark information - ID and Coordinates

        lmList = []
        handType = None

        if self.results.multi_hand_landmarks:

            handType = self.results.multi_handedness[handNo].classification[0].label

            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                        #we will print the ID and landmark info
                #print(id,lm)     ------------------------------------------------------------------------------
                        #we are gonna find the height, width and chanels of the image
                h, w, c = img.shape
                        #finding the cx and cy postion by multiplying the x and y values of the landmark
                cx, cy = int(lm.x * w), int(lm.y * h)

                        #find the ID located landmarks positions
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                        #isolate one finger and highlight it depending on its landmark ID
                #if id == 12:
                #print(handType)
                if draw:
                    cv2.circle(img, (cx,cy), 6, (207, 109, 85), cv2.FILLED)

        return lmList, handType

def main() :
    pTime = 0
    cTime = 0
    # helps capture the footage seen by the laptop camera
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    # captures the camera
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, handType = detector.findPosition(img)

        if len(lmList) !=0:
            print(lmList[4])

        # FPS Calculation
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        # display the frame rate on the camera as we detect the hands, it has a hershey plain font with a scale of 3,
        # blue colour and a thicknes of 3
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)  # what does this do?
        cv2.waitKey(1)


if  __name__ == '__main__':
    main()