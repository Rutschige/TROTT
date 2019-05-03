import sys
import numpy as np
import cv2
import pyximport
import time 
import ctypes
import os

import transforms #this is my custom transforms library, look in cython_stuff/transforms.pyx for the details.
import CropEditor
import imagePrep

pyximport.install()
np.set_printoptions(threshold=sys.maxsize)

#Im currently using tracker as the main loop. IDK how our structure is gona be in the end
def tracker(scaler = 1): #scaler works best with powers of 2
    baseDir = os.path.dirname(__file__) #lets us open files from current directory
    originalBall = cv2.imread(os.path.join(baseDir,"ball-gif/1.png"),0)
    #CropEditor.Crop().crop(originalBall) 
    center = imagePrep.getCenter(originalBall) #finds the initial location of the object you want to track

    originalDft = transforms.forward_transform(imagePrep.padImage(cv2.resize(originalBall, (0,0), fx = (1/scaler), fy = (1/scaler)).astype(np.complex))) #computes the dft and scales the image down to desierd size

    for i in range(1, 8):
        
        changeBall = cv2.imread(os.path.join(baseDir,"ball-gif/"+ str(i+1) +".png"),0)
        start = time.time()
        
        changeDft = transforms.forward_transform(imagePrep.padImage(cv2.resize(changeBall, (0,0), fx = (1/scaler), fy = (1/scaler)).astype(np.complex)))
        
        locDft = changeDft * originalDft / abs(changeDft * originalDft) 

        location = transforms.inverse_transform(locDft).real
        end = time.time()
        temp = np.where(location == np.amax(location))
        
        cent = ((temp[0]*scaler)-center[0], (temp[1]*scaler)-center[1])

        for y in range(0,6):
            for x in range(0,6):
                changeBall[(cent[0]+y, cent[1])] = 255
                changeBall[(cent[0]-y, cent[1])] = 255
                changeBall[(cent[0], cent[1]+x)] = 255
                changeBall[(cent[0], cent[1]-x)] = 255

        print("Center: ",temp[1], ",", temp[0], "\nTime: ", end-start)

        cv2.imshow('Location', changeBall)
        
        cv2.waitKey(1)

    cv2.destroyAllWindows()

tracker(4)