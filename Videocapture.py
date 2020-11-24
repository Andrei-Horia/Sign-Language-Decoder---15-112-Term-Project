import numpy as np
import cv2
import ClassImageProcessing
import random

def record():
    cap = cv2.VideoCapture(0)

    imageChecker = False
    count = 0
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Set the color of the rectangle
        if(imageChecker == True):
            cv2.rectangle(gray,(450,150),(620,350),(255,255,255),3)
        else:
            cv2.rectangle(gray,(450,150),(620,350),(0,255,0),3)

        cv2.line(gray,(535,150),(535,350),(130,130,130),2)
        cv2.line(gray,(450,250),(620,250),(130,130,130),2)
        # Display the resulting frame
        cv2.imshow('frame',gray)

        cv2.imwrite("test" + str(count) + ".jpg", frame)
        count += 1

        
        if((count-10)%100==0 and count >= 100):
            imageChecker = ClassImageProcessing.ImageProcessing(count-10)
            imageChecker = imageChecker.startAll()
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture

    cap.release()
    #Photoes.init(200)
    cv2.destroyAllWindows()

def gameRecord():

    cap = cv2.VideoCapture(0)
    count = 0

    letter = random.randint(0,25) + 65
    val = None
    
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Set the color of the rectangle
        if(val == None or count >= 20):
            cv2.rectangle(gray,(450,150),(620,350),(125,125,125),3)
        elif(val == False and count < 20):
            cv2.rectangle(gray,(450,150),(620,350),(0,0,0),3)
        elif(val == True and count < 20):
            cv2.rectangle(gray,(450,150),(620,350),(255,255,255),3)

        cv2.line(gray,(535,150),(535,350),(130,130,130),2)
        cv2.line(gray,(450,250),(620,250),(130,130,130),2)

        cv2.putText(gray,str(chr(letter)), (510,120), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255),10)
        # Display the resulting frame
        cv2.imshow('frame',gray)
    
        pressedKey = cv2.waitKey(1) & 0xFF
        if pressedKey == ord('q'):
            break
        elif pressedKey == ord('s'):
            cv2.imwrite("game.jpg", frame)
            A = ClassImageProcessing.Game(letter)
            val = A.start()
            count = 0
            letter = random.randint(0,25) + 65
                
        count += 1
        
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

#record()
