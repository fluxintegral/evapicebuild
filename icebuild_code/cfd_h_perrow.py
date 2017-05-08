# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 12:55:42 2017

@author: pretorj
"""
import matplotlib.pylab as plt
import numpy as np

tperrow = [278, 273.6,273.1, 272.5, 272.1, 271.7, 271.4, 271.0, 270.8, 270.6, 270.5]
dt = np.array(tperrow[:10])- np.array(tperrow[1:11])
tperrowdmesh = [278, 273.6,273.2, 272.6, 272.3, 271.9, 271.7, 271.4, 271.2, 271.0, 271.0]
dtdmesh = np.array(tperrowdmesh[:10])- np.array(tperrowdmesh[1:11])
tperrow1 = [278, 275.5, 274.0, 273.1, 272.6, 272.1, 271.7, 271.3, 271.1, 270.8, 270.7]
dt1 = np.array(tperrow1[:10])- np.array(tperrow1[1:11])
tperrow2 = [278, 276.1, 276.0, 273.7, 273.1, 272.5, 272.1, 271.6, 271.3, 271.0, 271.0]
dt2 = np.array(tperrow2[:10])- np.array(tperrow2[1:11])
tperrow3 = [278, 276.1, 276.1, 275.5, 273.7, 273.0, 272.5, 272.0, 271.7, 271.3, 271.3]
dt3 = np.array(tperrow3[:10])- np.array(tperrow3[1:11])

tsurf=268.15
af = 0.0006978849495
cp = 1005
mdot = 1.28*1.4*0.04*0.0025
h = cp*mdot*dt/(af*(np.array(tperrow[1:])-tsurf))
h1 = cp*mdot*dt1/(af*(np.array(tperrow1[1:])-tsurf))
h2 = cp*mdot*dt2/(af*(np.array(tperrow2[1:])-tsurf))
h3 = cp*mdot*dt3/(af*(np.array(tperrow3[1:])-tsurf))
plt.plot(h)
plt.plot(h1)
plt.plot(h2)
plt.plot(h3)

plt.figure()
plt.plot(tperrow)
plt.plot(tperrow1)
plt.plot(tperrow2)
plt.plot(tperrow3)

plt.figure()
plt.plot(tperrow, label = 'Mesh 1')
plt.plot(tperrowdmesh, label = 'Mesh 2')
plt.xlabel('Pass')
plt.ylabel('Av Temp')
plt.legend()



