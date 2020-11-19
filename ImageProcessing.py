import cv2
import ImageWriter
import sys
import random


class ImageProcessing():
    
    def __init__(self,size):
        self.pic = self.cropImage("test" + str(size) + ".jpg")

    def cropImage(self,name):
        pic = ImageWriter.loadPicture(name)
    
        return pic
    
    def startAll(self):
        
        pic = self.pic
    
        self.convertBlackandWhite()

        ok = 0
        for x in range(ImageWriter.getWidth(pic)):
            for y in range(ImageWriter.getHeight(pic)):
                col = ImageWriter.getColor(pic,x,y)
                if(col == [0,0,0]):
                    ok = 1
                    break
            if(ok == 1):
                break

        if(ok==0):
            return True

        #ImageWriter.showPicture(pic)
        if(ok == 1):
            #Get vertical segmentatation
            left,right = self.findFirstBlack()
            left = left - 1

            #Check Marker
            for y in range(ImageWriter.getHeight(pic)):
                ImageWriter.setColor(pic,left+1,y,[0,255,0])

            #Get horizontal segmentation
            up,down = self.horizontalSegmentation(left,right)
            up = up - 1

            #Check Marker
            for x in range(ImageWriter.getWidth(pic)):
                ImageWriter.setColor(pic,x,up+1,[0,255,0])

            self.fillCenter(left,right,up,down)
            self.fillSizes(left,right,up,down)
            self.fillGapsBlack(left,right,up,down)
            
            ImageWriter.updatePicture(pic)
            ImageWriter.showPicture(pic)
            result=self.calculate(left,right,up,down)

            self.table(result)
        return False

    #This function converts to grayscale and then to black and white    
    def convertBlackandWhite(self):
        pic = self.pic
        
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
    def findFirstBlack(self):
        pic = self.pic
        
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
    def horizontalSegmentation(self,start,end):
        pic = self.pic
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
    def fillCenter(self,startX,endX,startY,endY):
        pic = self.pic

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
    def fillSizes(self,startX,endX,startY,endY):
        pic = self.pic
        
        for y in range(startY,endY):

            for x in range(startX+1,endX):
                col = ImageWriter.getColor(pic,x,y)
                colLeft = ImageWriter.getColor(pic,x-1,y)
                colUp = ImageWriter.getColor(pic,x,y-1)
                if(col == [255,255,255]):
                    if(colLeft == [0,255,0] or colUp == [0,255,0]):
                        ImageWriter.setColor(pic,x,y,[0,255,0])

    #This function fill the white gaps after filling
    def fillGapsBlack(self,startX,endX,startY,endY):
        pic = self.pic
        for x in range(startX,endX):
            for y in range(startY,endY):
                col = ImageWriter.getColor(pic,x,y)
                if(col == [255,255,255]):
                    ImageWriter.setColor(pic,x,y,[0,0,0])


    #This function calculates the amount of black pixels in each quadrant
    def calculate(self,startX,endX,startY,endY):
        pic = self.pic
        
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

                if(x<midX and y>midY):
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

  

    def table(self,result):
        min = 21000000
        Res = ""
        print(result)
        A,B,C,D = result[0],result[1],result[2],result[3]
        table = [
                 [0.610 , 0.360 , 0.410 , 0.947 ],
                 [0.810 , 0.210 , 0.870 , 0.857 ],
                 [0.350 , 0.504 , 0.299 , 0.842 ],
                 [0.369 , 0.001 , 0.840 , 0.663 ],
                 [0.805 , 0.305 , 0.652 , 0.885 ],
                 [0.382 , 0.423 , 0.829 , 0.883 ],
                 [0.442 , 0.726 , 0.360 , 0.750 ],
                 ]
        for i in range(7):
            val = 0
            for j in range(4):
                val += abs(result[j] - table[i][j])

            if(val<min):
                min = val
                Res = chr(65 + i)
                

        print(Res)
        


