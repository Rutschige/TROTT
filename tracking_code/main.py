import sys
import numpy as np
import cv2
import pyximport
import time 
import ctypes
import os
import serial

import transforms #this is my custom transforms library, look in cython_stuff/transforms.pyx for the details.
import CropEditor
import imagePrep
import Conversion

pyximport.install()
np.set_printoptions(threshold=sys.maxsize)



def getImage(cap):
    baseDir = os.path.dirname(__file__) #lets us open files from current directory
    location = os.path.join(baseDir, "ball-gif/" +str((cap%8)+1) + ".png")
    frame = cv2.imread(location, 0)
    
    return frame


#Im currently using tracker as the main loop. IDK how our structure is gona be in the end
def tracker(scaler = 1): #scaler works best with powers of 2
    cap = 0
    originalBall = getImage(cap)
    
    bounds = imagePrep.getFrame(originalBall)

    conversion =Conversion.Conversion(15.0, 12.5, bounds[1][0] - bounds[1][1],bounds[0][0] - bounds[0][1], 13)

    conversion.SetMaxPanAndTilt()

    originalBall = imagePrep.resizeImage(originalBall, bounds)
    center = imagePrep.getCenter(originalBall) #finds the initial location of the object you want to track
    originalDft = transforms.forward_transform(originalBall[::scaler,::scaler].astype(np.complex_)) #computes the dft and scales the image down to desierd size
    cv2.imshow("Initial DFT", cv2.resize(originalDft.real, (0,0), fx=scaler, fy=scaler))
    


    running=True
    while running:
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False

        changeBall = getImage(cap)
        changeBall = imagePrep.resizeImage(changeBall, bounds)
        start = time.time()
        
        changeDft = transforms.forward_transform(changeBall[::scaler,::scaler].astype(np.complex_))
        
        cv2.imshow("New DFT", cv2.resize(changeDft.real, (0,0), fx=scaler, fy=scaler))

        locDft = changeDft * originalDft / abs(changeDft * originalDft) 

        cv2.imshow("Combined DFT", cv2.resize(locDft.real, (0,0), fx=scaler, fy=scaler))

        location = transforms.inverse_transform(locDft).real

        

        end = time.time()
        temp = np.where(location == np.amax(location))
        
        cent = ((temp[0]*scaler)-center[0], (temp[1]*scaler)-center[1])

        pan, tilt = conversion.getDegrees(cent[0], cent[1])
        print("Pan: ", pan, " Tilt: ", tilt)
        
        print(bounds)
        for y in range(0,6):
            for x in range(0,6):
                changeBall[(cent[0]+y, cent[1])] = 255
                changeBall[(cent[0]-y, cent[1])] = 255
                changeBall[(cent[0], cent[1]+x)] = 255
                changeBall[(cent[0], cent[1]-x)] = 255

        print("Center: ",temp[1], ",", temp[0], "\nTime: ", end-start)

        cv2.imshow('Location', changeBall)
        
        cv2.waitKey(100)
        cap+=1

    cv2.destroyAllWindows()

tracker(16)