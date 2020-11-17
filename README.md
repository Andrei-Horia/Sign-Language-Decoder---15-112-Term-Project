# Sign-Language-Decoder---15-112-Term-Project

This program will decypher the sign language into normal text. 

# Instructions

For it to work, the user would have to create a sign in a certain area, which will be represented by a black frame, wait two-three seconds without moving or changing the sign, so the program recognizes the sign and then completely remove the hand out of the box. After some time, the color of the frame will turn white and then black, indicating that the user can now create a different sign in the same area. This process repeats until the user decides to close the video by pressing 'q.'


# Code:

The code will be distributed over three python files such that each file will accomplish a different function. The first file, ImageWriter, will allow other files to access the ImageWriter class. The second file, Videocapture, will continuously record a live video of the user making the sign. For this task, I will use the videocapture() feature of the cv2 library. In this file, I will also create a rectangular frame that will indicate the area/box where the user should show the sign. This box will have two phases. Phase 1, is when the frame is completely black and is indicating that the user can make a sign in that area. Once the user makes the sign, he is supposed to hold it for 2-3 seconds and then remove the hand from the frame. After this, the second phase is activated when the frame will turn white for 3 seconds, which indicates that the user can make another sign. This process is repeated until the user is done with the message and wants to exit. Currently, I have not implemented this phase functionality, but I will do so tomorrow. As it is now, the program changes the frames at some fixed time intervals. The third file, ImageProcessing, will analyze each 10th frame captured from VideoCapture. The algorithm works as follows: first, the frame will be cropped to the box dimensions to save time; second, the frame will be converted to grayscale and then directly to black and white; third, I will use vertical segmentation and horizontal segmentation to know the exact position of the sign (startX,endX,startY,endY); fourth, since some of the signs have gaps of black pixels (due to the light) I will use two filling algorithms to compensate for those gaps, and finally, I will split the image into 4 quadrants and calculate the number of black pixels into each quadrant. This result (which will be stored as a 4-valued list) will be sent to a function that will return the letter according to the amount of black pixels in each quadrant.   


For checking my work, each letter will be included in a list. We would have three such list categories: one for punch form letters (such as m or n), one for empty middle letters (such as o or c), and one for finger letters (such as b or d). Currently, I have implemented up to the fifth step, and I will continue working on the rest of the program during the following weeks. 

 
 # Future Plans 
 
 I am also planning on creating a "learning tool" after the code part is done. This tool will help the user learn the sign language by testing him on different letters. The rules are simple: one right letter gives a point. The game will have ten rounds, and once the rounds are over, the user could see his score. 
  
    
