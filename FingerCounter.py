import cv2
import time
import os
import HandTrackingModule as htm

bHandImage = False

wCam, hCam = 1280, 1080

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "FingerImages"
myList = os.listdir(folderPath)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

pTime = 0
detector = htm.handDetector(detectionCon=0.75)

tipIds = [4,8,12,16,20]
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        fingers = []

        if lmList[1][1] > lmList[17][1]:
            # Thumb
            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        else:
            # Thumb
            if lmList[tipIds[0]][1] < lmList[tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        # 4 Fingers
        for id in range(1,len(tipIds)):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = fingers.count(1)    

        # For displaying images of hands
        if bHandImage:
            h, w, c = overlayList[totalFingers-1].shape
            img[0:h, 0:w] = overlayList[totalFingers-1]

        # For displaying text
        cv2.rectangle(img, (20,225), (170,425), (0,255,0),cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (255,0,0),25)
        
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (400,70),cv2.FONT_HERSHEY_PLAIN,3,
                (255,0,255),3)

    cv2.imshow("Image", img)
    # Enter key 'q' to break the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break