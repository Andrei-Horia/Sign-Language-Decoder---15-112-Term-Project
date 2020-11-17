# Sign-Language-Decoder---15-112-Term-Project

This program will decypher the sign language into normal text. 

For it to work, the user would have to create a sign in a certain area which will be represented by a black frame, wait two-three seconds without moving or changing the sign so the program recognizes the sign, and then completly remove the hand out of the box. After some time the color of the frame will turn white and then black, indicating that the user can now create a different sign in the same area. This process repeats until the user decides to close the video by pressing 'q'.


# Code:

The code will be distributed over three python files; each file will have a different function
File 1: ImageWriter 
    This file allows other files to access the ImageWriter class
		
File 2: Videocapture
 This file records a live video of the user making the sign (I will use the videocapture feature of cv2)
 I will also display a rectangle on the screen that will indicate the area/box where the user should create the sign.
   
 The rectangle will have two phases:
  	Phase 1: The user is making the sign which means that the hand is inside the box. In this phase the rectangle will have a black border 
	Phase 2: The user finished the sign and removed the hand out of the box. In this phase after 3 seconds the rectangle will change its border to white and return to phase1. 
				
   
   Currently, the rectangle will change phases every 3-4 seconds. (I will implement the phasining algorithm tommorrow)
   Each 10th frame will be sent to the 3rd file which will analyze it.
    
File 3: ImageProcessing
  This file will analyze the frame sent from Videocapture
  First, the frame will be cut to the rectangle size in order to save time
  Second, the frame will be converted to grayscale and then to black and white, where every white pixel will represent the background and every black pixel will be the hand.
  Third, I will use vertical segmentation and horizontal segmentation to capture the exact sign position (starting point, end point)
  Fourth, since some of the signs have a lot of white pixel where there were supposed to be black pixels, I am using two fill algorithms, one for the center and one for the         exterior, to turn the pixels that were supposed to be white into green pixels.
  Fifth, each remaining white pixel is supposed to be black so I convert them.
  Sixth, the picture will be segmented into four quadrants.
  Finally, I am calculating the percent of black pixels in each quadrant and based on the resulting numbers, I am deducing the letter.
  
  
    
