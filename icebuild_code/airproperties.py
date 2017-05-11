# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 14:13:56 2017

@author: pretorj
MODULE TO CALCULATE PROPERTIES OF AIR AND WATER VAPOUR
All temperature inputs DEGREES CENTIGRADE
RELATIVE HUMIDITY IS A FRACTION BETWEEN 0 AND 1

FUNCTIONS HEREIN SUMMARY:
Absolute Humidity   - vapourmass(Temperature, Relative Humidity)
Conductivity        - k(Temperature)
Density             - rho(Temperature, *Pressure)
Dewpoint            - Tdp(Temperature, Relative Humidity)
Diffusivity air vap - Dab(Temperature1, *Pressure1, *Temp2, *Pressure2)
Dynamic viscosity   - mu(Temperature)
Heat capacity       - cp(Temperature)
Lewis number        - Le(Temperature,*Pressure)
Relative Humidity   - relhumid(Temperature, Absolute Humidity)
Saturation pressure - Psat
Thermal Diffusivity - alpha(Temperature)


"""
import numpy as np

##############################################################################
##############################################################################

def vapourmass(temp,rh):
    '''
    Returns absolute humidity on kg/kg basis
    Source:
    Cost-Effective Refrigeration, D.J. Cleland, A.C. Cleland, S.D White,
    R.J. Love, I. Merts, A.R. East, J.F. Wang, and A.H.J Paterson, Massey
    University, Palmerston North, New Zealand,(2013), PP.6.3 
    '''
    
    if temp <= 0:
        pw = np.exp(28.7775 -(6071.67/(temp+271.11)))
#        print('t < 0 , %0.5f') %(pw)
    elif temp > 0:
        pw = np.exp(23.4795 -(3990.56/(temp+233.833)))        
#        print('t > 0 , %0.5f') %(pw)
    if rh > 1.0 or rh < 0.0 :
        print('!!!!!!!!!! RH MUST BE BETWEEN 0 AND 1 !!!!!!!!!')        

    P = 101325.0
    pv = pw*rh    # Partial pressure
    H = 18.0 * pv/(29.*(P-pv)) # absolute humidity (moisture) kg/kg dry air
    
    return(H)  # kg/kg

##############################################################################
##############################################################################

def vapourdensity(T,P = 101325.):
    '''
    Rv = 461.5
    '''
    R = 461.5
    T = T + 273.15
    density = P/(R*T)
    
    return(density)
##############################################################################
##############################################################################

def k(T):
    T = T + 273.15
    kis = (2.334*10**-3*T**(3./2.))/(164.54 + T)
    
    return(kis)

##############################################################################
##############################################################################

def rho(T,P = 101325):
    '''Return density of air 
        Source: Ideal gas law '''
    R =  287.05
    T = T + 273.15
    density = P/(R*T)
    
    return(density)

##############################################################################
##############################################################################
    
def Tdp(T,RH):
    ''' Source: Magnus Formula'''
        
    T = np.array(T)
    for i in range(0,len(T)):
                  
        if T[i] > 0. and T[i] <= 50.:
            b = 17.368
            c = 238.88 # degC
            
                
        if T[i] >= -40. and T[i] <= 0.:
            b = 17.966
            c = 247.15 # degC

        y =np.log(RH)+b*T/(c+T)   # Magnus Formula
        Tdewpoint = c*y/(b-y)           # Magnus Formula

    return(Tdewpoint)            
    
##############################################################################
##############################################################################

def Dab(T, P = 101325., T2 = 298.15, P2 = 101325.):
    #source: Cengel, Heat and mass transfer a practical approach 3rd ed.,
    #pp. 780-781
    Dab2= 2.5*10**-5
    T = T + 273.15
    Dab1 = Dab2*P2/P*(T/T2)**(3/2) # Result is within 5% of Lee et al.(1997)
    
   
    return(Dab1)
##############################################################################
##############################################################################

def mu(T):
    
    T = T + 273.15  
    C = 1.458e-6
    S = 110.4
    mu = (C*T**(3./2.))/(T +S)  # Sutherland, W (1983), The visc of gases
    
    return(mu)


##############################################################################
##############################################################################
    
def cp(T):
    '''source: Cengel, Heat and mass transfer a practical approach 3rd ed.,
       pp. 860 from Table A-15'''

    
    Tset = [-150,-100, -50, -40, -30, -20, -10, 10, 15, 70, 80, 90, 100, 120,
            140, 160, 180, 200,250, 300, 350, 400, 450, 500, 600, 700, 800,
            900, 1000, 1500, 2000]
              
    Cpset= [983, 966, 999, 1002, 1004, 1005, 1006, 1006, 1007, 1007, 1008 ,
            1008, 1009, 1011, 1013, 1016, 1019, 1023, 1033, 1044, 1056, 
            1069, 1081, 1093, 1115, 1135, 1153, 1169, 1184, 1234, 1264]            
            
    return(np.interp(T,Tset,Cpset))
    

##############################################################################
##############################################################################
    
def Le(T,P = 101325.):

    T = np.array(T)
    lewisnr = alpha(T)/Dab(T,P)
    
    return(lewisnr)

##############################################################################
##############################################################################
    
def relhumid(temp,H):
    '''
    Cost-Effective Refrigeration, D.J. Cleland, A.C. Cleland, S.D White,
    R.J. Love, I. Merts, A.R. East, J.F. Wang, and A.H.J Paterson, Massey
    University, Palmerston North, New Zealand,(2013), PP.6.3 
    '''
    if temp <= 0:
        pw = np.exp(28.7775 -(6071.67/(temp+271.11)))

    elif temp > 0:
        pw = np.exp(23.4795 -(3990.56/(temp+233.833)))        
        
    P = 101325.0
    pv = 29.*H*P/(18.+29.*H)
    rh = pv/pw
    return(rh) 

##############################################################################
##############################################################################

def Psat(T):
    """Arden Buck Equations
    Calculates the Saturation vapor pressure as function of temperature of moist
    air
    -Buck, A. L.(1981), New equations for computing vapor pressure and enhancement
    factor, J. Appl. Meteorol., 20:1527-1532
    -Buck (1996), Buck Reserach CR-1A User's Manual, Appendix1
    """
    
    T = np.array(T)
    for i in range(0,len(T)):
          
        if T[i] > 0. and T[i] <= 50.:
            Ps = 0.61121*np.exp((18.678 - T/234.5)*(T / (257.14 + T)))
                
        elif T[i] >= -80. and T[i] <= 0.:
            Ps = 0.61115*np.exp((23.036 - T/333.7)*(T / (279.82 + T)))
        
       

    return(Ps)      


##############################################################################
##############################################################################
    
def alpha(T, P = 101325.0):
    ''' thermal diffusivity '''
    
    alp = k(T)/(rho(T,P)*cp(T))
    
    return(alp)


##############################################################################
##############################################################################