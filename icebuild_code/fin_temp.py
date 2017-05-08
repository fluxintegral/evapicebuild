# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 09:27:25 2017

@author: pretorj
Fin equations
"""

import numpy as np
import matplotlib.pylab as plt

Tb = -24.
Tinf = -18.
h = 25.
k = 237.
L = 0.025
t = 0.0002
p = 2.*(t+L)
Ac = t*L
x = np.arange(0., 0.0251, 0.001)
x = np.array(x)

m = np.sqrt(h*p/(k*Ac))

Tx = (Tb - Tinf)*(np.exp(-x*np.sqrt(h*p/(k*Ac))))+ Tinf
Q = np.sqrt(h*p*k*Ac) * (Tb - Tinf)

# adiatbatic fin tip



plt.plot(x, Tx)
print Q


Tx = Tx = (Tb - Tinf)*((np.cosh(m*(L-x)))/np.cosh(m*L)) + Tinf
Q = np.sqrt(h*p*k*Ac) * (Tb - Tinf)*np.tanh(m*L)

plt.plot(x, Tx, 'r-')
print Q

mL= 2.5 # 98.7% eff
mL = 5. # 100% eff
mL = 1. # 76% eff

L = 1/m

print L