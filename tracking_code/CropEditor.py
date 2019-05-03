
# coding: utf-8

# In[ ]:

import tkinter.messagebox

import cv2
import numpy as np

def messageBox(): 
	"""
	function displays box and asks if the user wishes to continue with there currently cropped image
	returns true if the user wishes to continue, else false
	"""
	root = tkinter.Tk()
	root.withdraw()
	answer = tkinter.messagebox.askquestion("Image-Crop", "Continue?")
	if answer == "no":
		return False
	else:
		return True


class Crop():
	def __init__(self):
		self.roi=[0,0,0,0] 
		self.selection=False 

	roi = []

	# Mouse Callback for ROI selection
	# event: The event that took place (left mouse button pressed, left mouse button released, mouse movement, etc).
	# x: The x-coordinate of the event.
	# y: The y-coordinate of the event.
	# flags: Any relevant flags passed by OpenCV.
	# params: Any extra parameters supplied by OpenCV.
	def roi_selection(self,event, x, y, flags, param):
		#Refernce to the global variables
		#On Left mouse button click records roi with mouse selection status to True
		if event == cv2.EVENT_LBUTTONDOWN:
			self.selection = True
			self.roi = [x, y, x, y]
		#On Mouse movement records roi with mouse selection status to True
		elif event == cv2.EVENT_MOUSEMOVE:
			if self.selection == True:
				self.roi[2] = x
				self.roi[3] = y			

		#If Left mouse button is released changes mouse selection status to False
		elif event == cv2.EVENT_LBUTTONUP:
			self.selection = False
			self.roi[2] = x
			self.roi[3] = y


	def crop(self,input_img):
		#Original Image Window Name
		window_name='Input Image'

		#Cropped Image Window Name
		window_crop_name='Cropped Image'

		#Escape ASCII Keycode
		esc_keycode=27

		#Time to waitfor
		wait_time=1
		
		# Make a copy of original image for cropping
		clone = input_img.copy()
		#Create a Window
		#cv2.WINDOW_NORMAL = Enables window to resize.
		#cv2.WINDOW_AUTOSIZE = Default flag. Auto resizes window size to fit an image.
		cv2.namedWindow(window_name,cv2.WINDOW_AUTOSIZE)
		#Set mouse handler for Window with roi_selection function callback
		cv2.setMouseCallback(window_name, self.roi_selection)
		#Loop 
		while True:
			#Show original image in window
			cv2.imshow(window_name,input_img)
			#if roi has all parameters filled
			if len(self.roi) == 4:
				#Make a copy of orginal image before drawing rectangle on it
				input_img = clone.copy()
				#Check if any pixl coorinalte is negative and make it zero
				self.roi = [0 if i < 0 else i for i in self.roi]
				#Draw rectangle on input_img
				#input_image: source image
				#(roi[0], roi[1]): Vertex of the rectangle
				#(roi[2], roi[3]): Opposite Vertex of the rectangle
				#(0, 255, 0): Rectangular Color
				# 2: Thickness
				cv2.rectangle(input_img, (self.roi[0],self.roi[1]), (self.roi[2],self.roi[3]), (0, 255, 0), 2)	
				#Make x and y coordiates for cropping in ascending order
				#if x1 = 200,x2= 10 make x1=10,x2=200
				if self.roi[0] > self.roi[2]:
					x1 = self.roi[2]
					x2 = self.roi[0]
				#else keep it as it is	
				else:
					x1 = self.roi[0]
					x2 = self.roi[2]
				#if y1 = 200,y2= 10 make y1=10,y2=200 	
				if self.roi[1] > self.roi[3]:
					y1 = self.roi[3]
					y2 = self.roi[1]
				#else keep it as it is	
				else:
					y1 = self.roi[1]
					y2 = self.roi[3]	
					
				#Crop clone image
				crop_img = clone[y1 : y2 , x1 : x2]
				#check if crop_img is not empty
				if crop_img.size and not self.selection:
					#Create a cropped image Window
					cv2.namedWindow(window_crop_name,cv2.WINDOW_AUTOSIZE)
					#Show image in window
					cv2.imshow(window_crop_name,crop_img)
					if messageBox():
						cv2.destroyAllWindows()
						return ((y1,y2),(x1,x2)), crop_img
					else:
						self.roi=[]
						
					
				
			
			#Check if any key is pressed
			k = cv2.waitKey(wait_time)
			#Check if ESC key is pressed. ASCII Keycode of ESC=27
			if k == esc_keycode:  
				#Destroy All Windows
				cv2.destroyAllWindows()
				break

