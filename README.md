# Sign-Language-Decoder---15-112-Term-Project

This program will decypher the sign language into normal text. 

# Instructions

For it to work, the user would have to create a sign in a certain area, which will be represented by a black frame, wait two-three seconds without moving or changing the sign, so the program recognizes the sign and then completely remove the hand out of the box. After some time, the color of the frame will turn white and then black, indicating that the user can now create a different sign in the same area. This process repeats until the user decides to close the video by pressing 'q.'

Also, the program will have a learning tool in form of a game, which will test how well does the user know the signs. The user will have to make a given sign inside the box and then press 's' in order to submit the picture. Then the frame will either turn black, indicating a wrong sign, or white, indicating a correct answer. The user can make signs and send them until he presses 'q' and exits.

# Code:

The code will be distributed over four python files such that each file will accomplish a different function. The first file, ImageWriter, will allow other files to access the ImageWriter class. The second file, Videocapture, will continuously record a live video of the user making the sign. For this task, I will use the videocapture() feature of the cv2 library. In this file, I will also create a rectangular frame that will indicate the area/box where the user should show the sign. After 3-4 seconds a picture will be automatically sent to the ImageProcessing file which will decode the character. Should the user send an empty frame, the frame will turn white, indicating that the user should remake the sign. The third file, ImageProcessing, will analyze each 10th frame captured from VideoCapture. The algorithm works as follows: first, the frame will be cropped to the box dimensions to save time; second, the frame will be converted to grayscale and then directly to black and white; third, I will use vertical segmentation and horizontal segmentation to know the exact position of the sign (startX,endX,startY,endY); fourth, since some of the signs have gaps of black pixels (due to the light) I will use two filling algorithms to compensate for those gaps, and finally, I will split the image into 4 quadrants and calculate the number of black pixels into each quadrant. This result (which will be stored as a 4-valued list) will be sent to a function that will return the letter according to the amount of black pixels in each quadrant. The fourth file is just a Graphical Interface for the User. When the fourth file is run three button will appear indicating the part of the program that will run. Each clicked button will raise a pop up that will contain the instructions of that section. Should the user close the pop up, the program will run either the translator or the learning tool.


For checking some of the letters which are very similar, such as A or N, I will have separate functions which will look at little differences between the characters in order to increase the accuracy of the program. I am planning on creating 3 such functions, one for A,N,T, one for R and U, and one for E and M/S.

 
 # Future Plans 
 
Improve the GUI of the program by adding a score functionality that will remeber the score after each round and add it into a "My Scores" widget.
Improve the accuracy of the program by creating several more separate functions.
Create a 10 round feature for the game.
    
