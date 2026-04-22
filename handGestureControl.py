## Imports the Modules/Libraries ######

import cv2
import time
import numpy as np
import handTrackingModule as hTM
import handTrackingVol
import math

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

####Creates a Loop for the Hand Tracking ###
while True:
    success, img = cap.read()
    # flips the camera image horizontally - this is due to the fact that the image gets mirrored giving the perspective of the individual.
    # It gives a mirrored image.
    img = cv2.flip(img, 1)
    img = detector.findHands(img, draw=True)
    lmList, handType = detector.findPosition(img, draw=False)




