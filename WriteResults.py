#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 23:23:20 2020

@author: user
"""

import os
import xlwt

def writeResults(path, resultsFolderName, stepsTotal, sliceNoTotal, refPt, X_cent, Y_cent, X_segment, Y_segment, X, Y): 
    os.chdir(path)
    make_dir = "mkdir "+ str(resultsFolderName)
    os.system(make_dir)
    os.chdir(resultsFolderName)
    
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
