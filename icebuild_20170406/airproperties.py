# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 14:13:56 2017

@author: pretorj
"""

def mu(T):
    T = T + 273.15  
    C = 1.458e-6
    S = 110.4
    mu = (C*T**(3./2.))/(T +S)  # Sutherland, W (1983), The visc of gases
    
    return(mu)

def rho(T,P = 101325):
    "(Temp (C), P (Pa)- Ideal gas law)"
    R =  287.05
    T = T + 273.15
    density = P/(R*T)
    
    return(density)
    
def cp(T):
    #source: Cengel, Heat and mass transfer a practical approach 3rd ed.,
    #pp. 860
    import numpy as np
    
    Tset = [-150,-100, -50, -40, -30, -20, -10, 10, 15, 70, 80, 90, 100, 120,
            140, 160, 180, 200,250, 300, 350, 400, 450, 500, 600, 700, 800,
            900, 1000, 1500, 2000]
              
    Cpset= [983, 966, 999, 1002, 1004, 1005, 1006, 1006, 1007, 1007, 1008 ,
            1008, 1009, 1011, 1013, 1016, 1019, 1023, 1033, 1044, 1056, 
            1069, 1081, 1093, 1115, 1135, 1153, 1169, 1184, 1234, 1264]            
            
    return(np.interp(T,Tset,Cpset))
    
def k(T):
    T = T + 273.15
    kis = (2.334*10**-3*T**(3./2.))/(164.54 + T)
    
    kg = 0.132 + 3.13e-4*rho(T)+ 1.6e-7*(rho(T))**2
   
    return(kis)


    
    
def alpha(T, P = 101325.0):
    
    
    alp = k(T)/(rho(T,P)*cp(T))
    
    return(alp)

def Dab(T, P = 101325., T2 = 298.15, P2 = 101325.):
    #source: Cengel, Heat and mass transfer a practical approach 3rd ed.,
    #pp. 780-781
    Dab2= 2.5*10**-5
    T = T + 273.15
    Dab1 = Dab2*P2/P*(T/T2)**(3/2)
    
    return(Dab1)

    
def Le(T,P = 101325.):
    import numpy as np
    T = np.array(T)
    lewisnr = alpha(T)/Dab(T,P)
    
    return(lewisnr)
    