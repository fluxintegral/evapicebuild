# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 11:28:18 2017

@author: pretorj
"""

import numpy as np
import vapourmass as vp

Le = 0.87
wi = 0.9
nf = 0.8
ho = 500
Af = np.pi*0.008*0.3 # tube surf area
rho_air = 1.3
cp_air = 1000
V = 1.3
Ti = 5
Tf = -3
w_sat_f = vp.vapourmass(Tf,0.99)
wi  = vp.vapourmass(Ti,.75)


wii = w_sat_f-(w_sat_f- wi)*np.exp(-(nf*ho*Af)/(rho_air*cp_air*V*Le**(2/3)))

Tii = Tf - (Tf-Ti)*np.exp(-(nf*ho*Af)/(rho_air*cp_air*V))

print Ti - Tii
print wi- wii