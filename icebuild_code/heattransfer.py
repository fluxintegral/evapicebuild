# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 11:13:38 2017

@author: pretorj
"""

def lmtd(Ts, Te, Ti):
    import numpy as np
    Ts , Te, Ti = float(Ts)
    Te = float(Te)
    Ti = float(Ti)
    dTe = Ts - Te
    dTi = Ts - Ti
    T = (dTe - dTi)/np.log(dTe/dTi)
    
    return T
    
def Nuflat(Rex, Pr):
    """    
    Nu for airflow over a flat plate from Heat and mass transfer: A practical 
    approach ed3, Cengel pp 402 
    """
    Rex = float(Rex)
    Pr = float(Pr)

    if Rex < 5*10**5:
        Nu = 0.664*Rex**0.5*Pr**(1/3.)
        print 'lam'
    elif Rex >= 5*10**5:
        Nu =  0.037*Rex**0.8*Pr**(1/3.) 
        print 'turb'
    
    return Nu
    
