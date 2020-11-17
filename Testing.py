import numpy as np
import cv2
#import Photoes

cap = cv2.VideoCapture(0)

count = 0
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here

    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Set the color of the rectangle
    if(count%100>=40 and count%100<60):
        cv2.rectangle(gray,(450,150),(620,350),(255,255,255),3)
    else:
        cv2.rectangle(gray,(450,150),(620,350),(0,255,0),3)
    
    # Display the resulting frame
    cv2.imshow('frame',gray)

    #!!!!Uncomment only if required!!!!
    #cv2.imwrite("d.jpg", frame)
    count += 1
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture

cap.release()
#Photoes.init(200)
cv2.destroyAllWindows()
