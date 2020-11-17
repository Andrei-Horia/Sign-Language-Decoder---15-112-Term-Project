import cv2
import ImageWriter
import sys
import random

#This function crops the image to the required size
def cropImage(name):
    pic = ImageWriter.loadPicture(name)
    
    convertBlackandWhite(pic)
    
    cv2.waitKey(0)
    return pic

#This function converts to grayscale and then to black and white
def convertBlackandWhite(pic):
    width = ImageWriter.getWidth(pic)
    height = ImageWriter.getHeight(pic)
    col = []
    for y in range(height):
        for x in range(width):
            col = ImageWriter.getColor(pic, x, y)

            gray = sum(col)//3
            avg = 255
            
            #Black and White check 
            if(gray<=138.5):
                avg = 0
                
            ImageWriter.setColor(pic,x,y,[avg,avg,avg])

#This function does the vertical segmentation
def findFirstBlack(pic):
    width = ImageWriter.getWidth(pic)
    height = ImageWriter.getHeight(pic)
    left, right = 0,0
    countBlack = 0
    maxBlack = 0
    for x in range(width):
        meetBlack = False
        for y in range(height):
            col = ImageWriter.getColor(pic,x,y)
            
            if(col == [0,0,0]):
               countBlack += 1
               meetBlack = True
               break
        
        if(meetBlack == False):
             if(countBlack > maxBlack):
                    maxBlack = countBlack
                    left = x - countBlack
                    right = x
             countBlack = 0
                
    
    if(countBlack > maxBlack):
         maxBlack = countBlack
         left = x - countBlack
         right = x
            
    return left,right

#This function does the horizontal segmentation
def horizontalSegmentation(pic,start,end):
    width = end
    height = ImageWriter.getHeight(pic)
    up, down = 0,0
    countBlack = 0
    maxBlack = 0
    for y in range(height):
        meetBlack = False
        for x in range(start,width):
            col = ImageWriter.getColor(pic,x,y)
            if(col == [0,0,0]):
               countBlack += 1
               meetBlack = True
               break

        
        if(meetBlack == False):
             if(countBlack > maxBlack):
                    maxBlack = countBlack
                    up = y - countBlack-1
                    down = y
             countBlack = 0
                
    if(countBlack > maxBlack):
            maxBlack = countBlack
            up = y - countBlack-1
            down = y
               
    return up,down

#This function fills the interior with green pixels
def fillCenter(pic,startX,endX,startY,endY):
    midY = (startY + endY)//2

    midX = (startX + endX)//2

    
    for x in range(midX,endX):
        col = ImageWriter.getColor(pic,x,midY)
        if(col == [255,255,255]):
            ImageWriter.setColor(pic,x,midY,[0,255,0])
        else:
            break

    for x in range(midX-1,startX,-1):
        col = ImageWriter.getColor(pic,x,midY)
        if(col == [255,255,255]):
            ImageWriter.setColor(pic,x,midY,[0,255,0])
        else:
            break

    for y in range(midY-1,startY,-1):
        col = ImageWriter.getColor(pic,midX,y)
        if(col == [255,255,255] or col == [0,255,0]):
            ImageWriter.setColor(pic,midX,y,[0,255,0])
        else:
            break

    
    for y in range(midY,endY):
        col = ImageWriter.getColor(pic,midX,y)
        if(col == [255,255,255] or col == [0,255,0]):
            ImageWriter.setColor(pic,midX,y,[0,255,0])
        else:
            break
    
    for y in range(midY+1,endY):

        for x in range(startX+1,endX):
            col = ImageWriter.getColor(pic,x,y)
            colDown = ImageWriter.getColor(pic,x,y-1)
            
            if(col == [255,255,255]):
               if(colDown == [0,255,0]):
                   ImageWriter.setColor(pic,x,y,[0,255,0])
            
    for y in range(midY,startY,-1):

        for x in range(startX+1,endX):
            col = ImageWriter.getColor(pic,x,y)
            colUp = ImageWriter.getColor(pic,x,y+1)
            
            if(col == [255,255,255]):
               if(colUp == [0,255,0]):
                   ImageWriter.setColor(pic,x,y,[0,255,0])


    for x in range(midX,endX):

        for y in range(startY,endY):
            col = ImageWriter.getColor(pic,x,y)
            colLeft = ImageWriter.getColor(pic,x-1,y)
            
            if(col == [255,255,255]):
               if(colLeft == [0,255,0]):
                   ImageWriter.setColor(pic,x,y,[0,255,0])

    for x in range(midX,startX,-1):
        for y in range(startY,endY):
            col = ImageWriter.getColor(pic,x,y)
            colRight = ImageWriter.getColor(pic,x+1,y)
            
            if(col == [255,255,255]):
               if(colRight == [0,255,0]):
                   ImageWriter.setColor(pic,x,y,[0,255,0])


#This function fills the exterior with green pixels
def fillSizes(pic,startX,endX,startY,endY):

    for y in range(startY,endY):

        for x in range(startX+1,endX):
            col = ImageWriter.getColor(pic,x,y)
            colLeft = ImageWriter.getColor(pic,x-1,y)
            colUp = ImageWriter.getColor(pic,x,y-1)
            if(col == [255,255,255]):
                if(colLeft == [0,255,0] or colUp == [0,255,0]):
                    ImageWriter.setColor(pic,x,y,[0,255,0])

#This function fill the white gaps after filling
def fillGapsBlack(pic,startX,endX,startY,endY):
    for x in range(startX,endX):
        for y in range(startY,endY):
            col = ImageWriter.getColor(pic,x,y)
            if(col == [255,255,255]):
                ImageWriter.setColor(pic,x,y,[0,0,0])


#This function calculates the amount of black pixels in each quadrant
def calculate(pic,startX,endX,startY,endY):

    midX,midY = 0,0
    midX = (startX + endX)//2
    midY = (startY + endY)//2

    result = [0,0,0,0]
    black = [0,0,0,0]
    total = [0,0,0,0]

    
    for y in range(startY,endY):
        for x in range(startX,endX):
            
            col = ImageWriter.getColor(pic,x,y)
            if(x<midX and y<midY):
                if(col == [0,0,0]):
                   black[0] += 1
                total[0] += 1
                

            if(x>midX and y<midY):
                if(col == [0,0,0]):
                   black[1] += 1
                total[1] += 1

            if(x>midX and y<midY):
                if(col == [0,0,0]):
                   black[2] += 1
                total[2] += 1

            if(x>midX and y>midY):
                if(col == [0,0,0]):
                   black[3] += 1
                total[3] += 1

    result = [round(black[0]/total[0],3),round(black[1]/total[1],3),
              round(black[2]/total[2],3),round(black[3]/total[3],3)]

    return result
                   
def init(size):
    for i in range(65,80,5):
        pic = "frame" + str(i) + ".jpg"
        pic = cropImage(pic)

        #Get vertical segmentatation
        left,right = findFirstBlack(pic)
        left = left - 1
        print(left,right)

        #Check Marker
        for y in range(ImageWriter.getHeight(pic)):
            ImageWriter.setColor(pic,left+1,y,[0,255,0])
            ImageWriter.setColor(pic,left,y,[255,0,0])
            ImageWriter.setColor(pic,right,y,[255,0,0])

        #Get horizontal segmentation
        up,down = horizontalSegmentation(pic,left,right)
        up = up - 1

        #Check Marker
        for x in range(ImageWriter.getWidth(pic)):
            ImageWriter.setColor(pic,x,up+1,[0,255,0])
            ImageWriter.setColor(pic,x,up,[255,0,0])
            ImageWriter.setColor(pic,x,down,[255,0,0])

        #ImageWriter.updatePicture(pic)
        #ImageWriter.showPicture(pic)
        fillCenter(pic,left,right,up,down)
        fillSizes(pic,left,right,up,down)
        fillGapsBlack(pic,left,right,up,down)
        #fillImage(pic,vertical)
        ImageWriter.updatePicture(pic)
        ImageWriter.showPicture(pic)
        result=calculate(pic,left,right,up,down)

init(200)
    

    
