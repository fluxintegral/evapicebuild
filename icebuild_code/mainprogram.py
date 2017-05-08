# -*- coding: utf-8 -*-
"""
Created on Tue May  2 13:30:16 2017

@author: pretorj
"""

import geometry as geom
import fancurvemodel as fan
import airproperties as air
import frostproperties as frost
import controlvolume as cor
import heatandfriction as jf
import numpy as np
import matplotlib.pylab as plt


### Initial parameters
Te = -5
Treturn = -2
RHreturn = 0.85
t = 0           # Time 0s
frostx = 10e-6  # Non zero frost thickness starting condition
Ts = Te         # Frost == Evap Surface Temp
dt = 1          # Seconds 
targetminerrorTfs = 0.01 # maximum difference between assumed and calculated frost surface temperature
dperror = 0.1
maxtime = 3 # hours

### Evap geometry Unit m
Passes = 3
Finpitch = [.008 ,.008, 0.008]
TubeDiameter = 0.008 
Width = 0.314 # endplate to endplate
tubepitch = 0.027
control_vol_h = 0.027


##################

pmax = 65   # maximum pressure drop desired or derived from max compartment temperature distribution requirement

## Initialise variables
#SegmentsPerPass = 
seconds = np.round(maxtime*3600)
dptrace = np.zeros(seconds)
mdottrace = np.zeros(seconds)

ftrace = np.zeros((seconds,Passes))
fxtrace = np.zeros((seconds,Passes))
htrace = np.zeros((seconds,Passes))




minxsection = np.zeros(Passes)
dpperpass = np.zeros(Passes)
T = np.zeros(Passes+1) # +1 To allow for the inlet control volume
Ts = np.zeros(Passes)
Ts = Te # update to reflect frost surface temperature
w = np.zeros(Passes+1)
w[0] = air.vapourmass(Treturn,RHreturn)
frostx = np.zeros(Passes)
#RH = np.zeros(N)
#RH[0] = air.relhumid(Tini,W[0])
#moisturedeposit = np.zeros(N)
#qlat = np.zeros(N)
#qsen = np.zeros(N)
#Tdew = np.zeros(N)
#rho_frost = np.zeros(N)

### Fan curve
nofrost_resistancecurve = 0. # update!
dpevap = 14.   # assume initial pressure drop to get initial mass flow rate
dptotal = nofrost_resistancecurve + dpevap

while dptotal < pmax:
    
    t = t + dt      # increment time
    dptrace[t] = dptotal
    mdot = fan.fancurve(dptotal)
    mdottrace[t] = mdot
    print('---------------')
    print('Time Step Summary')
    print('---------------')
    print('time: %i sec' %t)    
    print('mdot: %0.4f kg/s' %mdot)    
    print('DP: %0.1f Pa' %dptotal)
        
    i = 0
    surfaceareatotal = 0 
    Tair = Treturn
    RH = RHreturn
    dptotal = 0
    T[0] = Treturn
    
    
    while i < Passes:
        
        ## Calculate geometric properties of pass        
        surfacearea = geom.asurfperpass(frostx[i],TubeDiameter,Width,Finpitch[i])
        minxsection = geom.axperpass(frostx[i],TubeDiameter,Width,Finpitch[i])
                
        ## Air properties
        visc    = air.mu(Tair)
        rho_air = air.rho(Tair)
        Pr      = 0.73
        k_air   = air.k(Tair)
        Tdp     = air.Tdp([Tair],RH)
        D       = air.Dab(Tair)
        Cp_air  = air.cp(Tair)
        Lewis   = air.Le(Tair)
        alp     = air.alpha(Tair)
        
        ## Frost Properties
        rho_f   = frost.rho_f(Ts,Tdp)
        kfrost = frost.kf(rho_f)
        
        ## Flow Regime and Properties
        Vmax = mdot/(rho_air*minxsection)
        
        Vmean = mdot/(rho_air*Width*(0.025))
        Re   = rho_air*Vmax*(TubeDiameter)/visc
        
        ## Heat transfer and pressure drop
        j, f, Dh= jf.jffactors(Finpitch[i],tubepitch,0.05,TubeDiameter+frostx[i]*2,1,Re,control_vol_h,minxsection,surfacearea)
        h = j*rho_air*Vmax*Cp_air/(Pr**0.66)
#        f = 0.1
#        h = 20
        dpperpass = f * control_vol_h/Dh*2*rho_air*Vmax**2
        
        ftrace[t,i] = f 
        htrace[t,i] = h
        
        ## Control volume interfaces
        T[i+1] = cor.Tii(h,surfacearea,mdot,Cp_air,Ts,T[i])
        w[i+1] = cor.wii(h,surfacearea,mdot,Cp_air,Ts,T[i],w[i],air.vapourmass(Ts,1),Lewis)
        qsens =  cor.qsens(T[i],T[i+1],mdot,Cp_air)
        qlat  = cor.qlat(w[i],w[i+1],mdot)
        frostmass = (w[i]-w[i+1])*mdot
        frostvol = frostmass/rho_f
        frostlayer = geom.dfpersegment(frostvol, TubeDiameter,Finpitch[i])
        frostx[i] = frostx[i] + frostlayer
        ## Evaporator totals
        fxtrace[t,i] = frostx[i]
        dptotal = dpperpass + dptotal
                
        ## Output per pass summary
#        print('---------------')
#        print('Pass: %i' %(i+1))  # +1 Added for human readablity
#        print('---------------')
#        print('Min x Area:\t %0.5f m^2' %minxsection)
#        print('Surf Area:\t %0.5f m^2' %surfacearea)
#        print('Vmax:\t\t %0.2f m/s' %Vmax)
#        print('Vmean:\t\t %0.2f m/s' %Vmean)
#        print('Re: \t\t %i' %Re)
#        print('Frost Density: \t %i' %rho_f)
#        print('DP: \t\t %0.1f' %dpperpass)
#        print('h: \t\t %0.1f' %h)
#        print('f: \t\t %0.5f' %f)
#        print('Te,cv: \t\t %0.1f' %T[i+1])
#        print('w,cv: \t\t %0.1f g' %((w[i+1])*1000))
#        print('m_frost,cv: \t %0.5f g' %(frostmass*1000))
#        print('Qsens: \t\t %0.1f' %qsens)
#        print('Qlat: \t\t %0.1f' %qlat)
#        print('Frost thick: \t %0.5f' %frostx[i])
#        
        
        
        #print('DP: \t\t %0.1f',%dp)
        
        
#        print('X Surf Area: %0.6f' %minxsection[i])
        i += 1
        
        
        
        



print('######################\nSUMMARY OF SIMULATION\n######################')
print('Total Time: %0.1f minutes' %(t/60.))
print('Most Restricted pass: %0.1f ' %(t/60.))

endat = t -50

plt.figure()
plt.plot(dptrace[0:endat])
plt.xlabel('Time s')
plt.ylabel('DP [Pa]')

plt.figure()
plt.plot(ftrace[5:endat,0])

plt.plot(ftrace[5:endat,1])

plt.plot(ftrace[5:endat,2])
plt.xlabel('Time s')
plt.ylabel('friction factor [-]')

plt.figure()
plt.plot(fxtrace[0:endat,0], label = 'pass 1')

plt.plot(fxtrace[0:endat,1], label = 'pass 2')

plt.plot(fxtrace[0:endat,2], label = 'pass 3')
plt.legend()
plt.xlabel('Time s')
plt.ylabel('frost thickness')

plt.figure()
plt.plot(mdottrace[0:endat])
plt.xlabel('Time s')
plt.ylabel('kg/s')
