import numpy as np
import cv2
import ClassImageProcessing
import random
import time



###------------Record-------------####
def record():
    cap = cv2.VideoCapture(0)

    imageChecker = False
    count = 0

    #Load Loading Screen
    loadingScreen = cv2.imread("L.jpg")
    loadingScreen = cv2.resize(loadingScreen, (640,482), interpolation = cv2.INTER_AREA)

    lock = 10
    letter = ""
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

        #Draw the box
        cv2.line(gray,(535,150),(535,350),(130,130,130),2)
        cv2.line(gray,(450,250),(620,250),(130,130,130),2)

        #Display the letter
        if(letter != "" and letter != " "):
            cv2.putText(gray,str(letter), (120,360), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255),10)

        # Display the resulting frame
        if lock<=7:
            cv2.imshow('frame',loadingScreen)
        else:
            cv2.imshow('frame',gray)

        count += 1
        lock += 1

        #Save the frame
        if((count-10)%100==0 and count >= 100):
            cv2.imwrite("test.jpg", frame)
            lock = 0

        #Analyze the frame
        if(lock == 7):
            A = ClassImageProcessing.ImageProcessing()
            imageChecker = A.startAll()
            val = A.getMessage()
            letter = val
            letter.strip()
            if(letter[-1]>='A' and letter[-1]<='Z'):
               letter = letter[-1]
            else:
                letter= letter[-2]
                
            #print(letter[-1])
            #print(val)

        #Check the pressed key
        pressedKey = cv2.waitKey(1) & 0xFF
            
        if pressedKey == ord('q'):
            A = ClassImageProcessing.ImageProcessing()
            break
        elif pressedKey == ord('d'):
            A = ClassImageProcessing.ImageProcessing()
            A.delete()
            

    # When everything done, release the capture

    cap.release()
    #Photoes.init(200)
    cv2.destroyAllWindows()
    val = A.getMessage()
    A.reset()
    return val
    
###---------------------Game Record------------------###
def gameRecord():

    cap = cv2.VideoCapture(0)
    count = 0
    correct = 0
    letter = random.randint(0,25) + 65
    val = None
    gameRound = 0

    #Add the loading Screen
    loadingScreen = cv2.imread("L.jpg")
    loadingScreen = cv2.resize(loadingScreen, (640,482), interpolation = cv2.INTER_AREA)

    OK = False
    lock = 10
                               
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

        #Format the box
        cv2.line(gray,(535,150),(535,350),(130,130,130),2)
        cv2.line(gray,(450,250),(620,250),(130,130,130),2)

        cv2.putText(gray,str(chr(letter)), (510,120), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255),10)
        # Display the resulting frame

        if(lock>=7):
            cv2.imshow('frame',gray)
        else:
            cv2.imshow('frame',loadingScreen)

        lock += 1

        #Analyze the scores
        if(OK == True and lock == 7):
            A = ClassImageProcessing.Game(letter)
            val = A.start()
            if(val == True):
                correct += 1
    
            count = 0
            letter = random.randint(0,25) + 65
            gameRound += 1
            OK = False

        #Remeber which key was pressed
        pressedKey = cv2.waitKey(1) & 0xFF
            
        if pressedKey == ord('q'):
            break
        
        elif pressedKey == ord('s'):
            lock = 0
            cv2.imwrite("game.jpg", frame)
            OK = True
            
        if(gameRound == 5):
            break
            
        count += 1
        
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    return correct

#record()
