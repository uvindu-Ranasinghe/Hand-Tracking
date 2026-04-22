######### Hand Tracking Controlled Volume Changer ##########

### Imports the Modules/Libraries ######

import cv2
import time
import numpy as np
import handTrackingModule as hTM
import math
from pycaw.pycaw import AudioUtilities

#####################################

####### Camera Parameters #######

wCam, hCam = 640, 480 #size of the camera window pop up

######################################

######Captures the Cam###########

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

######################################

detector = hTM.HandDetector(detectionCon=0.6, trackCon=0.6, maxHands=1)

######################################

#####Volume Control Setup#####
device = AudioUtilities.GetSpeakers()
volume = device.EndpointVolume
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

#####Volume Variables#####
vol = 0
volBar = 400
volPer = 0
volumeLocked = True
hMin = 0.2
hMax = 1.5


####Creates a Loop for the Hand Tracking Volume Controller###
while True:
    success, img = cap.read()
    # flips the camera image horizontally - this is due to the fact that the image gets mirrored giving the perspective of the individual.
    # It gives a mirrored image.
    img = cv2.flip(img, 1)
    img = detector.findHands(img, draw=True)
    lmList, handType = detector.findPosition(img, draw=False)

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
        length = math.hypot(x2 - x1, y2 - y1)  # finds the hypotenuse to find the length of the line

        ##Normalise the length
        nLen = length / handSize

        rawVolPer = float(np.interp(nLen, [hMin, hMax], [0, 100]))

        volPer =int( round(rawVolPer/5) * 5)

        volScalar = volPer / 100

        volBar = np.interp(volPer, [0, 100], [400, 200])

        volume.SetMasterVolumeLevelScalar(volScalar, None)

        #draws a circle at index and thumb
        cv2.circle(img, (x1, y1), 8, (155, 151, 232), cv2.FILLED)
        cv2.circle(img, (x2, y2), 8, (155, 151, 232), cv2.FILLED)
        #draws a line between the index and thumb points
        cv2.line(img, (x1, y1), (x2, y2), (232, 158, 206), 3)
        #draws a circle in the middle point of line of the thumb and index fingers
        cv2.circle(img, (cx, cy), 8, (155, 151, 232), cv2.FILLED)

        # when the fingers touch it will create a button effect
        if nLen < 0.2:
             cv2.circle(img, (cx, cy), 10, (100, 180, 170), cv2.FILLED)


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

