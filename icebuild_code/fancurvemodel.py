# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 09:46:53 2017

@author: pretorj
"""

import numpy as np
def fancurve(dp):
    """ Fan curve from testing at room temperature at speed 255 on Bob's 
        telescope
    """
    lps = np.array([14.49,13.94,13.33,12.39,11.83,10.89,9.86,8.01,6.39,4.30,0])    
    mdot = lps/1000*1.24
    p = np.array([8.6,11.7,15.3,21.1,24.5,29.1,34.1,43.6,52.8,60.2,65.2])
    mdot = np.interp(dp,p,mdot)
    
    return(mdot)



