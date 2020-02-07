#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 13:51:13 2019

@author: Aashay Tinaikar, Graduate student, TU Munich
"""

import os
import numpy as np
import pydicom
import glob
import cv2
from matplotlib import pyplot as plt
from pynput import keyboard
from PIL import ImageFont, ImageDraw, Image
import tkinter

# mouse callback function
def mouse_response(event, x, y, flags, param):
    global t_step, slice_no, pointer, stepsTotal, sliceNoTotal, refPt
    if event == cv2.EVENT_LBUTTONDBLCLK:
        img = cropped_images_Cine[:,:,:,t_step%stepsTotal, slice_no%sliceNoTotal].astype(np.uint8)
        cv2.circle(img, (x,y), 1, (255,0,0), -1)
        #label_text(img, index, x, y)
        cropped_images_Cine[:,:,:,t_step%stepsTotal, slice_no%sliceNoTotal] = img.astype(np.float64)
        X[pointer[t_step%stepsTotal,0, slice_no%sliceNoTotal], t_step%stepsTotal, slice_no%sliceNoTotal] = x + refPt[0][0]
        Y[pointer[t_step%stepsTotal,0, slice_no%sliceNoTotal], t_step%stepsTotal, slice_no%sliceNoTotal] = y + refPt[0][1]
        
        pointer[t_step%stepsTotal,0,slice_no%sliceNoTotal] += 1 
        
    elif event == cv2.EVENT_RBUTTONDBLCLK:
        t_step += 1
        plt.title('Image details: Image slice_no = ' + np.str(slice_no%sliceNoTotal) + ' and t_step = ' + np.str(t_step%stepsTotal) )
        plt.draw()
              
    elif event == cv2.EVENT_MBUTTONDBLCLK :
        t_step -=1
        plt.title('Image details: Image slice_no = ' + np.str(slice_no%sliceNoTotal) + ' and t_step = ' + np.str(t_step%stepsTotal) )
        plt.draw()
        
def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables
    global refPt, cropping, t_step, slice_no, sliceNoTotal, stepsTotal
    img = images_Cine[:,:,:,t_step%stepsTotal,slice_no%sliceNoTotal].astype(np.uint8)
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True
 
	# check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x, y))
        cropping = False
        # record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		
        # draw a rectangle around the region of interest
        cv2.rectangle(img, refPt[0], refPt[1], (255, 255, 255), 1)
        images_Cine[:,:,:,t_step%stepsTotal,slice_no%sliceNoTotal] = img.astype(np.float64)
        #cv2.imshow("ROISelection", img)

def segmentation_routine(event, x, y, flags, param):
    global t_step, slice_no, X_cent, Y_cent, sliceNoTotal, stepsTotal
    global n
    if event == cv2.EVENT_LBUTTONDBLCLK:
        img = cropped_images_Cine_seg[:,:,:,t_step%stepsTotal, slice_no%sliceNoTotal].astype(np.uint8)
        if n <=6:            
            cv2.circle(img, (x,y), 1, (255,0,0), -1)
            if n == 0:
                X_cent[slice_no] = x
                Y_cent[slice_no] = y
            else:
                X_segment[n-1, slice_no] = x
                Y_segment[n-1, slice_no] = y
                                        
        cropped_images_Cine_seg[:,:,:,t_step%stepsTotal, slice_no%sliceNoTotal] = img.astype(np.float64)
        n = n + 1
        
    elif event == cv2.EVENT_RBUTTONDBLCLK:
        t_step += 1
        plt.title('Image details: Image slice_no = ' + np.str(slice_no%sliceNoTotal) + ' and t_step = ' + np.str(t_step%stepsTotal) )
        plt.draw()
              
    elif event == cv2.EVENT_MBUTTONDBLCLK :
        t_step -=1
        plt.title('Image details: Image slice_no = ' + np.str(slice_no%sliceNoTotal) + ' and t_step = ' + np.str(t_step%stepsTotal) )
        plt.draw()

def drawSegments(image_series, X_c, Y_c, X, Y):
    global sliceNoTotal, stepsTotal
    for j in range (0, sliceNoTotal):
        for i in range (0,stepsTotal):
            img = image_series[:,:,:,i%stepsTotal,j%sliceNoTotal].astype(np.uint8)
            for n in range (0,6):
                if X[n,j] != 0:
                    cv2.line(img,(X_c[j],Y_c[j]),(X[n,j].astype(np.int),Y[n,j].astype(np.int)),(255,255,255),1)
            image_series[:,:,:,i%stepsTotal, j%sliceNoTotal] = img.astype(np.float64)
    return image_series    
        

def label_images(img_series, sliceTotal, stepsTotal):
    
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (5,5)
    fontScale              = 0.2
    fontColor              = (0,255,0)
    lineType               = 1
    
    for i in range(0,sliceTotal):
        for j in range(0, stepsTotal):
            content = 'Image_slice = ' + np.str(slice_no + 1) + " and t_step = " + np.str(t_step + 1)
            img = img_series[:,:,:,j, slice_no].astype(np.float64)
            cv2.putText(img,content, bottomLeftCornerOfText, font, fontScale,
                            fontColor, lineType)
            img_series[:,:,:,j, slice_no] = img.astype(np.uint8)
    #if key == keyboard.Key.backspace:
    #    t_step-=1
    
def show_coords(event, x, y, flags, param):
    print("Inside show_coords")
    for index in range (0, 30) :
        tkinter.Label(window, text = X[index]).grid(row = index+1, column = 1)
        tkinter.Label(window, text = Y[index]).grid(row = index+1, column = 2)
        
from PIL import Image as PImage

def loadImages(path):
    
    os.chdir(path)
    sliceList = glob.glob('*_tf2d18_retro_iPAT_*/')
    os.chdir('../../')
    sliceList = sorted(sliceList)
    sliceNoTotal = len(sliceList)
    t_StepsTotal = 25
    
    
    imagesList = os.listdir(path + sliceList[0] +'png/')
    imagesList = sorted(imagesList)
    test_img = cv2.imread(path + sliceList[0] +'png/' + imagesList[1])
    rows = np.shape(test_img)[0]
    cols = np.shape(test_img)[1]
    channels = np.shape(test_img)[2]
    Images = np.zeros((rows,cols,channels,t_StepsTotal, sliceNoTotal))
    
    for j in range(0,sliceNoTotal):
        
        # return array of images
        imagesList = os.listdir(path + sliceList[j] +'png/')
        imagesList = sorted(imagesList)
        test_img = cv2.imread(path + sliceList[0] +'png/' + imagesList[1])
        
        rows = np.shape(test_img)[0]
        cols = np.shape(test_img)[1]
        channels = np.shape(test_img)[2]
        
        if j == 0:
            Images = np.zeros((rows,cols,channels,t_StepsTotal, sliceNoTotal))
        
        if t_StepsTotal != np.size(imagesList):
                print ('Number of images in cine sequence are not equal to 25')
                
        i = 0
        for image in imagesList:
            #img = PImage.open(path + image)
            #Images.append(img)
            Images[:,:,:,i,j] = cv2.imread(path + sliceList[j] +'png/' + image)
            i+=1
    return Images, rows, cols, channels, sliceNoTotal

#=============================================================================
#Initialization
#=============================================================================

#Specify the folder path of one particular patient 
path = "./cineMRIFreiburg/20130328_143002_SymphonyTim_Freiburg_LQT_Kinder_TPM/"

#Load your images in an array
#loadImages command is case specific command which will arrange x-y-z-cine-slices 
#in a proper 5-D matrix which enables us to easily handle it
[images_Cine, rows, cols, channels, sliceNoTotal] = loadImages(path)    

key  = 0
X = np.zeros((30,25,sliceNoTotal))
Y = np.zeros((30,25,sliceNoTotal))
pointer = np.zeros((25,1,sliceNoTotal)).astype(np.int)
X_cent = np.zeros((sliceNoTotal,1)).astype(int)
Y_cent = np.zeros((sliceNoTotal,1)).astype(int)
index = 0
t_step = 0
slice_no = 0
stepsTotal = 25
n = 0
X_segment = np.zeros((6,sliceNoTotal))
Y_segment = np.zeros((6,sliceNoTotal))

blank_images = np.zeros((rows, cols, channels)).astype(np.uint8)
label_img = np.zeros((1,100))

#window = tkinter.Tk()
#window.title("Image Labels")

#============================================================================
#   For loading existing settings
#============================================================================
import xlrd
settings = xlrd.open_workbook(path + 'ManualTracking_results1/Preliminary_settings.xls')
ROIval = settings.sheet_by_name("Pan Coordinates")
Points = [(int(ROIval.cell_value(1,1)), int(ROIval.cell_value(1,2)))]
Points.append((int(ROIval.cell_value(2,1)), int(ROIval.cell_value(2,2))))

CentXY = settings.sheet_by_name("Centre Coordinates")
CentX = np.zeros((sliceNoTotal,1)).astype(int)
CentY = np.zeros((sliceNoTotal,1)).astype(int)

for i in range(0,12):
    CentX[i] = int(CentXY.cell_value(i+1,1)) - Points[0][0]
    CentY[i] = int(CentXY.cell_value(i+1,2)) - Points[0][1]
    
SegVals = settings.sheet_by_name("Segmentation Coordinates")
SegX = np.zeros((6,sliceNoTotal))
SegY = np.zeros((6,sliceNoTotal))

for i in range(0,6):
    for j in range (0, sliceNoTotal):
        SegX[i,j] = (float(SegVals.cell_value(i+2, 5*j + 1 )) - Points[0][0])
        SegY[i,j] = (float(SegVals.cell_value(i+2, 5*j + 2 )) - Points[0][1])
#=============================================================================
#   Selection of Field of view
#=============================================================================
refPt = []
cropping = False

#Loading the settings
refPt = Points 

#For manual selection of ROI
#cv2.namedWindow('ROISelection', cv2.WINDOW_NORMAL)
#cv2.setMouseCallback('ROISelection', click_and_crop)
#
## keep looping until the 'q' key is pressed
#while(1):
#    cv2.resizeWindow('ROISelection', 800, 800)
#    cv2.imshow('ROISelection', images_Cine[:, :, :, (t_step%stepsTotal), (slice_no%sliceNoTotal)].astype(np.uint8))
#    key = (cv2.waitKey(1) & 0xFF)
#    if key == ord("c"):
#        break
#cv2.destroyAllWindows()
#-----------------------------------------------------------------------------
 
if len(refPt) == 2:
    cropped_images_Cine = images_Cine[refPt[0][1]:refPt[1][1], 
                           refPt[0][0]:refPt[1][0], :, :, :]
    cv2.namedWindow('Cropped Image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Cropped Image', 800, 800)
    cv2.imshow('Cropped Image', cropped_images_Cine[:,:,:, (t_step%stepsTotal), (slice_no%sliceNoTotal)].astype(np.uint8))
    cv2.waitKey(0)
cv2.destroyAllWindows()

#=============================================================================
#   Myocardium Segmentation
#=============================================================================
Figure = plt.imshow(label_img, shape=(1,100))
plt.axis('off')
plt.title('Image details: Image slice_no = ' + np.str(slice_no%sliceNoTotal) + ' and t_step = ' + np.str(t_step%stepsTotal) )

cropped_images_Cine_seg = cropped_images_Cine.copy()

#For Loaded settings
X_cent = CentX
Y_cent = CentY
X_segment = SegX
Y_segment = SegY


#For manual segmentation
#cv2.namedWindow('Segmentation', cv2.WINDOW_NORMAL)
#cv2.setMouseCallback('Segmentation', segmentation_routine)
#slice_no = 0
#t_step = 0
#while(1): 
#    
#    #plt.title('Image details: Image index = ' + np.str(indexc) + ' and t_step = ' + np.str(t_step) )
#    #plt.draw()
#    cv2.resizeWindow('Segmentation', 800, 800)
#    cv2.imshow('Segmentation', cropped_images_Cine_seg[:,:,:,(t_step%stepsTotal), (slice_no%sliceNoTotal)].astype(np.uint8))
#    
#    key = cv2.waitKey(1)
#    if key & 0xFF == 82 :
#        slice_no+=1
#        n=0
#        plt.title('Image details: Image slice_no = ' + np.str(slice_no%sliceNoTotal) + ' and t_step = ' + np.str(t_step%stepsTotal) )
#        plt.draw()
#        
#    #if key & 0xFF == 84 :
#    #    slice_no-=1
#    #    plt.title('Image details: Image slice_no = ' + np.str(slice_no%sliceNoTotal) + ' and t_step = ' + np.str(t_step%stepsTotal) )
#    #    plt.draw()
#    
#    if key & 0xFF == 27 :
#        break
#cv2.destroyAllWindows()
#-----------------------------------------------------------------------------


cropped_images_Cine = drawSegments(cropped_images_Cine, X_cent, Y_cent, X_segment, Y_segment)
cropped_images_Cine_default = cropped_images_Cine.copy()
#=============================================================================
#   Myocardicum tracking 
#=============================================================================
cv2.namedWindow('CineMyocardiumTracking', cv2.WINDOW_NORMAL)
cv2.namedWindow('Previous window', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('CineMyocardiumTracking', mouse_response)
slice_no = 0
t_step = 0
plt.title('Image details: Image slice_no = ' + np.str(slice_no%sliceNoTotal) + ' and t_step = ' + np.str(t_step%stepsTotal))

while(1):
    
    #content = 'Image_slice = ' + np.str(slice_no + 1) + " and t_step = " + np.str(t_step + 1)
    #tkinter.Label(window, text = content, font=('Times', '18'), fg='blue')
    #for i in range(0,1):
    #    window.mainloop()
    
    cv2.resizeWindow('Previous window', 600, 600)
    if  t_step%stepsTotal == 0:
         cv2.imshow('Previous window', blank_images)         
    else: 
         cv2.imshow('Previous window', cropped_images_Cine[:,:,:,((t_step-1)%stepsTotal), (slice_no%sliceNoTotal)].astype(np.uint8))
    
    cv2.resizeWindow('CineMyocardiumTracking', 600, 600)
    cv2.imshow('CineMyocardiumTracking', cropped_images_Cine[:,:,:,(t_step%stepsTotal), (slice_no%sliceNoTotal)].astype(np.uint8)) 
    #with keyboard.Listener(on_press=on_press) as listener:
    #    listener.join()
    key = cv2.waitKey(1)
    if key & 0xFF == 82 :
        slice_no+=1
        plt.title('Image details: Image slice_no = ' + np.str(slice_no%sliceNoTotal) + ' and t_step = ' + np.str(t_step%stepsTotal) )
        plt.draw()
        
    if key & 0xFF == 84 :
        slice_no-=1
        plt.title('Image details: Image slice_no = ' + np.str(slice_no%sliceNoTotal) + ' and t_step = ' + np.str(t_step%stepsTotal) )
        plt.draw()
    
    if key & 0xFF == 8 :
        cropped_images_Cine[:,:,:,(t_step%stepsTotal), (slice_no%sliceNoTotal)] = cropped_images_Cine_default[:,:,:,(t_step%stepsTotal), (slice_no%sliceNoTotal)]
        X[:, t_step%stepsTotal, slice_no%sliceNoTotal] = 0
        Y[:, t_step%stepsTotal, slice_no%sliceNoTotal] = 0
        pointer[t_step%stepsTotal,0,slice_no%sliceNoTotal] = 0
        
    if key & 0xFF == 27 :
        break
cv2.destroyAllWindows()
plt.close()
#cv2.setMouseCallback("Point Co-ordinates", show_coords)
#show_coords()

#=============================================================================
#   Saving the co-ordinates
#=============================================================================
import xlwt

os.chdir(path)
make_dir = "mkdir ManualTracking_results2"
os.system(make_dir)
os.chdir('./ManualTracking_results2')

Preliminary_settings = xlwt.Workbook(encoding="utf-8")

#Sheet 1: Pan ROI
sheet1 = Preliminary_settings.add_sheet("Pan Coordinates")
sheet1.write(0,0, 'Point number')
sheet1.write(0,1, 'X')
sheet1.write(0,2, 'Y')

for i in range(0,2):
    sheet1.write(i+1,0,str(i+1))
    sheet1.write(i+1,1,str(refPt[i][0]))
    sheet1.write(i+1,2,str(refPt[i][1]))

#Sheet 2: Centre co-ordinates
sheet2 = Preliminary_settings.add_sheet("Centre Coordinates")
sheet2.write(0,0, 'Slice number')
sheet2.write(0,1, 'X')
sheet2.write(0,2, 'Y')

for i in range(0,sliceNoTotal):
    sheet2.write(i+1,0,str(i+1))
    sheet2.write(i+1,1,(X_cent[i,0]+refPt[0][0]).astype(str))
    sheet2.write(i+1,2,(Y_cent[i,0]+refPt[0][1]).astype(str))    

#Sheet 3: Segment points
sheet3 = Preliminary_settings.add_sheet("Segmentation Coordinates")

for j in range(0,sliceNoTotal):
    
    r = j*5
    sheet3.write(0,r, 'Slice' + str(j+1))
    sheet3.write(1,r, 'Point number')
    sheet3.write(1,r+1, 'X')
    sheet3.write(1,r+2, 'Y')

    for i in range(0,6):
        sheet3.write(i+2,r,str(i+1))
        sheet3.write(i+2,r+1, (X_segment[i,j]+refPt[0][0]).astype(str))
        sheet3.write(i+2,r+2, (Y_segment[i,j]+refPt[0][1]).astype(str))    

Preliminary_settings.save("Preliminary_settings.xls")


Segmentation_results = xlwt.Workbook(encoding="utf-8")

for s in range(0, sliceNoTotal):
    sheet = Segmentation_results.add_sheet("slice" + str(s+1))
    
    for j in range(0, stepsTotal):
        sheet.write(0,3*j,"timeStep" + str(j))
        sheet.write(1,3*j,"X-coord")
        sheet.write(1,3*j + 1, "Y-coord")
        
        for i in range(0,30):
            sheet.write(i+2, 3*j, X[i,j,s].astype(str))
            sheet.write(i+2, 3*j +1, Y[i,j,s].astype(str))
    
Segmentation_results.save("Segmentation_results.xls")


make_img_dir = "mkdir ResultImages"
os.system(make_img_dir)
os.chdir("./ResultImages")

for folder in range (0,sliceNoTotal):
    sliceFolder = "mkdir slice_" + str(folder+1)
    os.system(sliceFolder)
    for i in range (0,stepsTotal):
        img = cropped_images_Cine[:,:,:,i,folder]
        cv2.imwrite( "./slice_" + str(folder+1) +"/image_00"+ str(i) +".png", img )
    

#Tracking_co-ordinates = xlwt.Workbook(encoding="utf-8")

'''
Questions
1) Should we draw the segments for each slice location seperately? 
2) All the slices are not oriented exactly, therefore difficult to use the same segmentation  
3) How should we save the co-ordinates? In local X,Y, global X,Y ?
4) Do we also have to reorient the images or we )
can save the co-ordinates directly?
'''