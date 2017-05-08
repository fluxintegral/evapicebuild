# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 13:24:45 2017

Surface area per pass - asurfperpass
Cross sectional area per pass - axperpass
Frost thickness - dfpersegment
"""

import numpy as np



def asurfperpass(dfrost, dtube = 0.008, evapwidth = 0.314, finpitch = 0.01,\
                    finwidth = 0.025, finheight = 0.026,finthickness = 0.0002):
    ''' Calculates the surface area if dfrost = 0 then the result is the bare
        evap surface area if dfrost is > than 0 the exposed frost surface area
        per section is returned'''
    
    if finwidth == 0. or finheight == 0. or finthickness == 0. \
       or evapwidth <= finpitch:
        
       afin = 0.
       
    else:
       afin = 2.*dfrost*finwidth + 2.*dfrost*finheight + finheight*finwidth - \
       np.pi/4.*(dtube+2*dfrost)**2. 
    
    if afin ==0:
        finthickness = 0.     
        
    atube =  np.pi*(dtube + 2.* dfrost)* \
    (finpitch/2. - finthickness/2. - dfrost)
    
    aseg = afin + atube
    segments = evapwidth/(finpitch/2)
    passsurfarea = aseg*round(segments)
    
    return(passsurfarea)

def axperpass(dfrost,dtube=0.008, evapwidth = 0.314, finpitch = 0.01 , finwidth = 0.025, \
                 finheight = 0.027, finthickness = 0.0002, gap = 0.0):
    ''' This function returns the cross sectional flow area per section of
        evap'''
    ax = 2*(finpitch/2-dfrost - finthickness/2)*(finwidth/2-dtube/2-dfrost)+ \
    2*gap*finpitch/2
    
    segments = evapwidth/(finpitch/2)
    passcrosssectionarea = ax*round(segments)
    
    return(passcrosssectionarea)

def dfpersegment(Volfrostperseg, Dtube = 0.008, finpitch = 0.02 , \
                 finheight = 0.025 ,finwidth = 0.025 , finthick = 0.0002):
    
    # Vtotal = Vtube + Vfin
    
    coeff = [-np.pi, (-np.pi*Dtube + np.pi/2*finpitch -np.pi/2*finthick), \
             (finheight*finwidth-np.pi/4*Dtube**2-np.pi/2*Dtube*finthick+ \
              np.pi/2*Dtube*finpitch),-Volfrostperseg ]
    
    x1,x2,x3 = np.roots(coeff) 

    
    return(x3)
#-----------------------------------------------------------------------------
# TEST CODE
#-----------------------------------------------------------------------------
#import matplotlib.pylab as plt
#
#Dtube = 0.008
#finpitch = 0.005
#finheight = 0.027 
#finwidth = 0.025
#finthick = 0.00015
#thickness_eval =np.arange(-0.018,0.018,0.0005)
#N = len(thickness_eval)
#df = np.array([thickness_eval])
#volume = -np.pi*df**3 + (-np.pi*Dtube + np.pi/2*finpitch -np.pi/2*finthick)*df**2 + (finheight*finwidth-np.pi/4*Dtube**2-np.pi/2*Dtube*finthick+ np.pi/2*Dtube*finpitch)*df
#trend = np.zeros((N,2))
#trend[:,0] = df
#trend[:,1] = volume
#plt.plot(trend[:,0], trend[:,1], '-')