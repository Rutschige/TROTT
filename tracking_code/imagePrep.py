import numpy as np
import math
import CropEditor
import cv2
def getIndex(pixel, regions):
        for region in regions:
            if pixel in region:
                return regions.index(region)
        return -1

def getCenter(originalImage): #Finds circular blobs in the image and returns the center of the largest one
    location,image = CropEditor.Crop().crop(originalImage)
    regions = []
    up = -1
    for index, pixel in np.ndenumerate(image):
        left = -1
        if pixel == 0:
            if(index[1]-1) >= 0:
                left = getIndex((index[0],index[1]-1), regions)
            if(index[0]-1) >= 0:
                up = getIndex((index[0]-1,index[1]), regions)
            if(left > -1) and (up > -1) and (left != up):
                regions[left] += regions[up]
                regions[left].append(index)
                del(regions[up])
            elif left > -1:
                regions[left].append(index)
            elif up > -1:
                regions[up].append(index)
            else:
                regions.append([index])
    
    maxReg = regions[0]
    for region in regions:
        if len(region) > len(maxReg):    
            maxReg = region           
    center = (0,0)
    for point in maxReg:
        center = (center[0] + point[0] , center[1] + point[1])
    center = (center[0]+.5, center[1]+.5)
    center = (int(center[0]/len(maxReg)), int(center[1]/len(maxReg)))
    center = (center[0]+location[0][0], center[1]+location[1][0])

    return center

def getNumOfZero(num): #gets the number of zeros needed for zero padding
    ans = math.log(num,2)
    
    if ans > int(ans):
        ans = int(ans)+1
    ans = (2 ** ans) - num
    return int(ans)

def padImage(image): #returns a 255 padded version of the image so that its # of pixels is a power of two which is needed for fft
    ypad = getNumOfZero(image.shape[0])
    xpad = getNumOfZero(image.shape[1])
    return np.pad(image, ((0,int(ypad)),(0,int(xpad))), 'constant', constant_values=255)

def getFrame(image):
    bounds = CropEditor.Crop().crop(image)[0]
    return bounds
def resizeImage(image, bounds):
    image = image[bounds[0][0] : bounds[0][1] , bounds[1][0] : bounds[1][1]]
    return padImage(image)

