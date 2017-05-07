# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 09:09:49 2017

@author: pretorj
Arden Buck Equations
Calculates the Saturation vapor pressure as function of temperature of moist
air
-Buck, A. L.(1981), New equations for computing vapor pressure and enhancement
factor, J. Appl. Meteorol., 20:1527-1532
-Buck (1996), Buck Reserach CR-1A User's Manual, Appendix1
"""

def Psat(T):
    import numpy as np
    
    T = np.array(T)
    for i in range(0,len(T)):
          
        if T[i] > 0. and T[i] <= 50.:
            Ps = 0.61121*np.exp((18.678 - T/234.5)*(T / (257.14 + T)))
                
        elif T[i] >= -80. and T[i] <= 0.:
            Ps = 0.61115*np.exp((23.036 - T/333.7)*(T / (279.82 + T)))
        
       

    return(Ps)      

