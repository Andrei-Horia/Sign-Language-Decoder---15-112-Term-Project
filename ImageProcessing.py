import cv2
import ImageWriter
import sys
import random
import Accuracy

class ImageProcessing():
    MESSAGE = ""
    COUNT = 3
    
    def __init__(self):
        self.pic = self.cropImage("test.jpg")

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
            ImageProcessing.MESSAGE += " "
            if(ImageProcessing.COUNT%24==0):
                ImageProcessing.MESSAGE += "\n"
            ImageProcessing.COUNT += 1
            return True

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

            #ImageWriter.showPicture(pic)
            
            result=self.calculate(left,right,up,down)

            res = self.table(result,left,right,up,down)

            print(res)
            A = Accuracy.IncreaseAccuracy(pic,res,left,right,up,down)
            res = A.all()

            ImageProcessing.MESSAGE += res
            if(ImageProcessing.COUNT%24==0):
                ImageProcessing.MESSAGE += "\n"
            ImageProcessing.COUNT += 1
            print(res)
            ImageWriter.showPicture(pic)

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

        col = ImageWriter.getColor(pic,midX,midY)
        if(col == [255,255,255]):
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

  

    def table(self,result,startX,endX,startY,endY):
        min = 21000000
        Res = ""
        print(result)
        A,B,C,D = result[0],result[1],result[2],result[3]
        table = [
                 #A
                 [0.600 , 0.520 , 0.450 , 0.997 ],
                 #B
                 [0.556 , 0.490 , 0.904 , 0.947 ],
                 #C
                 [0.350 , 0.504 , 0.299 , 0.842 ],
                 #D
                 [0.369 , 0.001 , 0.840 , 0.783 ],
                 #E
                 [0.605 , 0.555 , 0.752 , 0.885 ],
                 #F
                 [0.312 , 0.483 , 0.829 , 0.893 ],
                 #G
                 [0.402 , 0.801 , 0.060 , 0.820 ],
                 #H
                 [0.430 , 0.801 , 0.012 , 0.820 ],
                 #I
                 [0.243 , 0.486 , 0.800 , 0.975 ],
                 #J
                 [0.720 , 0.650 , 0.915 , 1.000 ],
                 #K
                 [0.240 , 0.450 , 0.610 , 0.900 ],
                 #L 
                 [0.192 , 0.189 , 0.185 , 0.849 ],
                 #M
                 [0.604 , 0.473 , 0.906 , 0.999 ],
                 #N
                 [0.528 , 0.473 , 0.500 , 0.992 ],
                 #O
                 [0.520 , 0.695 , 0.360 , 0.865 ],
                 #P
                 [0.330 , 0.420 , 0.362 , 0.854 ],
                 #Q
                 [0.130 , 0.846 , 0.580 , 1.000 ],
                 #R
                 [0.407 , 0.003 , 0.810 , 0.787 ],
                 #S
                 [0.674 , 0.705 , 0.510 , 0.992 ],
                 #T
                 [0.445 , 0.233 , 0.556 , 0.985 ],
                 #U
                 [0.560 , 0.000 , 0.907 , 0.677 ],
                 #V
                 [0.281 , 0.500 , 0.640 , 0.845 ],
                 #W
                 [0.318 , 0.429 , 0.553 , 0.816 ],
                 #X1
                 [0.632 , 0.329 , 0.760 , 0.920 ],
                 #X2
                 [0.318 , 0.342 , 0.627 , 0.910 ],
                 #Y
                 [0.084 , 0.396 , 0.545 , 0.992 ],
                 #Z
                 [0.211 , 0.700 , 0.966 , 1.000 ],
                 ]
        for i in range(26):
            val = 0
            for j in range(4):
                val += abs(result[j] - table[i][j])

            if(val<min):
                min = val
                if(i < 23):
                    Res = chr(65 + i)
                else:
                    Res = chr(65 + i - 1)
                

        return Res

    def getMessage(self):
        return ImageProcessing.MESSAGE

    def delete(self):
        if(ImageProcessing.MESSAGE != " "):
            ImageProcessing.MESSAGE = ImageProcessing.MESSAGE[:len(ImageProcessing.MESSAGE)-1]
        
    def exit(self):
        return (self.MESSAGE)

    def reset(self):
        ImageProcessing.MESSAGE = ""

        
class Game(ImageProcessing):
    def __init__(self,letter):
        self.pic = ImageProcessing.cropImage(self,"game.jpg")
        self.letter = chr(letter)

    def start(self):
        pic = self.pic

        ImageProcessing.convertBlackandWhite(self)
        
        ok = 0
        for x in range(ImageWriter.getWidth(pic)):
            for y in range(ImageWriter.getHeight(pic)):
                col = ImageWriter.getColor(pic,x,y)
                if(col == [0,0,0]):
                    ok = 1
                    break
            if(ok == 1):
                break
        
        if(ok==1):
            left,right = ImageProcessing.findFirstBlack(self)
            left = left - 1

            #Check Marker
            for y in range(ImageWriter.getHeight(pic)):
                ImageWriter.setColor(pic,left+1,y,[0,255,0])


            #Get horizontal segmentation
            up,down = ImageProcessing.horizontalSegmentation(self,left,right)
            up = up - 1

            #Check Marker
            for x in range(ImageWriter.getWidth(pic)):
                ImageWriter.setColor(pic,x,up+1,[0,255,0])

            ImageProcessing.fillCenter(self,left,right,up,down)
            ImageProcessing.fillSizes(self,left,right,up,down)
            ImageProcessing.fillGapsBlack(self,left,right,up,down)
                
                            
            result=ImageProcessing.calculate(self,left,right,up,down)

            res = ImageProcessing.table(self,result,left,right,up,down)
            
            A = Accuracy.IncreaseAccuracy(pic,res,left,right,up,down)
            res = A.all()
            
            print(res)

            ImageWriter.showPicture(pic)
            
            #cv2.destroyAllWindows()

            
            if(res == self.letter):
                return True
            else:
                return False
        
