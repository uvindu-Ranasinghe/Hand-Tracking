######### Hand Tracking Controlled Volume Changer ##########

### Imports the Modules/Libraries ######
#These are pre-written code that act as tools to utilize extra features#

import cv2           #library that allows me to use the Camera and draw graphics
import time          #Tool used to cal the FPS
import numpy as np   #Math helper library
import handTrackingModule as htm  #imports the hand tracking module I made as htm.
import math           #Pre-built math functions
from pycaw.pycaw import AudioUtilities  #Lets python control the volume - got this from GITHUB

#####################################

####### Camera Parameters #######
wCam, hCam = 640, 480 #size of the camera window pop up

######################################

######Captures the Cam###########
cap = cv2.VideoCapture(0)  #which cam to use = eg default
cap.set(3, wCam)     #Sets the width of capture
cap.set(4, hCam)     #Sets the height of capture
pTime = 0                   #creates a variable that has an assinged value to calc fps

######################################

#####Creates a hand detector object######
detector = htm.HandDetector(detectionCon=0.7, trackCon=0.7, maxHands=1)

######################################

#####Volume Control Setup#####
device = AudioUtilities.GetSpeakers()   #gets the speaker device
volume = device.EndpointVolume          #assing an object called volume to allow volume control
VolRange = volume.GetVolumeRange()      #creates an object which has the volume range
minVol = VolRange[0]
maxVol = VolRange[1]

#####Volume Variables#####
vol = 0
volBar = 400
volPer = 0
volumeLocked = True

####MEDIAPIPE landmark IDS for the finger Tips#####
#create a list for the fingers tips relating to its landmarks
tipIds = [4, 8, 12, 16, 20]

####Creates a Loop for the Hand Tracking Volume Controller###
while True:
    success, img = cap.read()   #capture image from webcam
    img = detector.findHands(img, draw=False)   #detects hand and does not draw it
    lmList, handType = detector.findPosition(img, draw=False)  #gets the landmark list and the handType to find L or R hand

    #If the hand is detected by looking at the landmarks being present
    if len(lmList) != 0:

#gets the x and y co-ordinates of the thumb and index finger
        x1, y1 = lmList[4][1], lmList[4][2] #THUMB TIP
        x2, y2 = lmList[8][1], lmList[8][2] #INDEX TIP

#finds the MIDPOINT of the line on x-axis and y-axis
        cx,cy = (x1+x2)//2, (y1+y2)//2

##Calculate the Hand size
##using distance between wrist(0) and middle finger (9)
        wX, wY = lmList[0][1], lmList[0][2]
        mX, mY = lmList[9][1], lmList[9][2]
        handSize = math.hypot(wX-mX, wY-mY)

        ######Finds the distance between thumb and index#####
        length = math.hypot(x2 - x1, y2 - y1)  # finds the hypotheneus to find the lenght of the line

        ##Normalise the length
        #nLen - rough #find number###
        nLen = length / handSize

        # sets the range for the volume in dp
        vol = np.interp(nLen, [0.2, 1.3], [minVol, maxVol])  # -------------------------------------------------------
        # sets the range for the volume that is being displayed
        volBar = np.interp(nLen, [0.2, 1.3], [400, 200])
        # perecentage convertion of volume
        volPer = np.interp(nLen, [0.2, 1.3], [0, 100])

    #applys the volume changes
        volume.SetMasterVolumeLevel(vol, None)

        # when the fingers touch it will create a button effect

        if nLen < 0.2:
            cv2.circle(img, (cx, cy), 8, (100, 100, 158), cv2.FILLED)




        #draws a circle at index and thumb
        cv2.circle(img, (x1, y1), 8, (155, 151, 232), cv2.FILLED)
        cv2.circle(img, (x2, y2), 8, (155, 151, 232), cv2.FILLED)
        #draws a line between the index and thumb points
        cv2.line(img, (x1, y1), (x2, y2), (232, 158, 206), 3)
        #draws a circle in the middle point of line of the thumb and index fingers
        cv2.circle(img, (cx, cy), 8, (155, 151, 232), cv2.FILLED)


    #volume bar
    cv2.rectangle(img, (50, 200), (85, 400), (200, 202, 0), 2)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 202, 158), cv2.FILLED)
    #display the % of volume
    cv2.putText(img, f' {int(volPer)} %', (42, 420), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 202, 158), 1)
    cv2.putText(img, f'VOLUME', (40, 192), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,0,0), 1)

    #FPS display
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20,30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,0,0), 1)

    cv2.imshow("Volume Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

