# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 13:51:00 2017

@author: pretorj

"""
import numpy as np

# Heat transfer over a cylinder in cross flow

Re = 512
Pr = 0.7202

Nucyl = 0.3 + 0.62*Re**(1/2)*Pr**(1./3.)/((1. + (0.4/Pr)**(2./3.))**(1/4))*(1. + (Re/282000.)**(5./8.))**(4./5.)

# NU = h*D/k
k = 0.02808
D = 0.1

h = Nucyl*k/D

print(Nucyl, h)

h=300
As = 12*np.pi*0.008*0.3
V = 1
rho = 1.24
Ax = 0.08*0.3
mdot = rho * V * Ax
print (mdot)
Ts = 35.
Ti = 14.
Te = Ts -( Ts -Ti)*(np.exp(-As*h/(mdot*1005)))
Q = mdot*1005*(Te - Ti)
mdotwater = 0.1
Tewater = Q/(mdotwater*4180)-Ts
print(Te)
print(Q)
print(Tewater)
