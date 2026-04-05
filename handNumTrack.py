import cv2
import time
import os
import handTrackingModule as htm


#####################################
#parameters
wCam, hCam = 640, 480
######################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

folderPath = "finger_Images"
myList = os.listdir(folderPath)
print(myList)
overlayList = []

for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
   # print(f'{folderPath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))

detector = htm.HandDetector(detectionCon=0.75)

#create a list for the fingers
tipIds = [4, 8, 12, 16, 20]

while True:

    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:

        fingers = []

#in open cv max value is the top it starts at 0 AND THE LEFT OF THE SCREEN STARTS AT 0 AS WELL##########
        #FOR LEFT HAND

        if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

     #   #an if statement for the thumb - x axis involved - RIGHT HAND
     #   if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
     #       print("index finger open")
      #  else:
     #       print("index finger close")


#loop for fingers 1 to 5
        for id in range(1,5):
            if lmList[tipIds[id]][2] > lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        #print(fingers)

        #find how many 1's we have
        totalFinger = fingers.count(1)
        print(totalFinger)


        #fomat is index first and second is the element - we are looking to see if the y points are greater or lesser
       # if lmList[8][2] < lmList[6][2]:
            #print("index finger open")
       # else:
          #  print("index finger close")

    # automate the shape fixing to fit the overlay in
        h, w, c = overlayList[totalFinger - 1].shape
    #slicing the display & it creates an overlay (h x l)
        img[0:h, 0:w] = overlayList[totalFinger - 1] #it will take in the number of fingers minus 1 to find the index of the pic

    # FPS display
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250, 0, 0), 1)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

