# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 13:53:08 2017

@author: pretorj
"""

import numpy as np
import matplotlib.pylab as plt

rho = 450
L = 0.03
x = 0.4

mg = 1.213322e-5

iter = 18000

hf = np.zeros(iter)
hf[0] = 0

for i in np.arange(1,iter):
    dt = 1
    hf[i] = 1/(rho*L*x)*mg*dt + hf[i-1]
    
print hf
print len(hf)


plt.plot(np.arange(iter)/60.,hf*1000)
plt.xlabel('time [min]')
plt.ylabel('frost thickness [mm]')
    
    
    