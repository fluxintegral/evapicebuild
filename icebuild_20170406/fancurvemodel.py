# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 09:46:53 2017

@author: pretorj
"""

# DL da Silva et al 2011, Fan Curve

# THERE MAY BE AN ERROR IN CORRELATION OR CODE... COULD NOT FIND ERROR IN CODE

import matplotlib.pylab as plt
import numpy as np

dp = np.arange(0.1,60.)

V = (340. - 22.*dp + 0.57*dp**2. - 0.01*dp**3. + 4.4*10.**(-5.)*dp**4. - 1.1*10.**(-5.) * dp**5. )/ \
( 1. - 0.06*dp + 1.2*10.**(-3.)*dp**2. - 1.1*10.**(-5.)*dp**3. + 4.3*10.**(-8.)*dp**4. - 5.5*10.**(-11.) * dp**5.)



plt.plot( V, dp)