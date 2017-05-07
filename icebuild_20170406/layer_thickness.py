# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 13:35:20 2017

@author: pretorj
"""
import numpy as np
import matplotlib.pylab as plt

def dfpersegment(Volfrostperseg, Dtube = 0.008, finpitch = 0.02 , finheight = 0.025 ,finwidth = 0.025 , finthick = 0.0002):
    
    # Vtotal = Vtube + Vfin
    
    coeff = [-np.pi, (-np.pi*Dtube + np.pi/2*finpitch -np.pi/2*finthick), (finheight*finwidth-np.pi/4*Dtube**2-np.pi/2*Dtube*finthick+np.pi/2*Dtube*finpitch),-Volfrostperseg ]
    
    x1,x2,x3 = np.roots(coeff) 

    
    return(x3)

#finpitch = 0.005 
#Dtube = 0.008 
#finheight = 0.025 
#finwidth = 0.025 
#finthick = 0.0002
#
#df = np.linspace(0, 0.005,100)
#vol = finheight*finwidth*df - np.pi*df*(Dtube**2/4 + df**2 + df*Dtube) + np.pi/8*(4*df**2 + 4*df*Dtube)*(finpitch - finthick)
#
#volc = 0.000001
#x1,x2,x3 = deltafrost(volc)
#
#plt.plot(df,vol)
#plt.plot(x1,volc,'s')
#plt.plot(x2,volc,'x')
#plt.plot(x3,volc,'o')
#    
    
    