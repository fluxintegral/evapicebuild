# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 10:31:49 2017

@author: pretorj
"""

#qsens = mdot * cp * dt

#qlat = mdot * isens * dH

# Frost surface temperature

import numpy as np

rho = 1.3
cp = 1005.
V = 1.3
Ti = 5.
Tii= -1.
isv = 334.*1000
Ts = -5.
wi = 0.0001723
wii = 5.09939*10**-5
wsat = 5.09939*10**-5 
As = np.pi*0.008*0.2
xf = 0.001
kf = 0.2
Dw = 2.27360e-5

Qsens = rho*cp*V*(Ti - Tii)
Qlat = rho*isv* V *( wi- wii)

Tf = Ts + (Qsens + Qlat)/As*(xf/kf) - (rho*wsat*isv)/kf * Dw/tau