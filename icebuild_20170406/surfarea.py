# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 10:09:23 2017

@author: pretorj
"""
import numpy as np

def asurfpersection(dfrost,dtube = 0.008 ,finpitch = 0.01, finwidth = 0.025,finheight = 0.025,finthickness = 0.0002):
    ''' This function calculates the surface area on a per section basis of a
        columns evap, if dfrost = 0 then the result is the bare evap surface area
        if dfrost is > than 0 the exposed frost area is use as the evap surface area'''
    
    if finwidth == 0. or finheight == 0. or finthickness == 0. :
        
       afin = 0.
       
    else:
       afin = 2.*dfrost*finwidth + 2.*dfrost*finheight + finheight*finwidth - \
       np.pi/4.*(dtube+2*dfrost)**2. 
    
    if afin ==0:
        finthickness = 0.     
        
    atube =  np.pi*(dtube + 2.* dfrost)* \
    (finpitch/2. - finthickness/2. - dfrost)
    
    aseg = afin + atube
    
    return(aseg)

def axpersection(dfrost,dtube=0.008 ,finpitch = 0.01 , finwidth = 0.025, finheight = 0.025, finthickness = 0.0002, gap = 0.0):
    ''' This function returns the cross sectional flow area per section of evap'''
    ax = 2*(finpitch/2-dfrost - finthickness/2)*(finwidth/2-dtube/2-dfrost)+2*gap*finpitch/2
    
    return(ax)
    
    
    
    
    
    