# -*- coding: utf-8 -*-
"""
Created on Thu May  2 18:37:26 2019
Explanation: The python program below, reads the stream of incoming frames from the camera and 
updates the image with a new frame every 2 seconds. Resource used:
https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_image_display/py_image_display.html
@author: sanaz
"""

import cv2
from time import sleep

cap = cv2.VideoCapture(0)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    cv2.imwrite("frame%d.jpg", gray)     # save frame as JPEG file
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    sleep(2)
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()