# TROTT
The Robotic Object Tracking Turret

### The final project submission for COSC 4364 developed by:
* Grant Williams
* Tyler Driver
* Sanaz Farhadi
* Sebastian Macedonio

### Project Details:
TROTT will receive an image input within a predetermined frame, identify the object, and once the object is moved and another image frame is received will then move the laser turret to the center of the object's new position.
#### Hardware:
  * 1 x Arduino UNO
  * 1 x Breadboard
  * 3 x AC 100 - 240V to DC 5V 2A Power Adapter
  * 1 x 650nm 6mm 5V 5mW Red Laser Diode
  * 2 x Metal Gearing Servo Motor

The purpose of this project is to showcase concepts from Numerical Methods, those being the following:
* Errors
  * Being able to detect the correct object and ignore noise
  * Only being able to detect objects within the given frame
* Equations
  * Image processing algorithm to detect object (DFT/FFT)
  * Algorithm for translating (x, y) coordinates into degrees for servo rotation
* Optimization
  * Improving the efficiency of the DFT/FFT algorithm
  * Setting interval of image update to be reasonable but not overload Arduino with data

### Instruction to Run the Project:
The following libraries are needed to run this code
Please note that the commands on the left are used to
install the proper libraires and also note that most of these
libraries were installed using anaconda:

link for anaconda:
https://www.anaconda.com/

IMPORTANT: We are using a custom librairy for our FFT/IFFT implementation so that
we could use cython. Inorder for it to work, you must be using Python version 3.6.8
You can change your version with anaconda using the following command:
conda install python=3.6.8

* import sys -  conda install -c anaconda system 
* import numpy as np - conda install -c anaconda numpy
* import cv2 - conda install -c conda-forge opencv
* import pyximport - conda install -c anaconda cython
* import time - conda install -c conda-forge time
* import ctypes - conda install -c conda-forge pywin32-ctypes
* import os - conda install -c jmcmurray os
* import serial - python -m pip install pyserial
* import tkinter - conda install -c anaconda tk

Once you have the necesary libraries installed, cd to the project
directory and run the following command:
python ./tracking_code/main.py

Once the program starts, use the mouse to select the area where the
object will be tracked. After that, drag your mouse over the object
you would like to track. After this, the program will begin active
tracking. 
