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
    # Capture frame-by-frame
    frame = cap.read()[1]

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    return gray


#Im currently using tracker as the main loop. IDK how our structure is gona be in the end
def tracker(scaler = 1): #scaler works best with powers of 2
    arduino = serial.Serial('COM3', 9600)
    cap = cv2.VideoCapture(0) 

    calibration=True
    while calibration:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            calibration = False
        cv2.imshow("Calibration",getImage(cap))
    cv2.destroyAllWindows()
    arduino.write(bytes(b"stop"))
    
    baseDir = os.path.dirname(__file__) #lets us open files from current directory
    originalBall = getImage(cap)
    #CropEditor.Crop().crop(originalBall) 
    bounds = imagePrep.getFrame(originalBall)

    conversion =Conversion.Conversion

    conversion(conversion,bounds[0],bounds[1])

    conversion.SetMaxPanAndTilt(conversion)

    originalBall = imagePrep.resizeImage(originalBall, bounds)
    center = imagePrep.getCenter(originalBall) #finds the initial location of the object you want to track
    originalDft = transforms.forward_transform(originalBall[::scaler,::scaler].astype(np.complex_)) #computes the dft and scales the image down to desierd size

    


    running=True
    while running:
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False

        changeBall = getImage(cap)
        changeBall = imagePrep.resizeImage(changeBall, bounds)
        start = time.time()
        
        changeDft = transforms.forward_transform(changeBall[::scaler,::scaler].astype(np.complex_))
        
        locDft = changeDft * originalDft / abs(changeDft * originalDft) 

        location = transforms.inverse_transform(locDft).real
        end = time.time()
        temp = np.where(location == np.amax(location))
        
        cent = ((temp[0]*scaler)-center[0], (temp[1]*scaler)-center[1])

        pan,tilt=conversion.convertXAndY(conversion, cent[1],cent[2])
        
        arduino.write(bytes(str(pan)))
        arduino.write(bytes(str(tilt)))
        print("ArduinoData:", arduino.read_all)
        print(bounds)
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

tracker(16)