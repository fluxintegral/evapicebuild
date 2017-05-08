# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 09:45:58 2017

@author: pretorj

Generic Heat transfer and pressure drop correlations from Wang(2000)

j is the Coburn factor j = Nu/(Re*Pr**0.33)

"""
import numpy as np

def jffactors(Fp,PL,Pt,Do,N,Re,L,Ac,Ao):
    """ FP - Fin Pitch 
        PL - Longitudinal tube pitch
        Pt - Transverse Tube pitch
        Do - Tube Diameter
        N  - Number of passes
        Re - Reynolds number based on tube diameter
        L  - Depth of heat exhanger in air flow direction
        Ac - Minimum cross sectional flow area
        Ao - Total surface area
    """
        
    
    
    Dh = 4*Ac*L/Ao
    
    Dc = Do  # fin collar outside diameter was used this ~= Outside tube diam
       
    P1 = 1.9 - .23*np.log(Re)
    
    P2 = -0.236 + 0.126* np.log(Re)
    
    P3 = -0.361 - 0.042*N/(np.log(Re)) +0.158*np.log(N*(Fp/Dc)**0.41)
    
    P4 = -1.224 - (0.076*(PL/Dh)**1.42)/(np.log(Re))
    
    P5 = - 0.083 + 0.058*N/(np.log(Re))
    
    P6 = - 5.735 + 1.21*np.log(Re/N)
    
    
    if N == 1:
        j = 0.108 * Re**-0.29*(Pt/PL)**P1 * (Fp/Dc)**-1.084 * (Fp/Dh)**-0.786 \
        * (Fp/Pt)**P2
        
    elif N > 1:
        
        j = 0.086*Re**P3 * N**P4 * (Fp/Dc)**P5 * (Fp/Dh)**P6 * (Fp/Pt)**-0.93
    
    
    F1 = -0.764 + 0.739*(Pt/PL) + 0.177*(Fp/Dc) -0.00758/N
    
    F2 = -15.689 + 64.021/(np.log(Re))
    
    F3 = 1.696 - 15.695/(np.log(Re))
    
    f = 0.0267*Re**F1 * (Pt/PL)**F2 * (Fp/Dc)**F3
    
    return(j,f,Dh)


# Test results
#rho = 1.3
#L = 0.027
#j,f,Dh = jffactors(0.005,0.027,0.05, 0.008, 1., 500, 0.05, 0.0051408, 0.08316)
#V = 1
#dp = f * L/Dh*2*rho*V**2
#N = 5
#
#print(dp*N)
#
#
#dpcfdfirst =  1.462*V**2 + 0.666*V + (0.104*V**2 + 0.481*V)*(N-1)
#
#print(dpcfdfirst)
#Pr = 0.72
#h = j*(rho*V*1005)/(Pr**0.66)
#print(h)



