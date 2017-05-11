# -*- coding: utf-8 -*-
"""
Created on Tue May  2 09:51:36 2017

@author: pretorj
"""

# plot magnus formula

import numpy as np
import airproperties as air
import matplotlib.pylab as plt
import geometry as geom
import controlvolume as cor

def abshumid(wsatfs,wi,nf,ho,Af,mdot,cp,Le):
    
    wii = wsatfs -(wsatfs - wi)*np.exp(-nf*ho*Af/(mdot*cp*Le**(2./3.)))
    
    return(wii)


rh = 0.8


Ti = -1
Tfs = -4
wsatfs = air.vapourmass(Tfs,1) 
wi = air.vapourmass(Ti,rh)
#plt.plot(temp,dewpoint)


n_f =1
ho =20
Af = 0.05442467
cp =1006
Le = 1
mdot = 0.015

wii = cor.wii(ho,Af,mdot,cp,Tfs,Ti,wi,wsatfs,Le,n_f)
wii2 = abshumid(wsatfs,wi,n_f,ho,Af,mdot,cp,Le)
print('Wi = %0.2f g' %(wi*1000) )
print('Wii = %0.2f g' %(wii*1000) )
print('Wii2 = %0.2f g' %(wii2*1000))
if wi < wii:
    print('HKGK')
    
    


#
#Te = -5
#wsatairTE = air.vapourmass(Te,1)
#wsatairfs = air.vapourmass(-5.07934,1)
#Dv = air.Dab(-3)
#kfrost = 0.277
#isv = 2280e3
#Qlat = 0.4
#Qsens = 4
#Xf = 0.0001
#asurf = geom.asurfperpass(Xf,0.008,0.314,0.01)
#rho_air = air.rho(-2)
#tau =30
#
#Tfs = Te + (Qsens +Qlat)*Xf/(kfrost*asurf) - rho_air*wsatairTE*isv*Dv/\
#(kfrost*tau)*(np.cosh(wsatairfs/wsatairTE)-1)
#
#print(Tfs)

#print(np.exp((-n_f*ho*Af)/(cp*mdot*Le**(2/3))))