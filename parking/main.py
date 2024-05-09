'''
Author: K.Tanjim Ahammad
Date:27.04.2024
Purpose: Real time monitoring a parking lot for available space from a video feed
'''

import cv2  
import pickle 
import cvzone
import numpy as np


#video feed 
cap=cv2.VideoCapture('parking/carPark.mp4')
# size of the rectangle
width, height = 105, 48
fps = cap.get(cv2.CAP_PROP_FPS)
with open('parking/area.pkl', 'rb') as f:
        pos_list = pickle.load(f)

def checkparkingpos(img_pros):
    
    availability=0
    for pos in pos_list:
       x,y=pos
       img_crop=img_pros[y:y+height,x:x+width]
       #cv2.imshow(str('parking_position')+str(x*y),img_crop)
       count=cv2.countNonZero(img_crop)
       cvzone.putTextRect(img,str(count),(x,y+height-3),scale=1.5,thickness=2,offset=0,colorR=(0,0,255))
       if count< 1000:
           color=(0,255,0)
           thickness= 5
           availability+=1
       else:
          color=(0,0,255)
          thickness= 2
       cv2.rectangle(img, pos, (pos[0]+width, pos[1]+height), color, thickness)

    cvzone.putTextRect(img,f'Available spaces:{availability}/{len(pos_list)}',(20,40),scale=1.2,thickness=1,offset=20,colorR=(255,0,0))


while True:

  if cap.get(cv2.CAP_PROP_POS_FRAMES)==cap.get(cv2.CAP_PROP_FRAME_COUNT):
    cap.set(cv2.CAP_PROP_POS_FRAMES,0)
  success, img=cap.read()
  img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  img_blr=cv2.GaussianBlur(img_gray,(3,3),1)
  # convert it to binary
  img_threshold=cv2.adaptiveThreshold(img_blr,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
  img_med=cv2.medianBlur(img_threshold,5)
  kernel=np.ones((3,3),np.uint8)
  img_dilate=cv2.dilate(img_med,kernel,iterations=1)
  checkparkingpos(img_dilate)
  cv2.imshow('Real Time Parking Monitoring',img)
  #cv2.imshow('blur',img_dilate)
  cv2.waitKey(10)