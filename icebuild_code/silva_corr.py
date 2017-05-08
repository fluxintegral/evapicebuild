# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 09:41:06 2017

@author: pretorj
"""
import numpy as np
import matplotlib.pylab as plt
import geometry as geom
import airproperties as air
import frostproperties as frost
import controlvolume as cor
import fancurvemodel as fan  

   

Pinit = 16 # pa 8 evap 8 system
mdot = fan.fancurve(Pinit) # fan curve from ming's work
ho = 20
isv = 2830e3 # J/kg from Hermes (2009)
xfrosti = 0

cpa = 1005.
Tini = 14
RHini = 0.85


## Define evaporator geometry parameters
N = 11  # Number of passes
Di = 0.008 # tube diameter clean
width = 0.25 # end plate to end plate evap width in m
finpitch = [0.02, 0.02, 0.01, 0.01, 0.01, 0.005, 0.005, 0.005, 0.005, 0.005] # fin pitch per pass 0 for no fin, else fin pitch in m
finheight = 0.025
findepth = 0.025
finthick = 0.0002


Af = geom.asurfpersection(xfrosti)

## initialise variables
#T = np.zeros(N)
#T[0] = Tini
#rho1 = air.rho(T[0])
#W = np.zeros(N)
#W[0] = air.vapourmass(Tini,RHini)
#RH = np.zeros(N)
#RH[0] = air.relhumid(Tini,W[0])
#moisturedeposit = np.zeros(N)
#qlat = np.zeros(N)
#qsen = np.zeros(N)
#Tdew = np.zeros(N)
#rho_frost = np.zeros(N)
#
#
#
#for i in np.arange(1,N):
#    rho1 = air.rho(T[i-1]) 
#    T[i] = cor.Tii(ho,Af*seg,rho1,cpa,mdot,Tfs,T[i-1])
#    W[i] = cor.wii(ho,Af*seg,rho1,cpa,mdot,Tfs,T[i-1],W[i-1],air.vapourmass(Tfs,1),air.Le(Tfs))
#    RH[i] = air.relhumid(T[i],W[i])
#    moisturedeposit[i] = W[i-1] - W[i]
#    qlat[i] = moisturedeposit[i]*mdot*isv
#    qsen[i] = (T[i-1]-T[i])*cpa*mdot
#    Tdew[i] = air.Tdp([T[i]],(RH[i]))
#    rho_frost[i] = frost.rho_f(Tfs,Tdew[i])
#    #Tfrost = cor.Tfs(-5,(T[i-1]+T[i])/2,qsens(T[i-1],T[i])    
#    
#    
#hour = 0.66    
#min =60*hour
#iter = round( min*60)
#mfrost = np.zeros([iter,N])
#frost_thick = np.zeros([iter,N])
#xareaopen =  np.zeros([iter,N])
#for t in np.arange(1,iter):
#    # calculate grams per pass accumulative
#    
#    for i in np.arange(1,N):    
#        mfrost[t,i] = mfrost[t-1,i] + moisturedeposit[i]*mdot
#        frost_thick[t,i] = geom.dfpersegment((mfrost[t,i]/rho_frost[i])/seg,Di0,finpitch)
#        xareaopen[t,i] = geom.axpersection(frost_thick[t,i],Di0,finpitch)
#
#plt.plot(T,'x-')
#plt.plot([0,N],[Tfs]*2,'g-')  
#plt.xlabel('Pass')
#plt.ylabel('Temp')
#
#plt.figure()
#plt.plot(qlat,'gx-', label = 'latent')
#plt.plot(qsen,'rx-', label = 'sensible')
#plt.plot(qsen+qlat,'k--', label = 'sensible')
#plt.xlabel('Pass', fontsize = 14)
#plt.ylabel('Q ', fontsize = 14)
#plt.legend( fontsize = 14)
#plt.tick_params( labelsize = 14)
#
#plt.figure()
#plt.plot(W,'x-')  
#plt.xlabel('Pass')
#plt.ylabel('H (kgv/kgair)')
#
#plt.figure()
#plt.plot(RH,'x-')  
#plt.xlabel('Pass')
#plt.ylabel('RH (%)')
#
#
#plt.figure()
#plt.plot((frost_thick[-1,1:]*1000),'x-')  
#plt.tick_params(axis='both', labelsize = 14)
#plt.xlabel('Pass',fontsize = 18)
#plt.ylabel('$\delta t_{frost}$ (mm)',fontsize = 18)
#
#
#plt.figure()
#for i in np.arange(1,N):
#    
#    plt.plot(np.arange(1,iter)/60,mfrost[1:,i]*1000,'-', label = 'Pass %s' % i)
#
#plt.xlabel('Time')
#plt.ylabel('Frost mass (g)')
#plt.annotate('Total mass = %s g' %round(sum(mfrost[-1,:]*1000)), xy = (40,max(mfrost[:,1]*1000)))
#plt.legend(loc =2)
#
#plt.figure()
#for i in np.arange(1,N):
#    
#    plt.plot(np.arange(1,iter)/60,frost_thick[1:,i]*1000,'-', label = 'Pass %s' % i)
#
#plt.xlabel('Time')
#plt.ylabel('Frost Thickness')
#plt.annotate('Total mass = %s g' %round(sum(mfrost[-1,:]*1000)), xy = (40,max(mfrost[:,1]*1000)))
#plt.legend(loc =2)
#    
#plt.figure()
#for i in np.arange(1,N):
#    
#    plt.plot(np.arange(1,iter)/60,xareaopen[1:,i]*1000000,'-', label = 'Pass %s' % i)
#
#plt.xlabel('Time')
#plt.ylabel('X sectional open area $[mm^2]$')
#plt.legend(loc =2)
#    
#
#
#    

