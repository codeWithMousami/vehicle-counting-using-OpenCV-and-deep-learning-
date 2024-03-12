import cv2
import numpy as np

# Web camera
cap = cv2.VideoCapture('video.mp4')

min_width_rect = 80 # minimum width rectangle
min_height_rect = 80 # minimum height rectangle

count_line_position =550

# Initialize background subtractor
algo = cv2.createBackgroundSubtractorMOG2()

def center_handle(x,y,w,h):
    x1=int(w/2)
    y1= int(h/2)
    cx =x+x1
    cy =y +y1
    return cx,cy

detect = []
offset = 6 #allowable error between pixel
counter = 0

while True:
    ret, frame1 = cap.read()

    # Convert the frame to grayscale
    grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

    # Applying Gaussian blur to reduce noise
    blur = cv2.GaussianBlur(grey, (3, 3), 5)

    # Applying background subtraction on each frame
    img_sub = algo.apply(blur)

    # Dilate the resulting image to enhance the foreground objects
    dilat = cv2.dilate(img_sub, np.ones((5, 5)))

    # Closing operation to fill holes in foreground objects
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
    dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernel)

    # Find contours in the dilated image
    contourshape,h = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on the original frame (if needed)
    
    #cv2.imshow('Dectertor',dilatada)



    cv2.line(frame1,(25,count_line_position),(1200,count_line_position),(255,127,0),3)

    #To draw rectengle in vehicle
    for (i,c) in enumerate(contourshape):
        (x,y,w,h)= cv2.boundingRect(c)
        validate_counter = (w>= min_width_rect) and (h>=min_height_rect)
        if not validate_counter:
            continue

        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,255),2)
        cv2.putText(frame1,'VEHICLE :'+str(counter),(x,y-20),cv2.FONT_HERSHEY_DUPLEX,1,(255,0,255),2)        

        
        center = center_handle(x,y,w,h)
        detect.append(center)
        cv2.circle(frame1,center,4,(0,255,0),-1)

        for (x,y) in detect:
            if y<(count_line_position+offset) and y>(count_line_position-offset):
                counter+=1
                cv2.line(frame1,(25,count_line_position),(1200,count_line_position),(0,127,255),3)
                detect.remove((x,y))   
                print('Vehicle Counter :'+str(counter)) 

    cv2.putText(frame1,'VEHICLE COUNTER :'+str(counter),(450,70),cv2.FONT_HERSHEY_DUPLEX,2,(0,0,255),2)        

    # Display the result
    cv2.imshow('Video Original', frame1)

    if cv2.waitKey(1) == 13:
        break

cv2.destroyAllWindows()
cap.release()
