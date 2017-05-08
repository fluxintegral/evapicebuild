# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 15:32:49 2017

@author: pretorj
"""

##############################################################################
##############################################################################
import numpy as np
    
def kf(rho_f): 
    # From da Silva Thesis [2012] applicable for 50 < rho_f < 400
    k = 0.132 + 3.13e-4*rho_f +1.6e-7*rho_f**2
    
    return(k)

##############################################################################
##############################################################################

def rho_f(Ts,Tdewpoint):
    
#[1] First Principle modeling of frost accumulation on fan-supplied tube-fin
#    evaporators, D.L. Da Silva,CJ.L. Hermes, C Melo,
#    Applied Thermal Engineering, 2011, vol 30, 2616-2621.
    a = 494
    b = 0.11
    c = -0.06
    Ts = np.array(Ts)
    
    rho = a*np.exp(b*Ts+c*Tdewpoint)  #[1]    
    
    return(rho)
