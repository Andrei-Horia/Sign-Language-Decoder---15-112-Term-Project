import cv2
import ImageWriter
import sys
import random


class ImageProcessing():
    
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

            ImageWriter.showPicture(pic)
            
            result=self.calculate(left,right,up,down)

            res = self.table(result)
            
            if(res in "ANST"):
                loc = self.ANST(left,right,up,down)
                if(res != loc):
                    res = loc

            if(res in "RU"):
                loc = self.RU(left,right,up,down)
                if(res!=loc):
                    res = loc

            if(res in "BME"):
                loc = self.BME(left,right,up,down)
                if(res!=loc):
                    res = loc

            if(res in "VW"):
                loc = self.VW(left,right,up,down)
                if(res!=loc):
                    res = loc

            if(res in "CP"):
                loc = self.CP(left,right,up,down)
                if(res!=loc):
                    res = loc
            print(res)
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

  

    def table(self,result):
        min = 21000000
        Res = ""
        print(result)
        A,B,C,D = result[0],result[1],result[2],result[3]
        table = [
                 #A
                 [0.6000 , 0.520 , 0.450 , 0.997 ],
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
                 #X
                 [0.452 , 0.499 , 0.630 , 1.000 ],
                 #Y
                 [0.084 , 0.396 , 0.545 , 0.992 ],
                 ]
        for i in range(25):
            val = 0
            for j in range(4):
                val += abs(result[j] - table[i][j])

            if(val<min):
                min = val
                Res = chr(65 + i)
                

        return Res

    #Checker for letter A N and T
    def ANST(self,startX,endX,startY,endY):
        pic = self.pic
        midY = (startY + endY)//2
        
        if(endY-startY<=150):
           return "S"
        
        for x in range(startX,endX):
            
            col = ImageWriter.getColor(pic,x,startY + 20)
            
            if(col == [0,0,0]):
                if(x <= 8):
                    return "A"
                elif(x <= 17):
                    return ("T")
                elif(x <= 60):
                    return ("N")
                


    def RU(self,startX,endX,startY,endY):
        pic = self.pic

        black1 = True
        black2 = True
        black3 = True
        countRow1 = 0
        countRow2 = 0
        countRow3 = 0
        
        for x in range(startX+2,startX+70):
            col1 = ImageWriter.getColor(pic,x,startY+20)
            col2 = ImageWriter.getColor(pic,x,startY+25)
            col3 = ImageWriter.getColor(pic,x,startY+15)

            
            if(col1 == [0,0,0] and black1 == True):
                countRow1 += 1
                black1 = False

            if(col1 == [0,255,0] and black1 == False):
                black1 = True

            if(countRow1 == 2):
                return "R"

            if(col2 == [0,0,0] and black2 == True):
                countRow2 += 1
                black2 = False
                
            if(col2 == [0,255,0] and black2 == False):
                black2 = True
            
            if(countRow2 == 2):
                return "R"

            if(col3 == [0,0,0] and black3 == True):
                countRow3 += 1
                black3 = False

            if(col3 == [0,255,0] and black3 == False):
                black3 = True

            if(countRow3 == 2):
                return "R"
                
        return "U"    
        
    def BME(self,startX,endX,startY,endY):
        if(endY-startY) < 110:
            return "M"
        elif(endY-startY) < 170:
            return "E"
        return "B"

    def VW(self,startX,endX,startY,endY):
        pic = self.pic

        black1 = True
        black2 = True
        black3 = True
        countRow1 = 0
        countRow2 = 0
        count1 = 0
        count2 = 0
        
        for x in range(startX+2,startX+100):
            col1 = ImageWriter.getColor(pic,x,startY+20)
            col2 = ImageWriter.getColor(pic,x,startY+25)

            if(col1 == [0,0,0] and black1 == True and count1 >=5):
                countRow1 += 1
                black1 = False

            if(col1 == [0,255,0] and black1 == False):
                black1 = True
                count1 = 0

            if(col1 == [0,0,0]):
                count1 += 1

            if(countRow1 == 3):
                return "W"

            if(col2 == [0,0,0] and black2 == True and count2 >= 5):
                countRow2 += 1
                black2 = False
                
            if(col2 == [0,255,0] and black2 == False):
                black2 = True
                count2 = 0

            if(col2 == [0,0,0]):
                count2 += 1

            if(countRow2 == 3):
                return "W"
                
        return "V" 

    def CP(self,startX,endX,startY,endY):
        pic = self.pic
        middX = (startX + endX)//2
        middY = (startY + endY)//2
        col = ImageWriter.getColor(pic,middX,middY)
        if(col == [0,255,0]):
            return "C"
        return "P"
        
class Game(ImageProcessing):
    def __init__(self,letter):
        self.pic = ImageProcessing.cropImage(self,"game.jpg")
        self.letter = chr(letter)

    def start(self):
        pic = self.pic

        ImageProcessing.convertBlackandWhite(self)
        
        #loadingScreen = cv2.imread('LoadingScreen.jpg')
        #loadingScreen = cv2.resize(loadingScreen, (640,482), interpolation = cv2.INTER_AREA)
        #cv2.imshow('Loading Screen',loadingScreen)

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

            res = ImageProcessing.table(self,result)
            if(res in "ANST"):
                loc = ImageProcessing.ANST(self,left,right,up,down)
                if(res != loc):
                    res = loc

            if(res in "RU"):
                loc = ImageProcessing.RU(self,left,right,up,down)
                if(res!=loc):
                    res = loc

            if(res in "BME"):
                loc = ImageProcessing.BME(self,left,right,up,down)
                if(res!=loc):
                    res = loc

            if(res in "VW"):
                loc = ImageProcessing.VW(self,left,right,up,down)
                if(res!=loc):
                    res = loc
                    
            if(res in "CP"):
                loc = ImageProcessing.CP(self,left,right,up,down)
                if(res!=loc):
                    res = loc
                    
            print(res)

            ImageWriter.showPicture(pic)
            
            #cv2.destroyAllWindows()

            
            if(res == self.letter):
                return True
            else:
                return False
