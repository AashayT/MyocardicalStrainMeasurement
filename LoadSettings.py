#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 22:45:28 2020

@author: user
"""

import numpy as np
import xlrd

def readSettings(path, settingsFile, sliceNoTotal):
    
    settings = xlrd.open_workbook(path + str(settingsFile))
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
            
    return [Points, CentX, CentY, SegX, SegY]