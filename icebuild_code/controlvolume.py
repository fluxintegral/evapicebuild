# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 10:31:49 2017

@author: pretorj
"""

#qsens = mdot * cp * dt

#qlat = mdot * isens * dH

# Frost surface temperature

import numpy as np


##############################################################################
##############################################################################
    
def Tii(ho,Af,mdot,cpa,Tfs,Ti, n = 1):
    mm = -n*ho*Af/(mdot*cpa)
    Tii = Tfs - (Tfs-Ti)*np.exp(mm)
    return(Tii)

##############################################################################
##############################################################################
    
def wii(ho,Af,mdot,cpa,Tfs,Ti, wi, wsat, Le , n = 1.):
    
    mm = (-n*ho*Af)/(mdot*cpa*Le**(2./3.))   
    wii = wsat - (wsat-wi)*np.exp(mm)  # wsat is humidity ratio at Tfs
    return(wii)    

##############################################################################
##############################################################################
def dp(cf,rho,Lcv,Dh,V,Amin):
    
    dpcv = 2*cf*rho*Lcv/Dh*(V/Amin)**2
    
    return(dpcv)

##############################################################################
##############################################################################

def qsens(Ti,Tii,mdot,cp):
    q = mdot*cp*(Ti - Tii)
    return(q)

##############################################################################
##############################################################################

def qlat(wi,wii,mdot):
    isv = 2830e3
    q = mdot*isv*(wi-wii)
    return(q)
    
##############################################################################
##############################################################################
def Tfs(Ts,Tav,Qsens,Qlat,xf,rho_a,rho_frost,Asurf,kf,w_sat_s,Dw,w_sat_cv):
    '''
    Qsens - Sensible heat transfer per control volume
    Qlat  - Latent heat transfer per control volume
    xf    - frost thickness in control volume
    kf    - frost thermal conductivity from Lee et al. (1997)
    
    Asurf - Total surface area per control volume
    '''
    isv = 2830e3 # J/kg latent heat of desublimation from Hermes et al(2009)
    # Density of water vapour
    P = 101325.0
    R = 461.5
    T = Tav + 273.15
    rho_vapour = P/(R*T)
    ###    
    # Calculate tau
    # Equations from  A study of frost growth and densification on flat
    # surfaces, Hermes et al (2009), Experimental Thermal and fluid sciences,
    # vol 33, pp.371-379.
    rho_ice = 916.7
    eps = (rho_frost - rho_ice)/(rho_vapour - rho_ice) # eq 17
    tau = eps/(1-np.sqrt(1-eps))    # eq 18
    ############
    
    Tf = Ts + (Qsens + Qlat)/Asurf*(xf/kf) - (rho_a*w_sat_s*isv)/kf * Dw/tau* \
    (np.cosh(w_sat_cv/w_sat_s)-1)
    
    return(Tf)

##############################################################################
##############################################################################
