# -*- coding: utf-8 -*-
"""
Created on Tue May  2 09:51:36 2017

@author: pretorj
"""

# plot magnus formula

import numpy as np
import airproperties as air
import matplotlib.pylab as plt

rh = 0.5
temp = np.arange(-20,20,0.2)

dewpoint = air.Tdp(temp,rh)

plt.plot(temp,dewpoint)


