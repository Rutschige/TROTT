# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 18:15:07 2019
Instructions: To start we need to know highet and width of the frame and the distance between 
our frame and the camera. When making an instance of this class those values need to passed to
constructor. The next step is to call SetMaxPanAndTilt() function which will find maximum 
movement of the camera from the center to the upper and right most boundries of the frame.
Finally call convertXAndY function and pass in the coordinates of the object to get pan and
tilt for the lazer movement.
@author: Sanaz Farhadi
"""
import math

class Conversion:
    
    FrameWidth     = 0.00
    FrameHeight    = 0.00
    WidthMult      = 0.00
    HeightMult     = 0.00
    CameraDistance = 0.00
    MaxPan         = 0.00  #Maximum Horizontal movement in degrees for one direction
    MaxTilt        = 0.00  #Maximum Vertical movement in degrees for one direction
    
    def __init__(self, width, height, pWidth, pHeight, distance):
        self.FrameWidth      = width
        self.FrameHeight     = height
        self.WidthMult       = width/pWidth
        self.HeightMult      = height/pHeight
        self.CameraDistance  = distance
        
    def SetMaxPanAndTilt(self):
        frameX = self.FrameWidth/2
        frameY = self.FrameHeight/2
        self.MaxPan  = math.degrees(math.atan(frameX/self.CameraDistance))
        self.MaxTilt = math.degrees(math.atan(frameY/self.CameraDistance))
        
    def convertXAndY(self, objX, objY):
        # MaxPan and MaxTilt are multiplied by 2 to get maximum range of movement in both directions
        # Add 90 because the center is (90 deg, 90 deg)
        pan  = ((objX * self.WidthMult) / ( self.FrameWidth  / (2* self.MaxPan) )) + 90
        tilt = ((objY * self.HeightMult) / ( self.FrameHeight / (2* self.MaxTilt))) + 90
        return pan, tilt