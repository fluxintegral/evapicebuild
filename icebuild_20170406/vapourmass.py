# -*- coding: utf-8 -*-
"""
Created on Tue Feb 07 13:15:32 2017

@author: pretorj


%% REF FOR BELOW EQUATIONS
%% Cost-Effective Refrigeration, D.J. Cleland, A.C. Cleland, S.D White,
%% R.J. Love, I. Merts, A.R. East, J.F. Wang, and A.H.J Paterson, Massey
%% University, Palmerston North, New Zealand,(2013), PP.6.3 

"""
import numpy as np 
def vapourmass(temp,rh):
    "vapourcontent(volume (L),temperature (C),RH (Fraction))"
    
     
    
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
    
    return(H)
    
def relhumid(temp,H):
    if temp <= 0:
        pw = np.exp(28.7775 -(6071.67/(temp+271.11)))

    elif temp > 0:
        pw = np.exp(23.4795 -(3990.56/(temp+233.833)))        
        
    P = 101325.0
    pv = 29.*H*P/(18.+29.*H)
    rh = pv/pw
    return(rh)


    
    
        
        