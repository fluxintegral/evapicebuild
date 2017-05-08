# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 12:03:25 2017

@author: pretorj
Dew Point Temperature Calculator

"""

def Tdp(T,RH):
    import numpy as np
    
    T = np.array(T)
    for i in range(0,len(T)):
                  
        if T[i] > 0. and T[i] <= 50.:
            a = 6.1121 # millibar
            b = 17.368
            c = 238.88 # degC
            
                
        if T[i] >= -40. and T[i] <= 0.:
            a = 6.1121 # millibar
            b = 17.966
            c = 247.15 # degC
            
        
        y =np.log(RH/100.0)+b*T/(c+T)   # Magnus Formula
        Tdewpoint = c*y/(b-y)           # Magnus Formula

    return(Tdewpoint)        
        