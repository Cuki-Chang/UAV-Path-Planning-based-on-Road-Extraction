# cannot traverse/black = values below "[5, 5, 5]"
# can traverse/white = values above "[250, 250, 250]" 

import time
import cv2
import csv
import json 
from find_path_alg import find_path_alg
from find import find

t1=time.perf_counter()

# global variables
flag = 0

img = cv2.imread("RS/satgreen.png")
#img = cv2.imread("2MASK -V.png")

#img = cv2.imread("3mask-V.png")
#img = cv2.imread("3mask.png")

#img = cv2.imread("3 road mask.png")
#img = cv2.imread("70933_maskW.png")
#img = cv2.imread("70933_mask.png")

#print(img.shape)

width = int
height = int
x = int
y = int
window_name = "path finding"
starting_position = list()
ending_position = list()
path_color = (0, 0, 255)

def main():

    global img
    global width, height
    global window_name
    
    dimensions = img.shape
    height = dimensions[0]
    width = dimensions[1]


    # displaying the image in a window for a user to choose a starting position
    print("Choose a valid starting position (white pixel) by double left clicking on the image.")
    print("Click any key to exit out of this program at any time.\n")

    cv2.imshow(window_name, img)
    cv2.setMouseCallback(window_name, mouse_events)
    cv2.waitKey(0)

def mouse_events(event, x, y, flags, param):
    global flag

    global img
    global starting_position, ending_position
    global path_color

    if event == cv2.EVENT_LBUTTONDBLCLK:
        # need to check if rgb values correspond to the color white
        r = img[y][x][0]
        g = img[y][x][1]
        b = img[y][x][2]
        color_flag = 0
        if r >= 250 and g >= 250 and b >= 250:
            color_flag = 1
        if  r < 10 and g > 220 and b < 10:
                color_flag = 1
        else:
            print("You have chosen an invalid position. Choose a valid one.")

        # getting starting position
        if flag == 0 and color_flag == 1:
            cv2.imshow(window_name, img)
            print("The starting position you chose was: (%d, %d)" % (x, y))
            starting_position.append(x)
            starting_position.append(y)
            flag += 1
        # getting ending position
        elif flag == 1 and color_flag == 1:
            cv2.imshow(window_name, img)
            print("The ending position you chose was: (%d, %d)" % (x, y))
            ending_position.append(x)
            ending_position.append(y)

            # calling function to find path
            find_path()
            flag += 1
            
def find_path( ):
    global img
    global width, height
    global x, y
    global starting_position, ending_position
    global path_color



    #find_path_alg(img,width, height, starting_position, ending_position, path_color)
    find(img,width, height, starting_position, ending_position, path_color)


    # calling function to save the new image
    save_file()

def save_file():
    global img
    # writing the final image as user inputted filename
    filename = input("\nEnter a filename for the image to save as: ")
    try:
        cv2.imwrite(filename, img)
    except:
        print("The filename you entered is invalid. Exiting program.")
        exit()

    print("The image was successfully saved. Exiting program.")
    exit()
    

if __name__ == "__main__":

    main()

