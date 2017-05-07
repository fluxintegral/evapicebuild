# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 11:20:35 2017

@author: pretorj
frost thickness on tube
"""
import numpy as np
import vapourmass as vm
import airproperties as air
import matplotlib.pylab as plt




###############################################################################
###############################################################################
def Tdp(T,RH):
        
    T = np.array(T)
    for i in range(0,len(T)):
                  
        if T[i] > 0. and T[i] <= 50.:
            a = 6.1121 # millibar
            b = 17.368
            c = 238.88 # degC
            
                
        if T[i] >= -40. and T[i] <= 0.:
            a = 6.1121 # millibar
            b = 17.966
            c = 247.15 # degC

        y =np.log(RH/100.0)+b*T/(c+T)   # Magnus Formula
        Tdewpoint = c*y/(b-y)           # Magnus Formula

    return(Tdewpoint)            
###############################################################################    
###############################################################################
def rho_f(Ts,Tdewpoint):
    
#[1] First Principle modeling of frost accumulation on fan-supplied tube-fin
#    evaporators, D.L. Da Silva,CJ.L. Hermes, C Melo,
#    Applied Thermal Engineering, 2011, vol 30, 2616-2621.
    a = 494
    b = 0.11
    c = -0.06
    Ts = np.array(Ts)
    
    rho = a*np.exp(b*Ts+c*Tdewpoint)  #[1]    
    
    return(rho)

###############################################################################
###############################################################################
def frostbuild(mass_water,rho_ice,Di):
    
    #mass_water = 0.008  # kg
    #rho_ice = 400       # kg/m^3
    Lt= 0.3              # m
    #Di= 0.008           # m

    # solves pi*Lt*Xf^2+pi*lt*dt*Xf-mw/rho_ice
    iceeq = [np.pi*Lt, np.pi*Lt*Di, -mass_water/rho_ice]
    x1,x2 = np.roots(iceeq) 
    return(x2)

###############################################################################
###############################################################################
m_air= 0.012
Te = -5


minutes = 60
iter = 60 * minutes

hf = np.zeros(iter)
dtotal = np.zeros(iter)
mgtotal = np.zeros(iter+1)
D = 0.008
mgtotal[0] = 0 
#hf2 = np.zeros(iter)
#hf2[0] = 0
#Di2 = 0.008
#hf3 = np.zeros(iter)
#hf3[0] = 0
#Di3 = 0.008
#hf4 = np.zeros(iter)
#hf4[0] = 0
#Di4 = 0.008

T= -10.
V = .5

Re_d = air.rho(T) * V * D/ air.mu(T)
print (Re_d)

for i in np.arange(1,iter):
##############################################################################        
    
    Hdep = vm.vapourmass(5,0.70) - vm.vapourmass(4,0.72) # kgv/kgair
    mg = Hdep*m_air  # mass of frost accumulated per second
    rho_ice = rho_f(Te,Tdp([3],75))  # density of frost
    hf[i] = frostbuild(mg,rho_ice,D+sum(hf)) # hf is the height of the frost layer based on the diameter di
    dtotal[i] = D + sum(hf)        
    #Di = hf[i] 
    
    mgtotal[i+1] =  mgtotal[i] + mg
    
    
    
    

plt.figure()
plt.plot(np.arange(iter)/60.,hf*1000)
#plt.plot(np.arange(iter)/60.,hf2*1000,'k--')
#plt.plot(np.arange(iter)/60.,hf3,'r--')
#plt.plot(np.arange(iter)/60.,hf3,'g--')
plt.xlabel('time [min]')
plt.ylabel('frost layer added thickness [mm]')

plt.figure()
#plt.plot([0,i/60],np.array([0.008,0.008])*1000, label = 'Tube')
plt.plot(np.arange(iter)/60.,dtotal*1000) 
plt.xlabel('time [min]')
plt.ylabel('Effective Diameter [mm]')

plt.figure()
plt.plot(np.arange(iter)/60.,(dtotal*1000-8)/2) 
plt.xlabel('time [min]')
plt.ylabel('Frost Thickness [mm]')

plt.figure()
plt.plot(mgtotal*1000) 
plt.xlabel('iter')
plt.ylabel('Frost mass (g)')
    
    
###############################################################################    
#    Hdep2 = vm.vapourmass(2,0.95) - vm.vapourmass(-2,0.99)
#    mg2 = Hdep2*m_air
#    rho_ice = rho_f(Te,Tdp([3],99))
#    hf2[i] = frostbuild(mg2,rho_ice,Di2) + hf2[i-1]
#    #hf[i] = 1/(rho*L*x)*mg*dt + hf[i-1] # flat plate
#    Di2 = Di2 + hf2[i]
###############################################################################
#    rho_ice = rho_f(-15,Tdp([-2.5],99))
#    Hdep3 = vm.vapourmass(-2,0.99) - vm.vapourmass(-3,0.99)
#    mg3 = Hdep3*m_air
#
#    hf3[i] = frostbuild(mg3,rho_ice,Di3) + hf3[i-1]
#    
#    Di3 = hf3[i]
#    
###############################################################################
#    rho_ice = rho_f(-15,Tdp([-3.5],99))
#    Hdep4 = vm.vapourmass(-3,0.99) - vm.vapourmass(-3.8,0.99)
#    mg4 = Hdep4*m_air
#
#    hf4[i] = frostbuild(mg4,rho_ice,Di4) + hf4[i-1]
#    
#    Di4 = hf4[i]    
    



#plt.figure()
#plt.plot(np.arange(iter)/60.,hf*1000)
##plt.plot(np.arange(iter)/60.,hf2*1000,'k--')
##plt.plot(np.arange(iter)/60.,hf3,'r--')
##plt.plot(np.arange(iter)/60.,hf3,'g--')
#plt.xlabel('time [min]')
#plt.ylabel('frost thickness [mm]')
#
#plt.figure()
#plt.plot(np.arange(iter)/60.,dtotal)    


