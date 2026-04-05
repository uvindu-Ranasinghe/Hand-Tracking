######### Hand Tracking Controlled Volume Changer ##########

### Imports the Modules/Libraries ######
#These are pre-written code that act as tools to utilize extra features#

import cv2           #library that allows me to use the Camera and draw graphics
import time          #Tool used to cal the FPS
import numpy as np   #Math helper library
from pycparser.c_ast import For
import handTrackingModule as htm  #imports the hand tracking module I made as htm.
import math           #Pre-built math functions
from pycaw.pycaw import AudioUtilities  #Lets python control the volume - got this from GIT HUB

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
detector = htm.HandDetector(detectionCon=0.8, maxHands=1)

######################################

#####Volume Control Setup#####
device = AudioUtilities.GetSpeakers()   #gets the speaker device
volume = device.EndpointVolume          #assing an object called volume to allow volume control

###############IGNORE#################
#print(f"Audio output: {device.FriendlyName}")
#print(f"- Muted: {bool(volume.GetMute())}")
#print(f"- Volume level: {volume.GetMasterVolumeLevel()} dB")
###############IGNORE#################

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
    lmList, handType = detector.findPosition(img, draw=True)  #gets the landmark list and the handType to find L or R hand

    #If the hand is detected by looking at the landmarks being present
    if len(lmList) != 0:
        #print(lmList[4], lmList[8])

        fingers = []  #Creates a list to store the open(1) and close(0) stage of the fingers

        #######detect movement of the thumb######
        ##the thumb movement is side to side - we get x values##

        if handType == "Right":
            #checks to see if thumb tip is left of joint
            if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            #Checks to see if thumb tip is right of joint
        elif handType == "Left":
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        #####detect movement of the other 4 fingers#####
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]: #checks to see if the y value of index is below the joint
                fingers.append(1)
            else:
                fingers.append(0)

        ######IGNORE######
        # print(fingers)
        ######IGNORE######

#gets the x and y coodinates of the thumb and index finger
        x1, y1 = lmList[4][1], lmList[4][2] #THUMB TIP
        x2, y2 = lmList[8][1], lmList[8][2] #INDEX TIP

#finds the MIDPOINT of the line on x-axis and y-axis
        cx,cy = (x1+x2)//2, (y1+y2)//2

#draws a circle at index and thumb
        cv2.circle(img, (x1, y1), 8, (155, 151, 232), cv2.FILLED)
        cv2.circle(img, (x2, y2), 8, (155, 151, 232), cv2.FILLED)
#draws a line between the index and thumb points
        cv2.line(img, (x1, y1), (x2, y2), (232, 158, 206), 3)
#draws a circle in the middle point of line of the thumb and index fingers
        cv2.circle(img, (cx, cy), 8, (155, 151, 232), cv2.FILLED)

        ######Finds the distance between thumb and index#####
        length = math.hypot(x2-x1, y2-y1) #finds the hypotheneus to find the lenght of the line
        print(length)

        ######NOTE#####
        #Hange length range is from 150 to 20
        #volume range is from -65 to 0

        ###### Volume Control Gestures ######
        # only active if the thumb is open, index is open and other fingers closed #
        #volume change depending on the length of the line based on the minimum and max lenghth calibarions based on the max & low volume
        ########if fingers[0] == 1 and fingers[1] == 1 and sum(fingers[2:]) == 0: #fuck this does not work

            # Creates a length constraint for the max and mix lengths that can be recorded
            #length = max(18, min(length,146))

        # reference hand size
        x0, y0 = lmList[0][1], lmList[0][2]
        x9, y9 = lmList[9][1], lmList[9][2]

        handSize = max(1, math.hypot(x9 - x0, y9 - y0))

        normLength = length / handSize
        normLength = max(0.15, min(normLength, 0.8))

        #sets the range for the volume in dp
        vol = np.interp(length, [23, 146], [minVol, maxVol]) #-------------------------------------------------------
        #sets the range for the volume that is being displayed
        volBar = np.interp(length, [23, 146], [400, 200])
        #perecentage convertion of volume
        volPer = np.interp(length, [23, 146], [0, 100])

        #print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)
#when the fingers touch it will create a button effect
        if length < 23:
            cv2.circle(img, (cx, cy), 8, (232, 202, 158), cv2.FILLED)

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

    cv2.imshow("Image", img)
    cv2.waitKey(1)
