# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 09:41:06 2017

@author: pretorj
"""
import numpy as np
import matplotlib.pylab as plt
import vapourmass as vm
##############################################################################
##############################################################################
#def Dab(T):
#    # From da Silva Thesis [2012] applicable for 50 < rho_f < 400
#    Dab = (0.1326*T - 14.042)*10**-6
#    
#    return(Dab)
    
def Dab(T, P = 101325., T2 = 298.15, P2 = 101325.):
    #source: Cengel, Heat and mass transfer a practical approach 3rd ed.,
    #pp. 780-781
    Dab2= 2.5*10**-5
    T = T + 273.15
    Dab1 = Dab2*P2/P*(T/T2)**(3/2)
    
    return(Dab1)    

##############################################################################
##############################################################################
    
def kf(rho_f): 
    # From da Silva Thesis [2012] applicable for 50 < rho_f < 400
    k = 0.132 + 3.13e-4*rho_f +1.6e-7*rho_f**2
    
    return(k)

##############################################################################
##############################################################################
    
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
    
##############################################################################
##############################################################################

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

##############################################################################
##############################################################################
    
def Le(T,P = 101325.):
    
    T = np.array(T)
    lewisnr = alpha(T)/Dab(T)
    
    return(lewisnr)    

##############################################################################
##############################################################################

def cp(T):
    #source: Cengel, Heat and mass transfer a practical approach 3rd ed.,
    #pp. 860
        
    Tset = [-150,-100, -50, -40, -30, -20, -10, 10, 15, 70, 80, 90, 100, 120,
            140, 160, 180, 200,250, 300, 350, 400, 450, 500, 600, 700, 800,
            900, 1000, 1500, 2000]
              
    Cpset= [983, 966, 999, 1002, 1004, 1005, 1006, 1006, 1007, 1007, 1008 ,
            1008, 1009, 1011, 1013, 1016, 1019, 1023, 1033, 1044, 1056, 
            1069, 1081, 1093, 1115, 1135, 1153, 1169, 1184, 1234, 1264]            
            
    return(np.interp(T,Tset,Cpset))

##############################################################################
##############################################################################
    
def k(T):
    T = T + 273.15
    kis = (2.334*10**-3*T**(3./2.))/(164.54 + T)
    
    return(kis)

##############################################################################
##############################################################################
    
    
def alpha(T, P = 101325.0):
    
    
    alp = k(T)/(rho(T,P)*cp(T))
    
    return(alp)

##############################################################################
##############################################################################
    
def Tii(ho,Af,rho,cpa,V,Tfs,Ti, n = 1):
    mm = -n*ho*Af/(rho*cpa*V)
    Tii = Tfs - (Tfs-Ti)*np.exp(mm)
    return(Tii)

##############################################################################
##############################################################################
    
def wii(ho,Af,rho,cpa,V,Tfs,Ti, wi, wsat, Le , n = 1):
    
    
    mm = -n*ho*Af/(rho*cpa*V*Le**(2/3.))
    wii = wsat - (wsat-wi)*np.exp(mm)  # wsat is humidity ratio at Tfs
    return(wii)    

##############################################################################
##############################################################################
def Tfsi(Qsens,Qlat,xfrost,kfrost,rhoa,Asurf,wsats,wsatf):
    pass
    

##############################################################################
##############################################################################

def rho(T,P = 101325):
    "(Temp (C), P (Pa)- Ideal gas law)"
    R =  287.05
    T = T + 273.15
    density = P/(R*T)
    return(density)
    
##############################################################################
##############################################################################
def frostbuild(mass_water,rho_ice,Lt,Di):
    
    #mass_water = 0.008  # kg
    #rho_ice = 400       # kg/m^3
    #Lt= 0.3              # m
    #Di= 0.008           # m

    # solves pi*Lt*Xf^2+pi*lt*dt*Xf-mw/rho_ice
    iceeq = [np.pi*Lt, np.pi*Lt*Di, -mass_water/rho_ice]
    x1,x2 = np.roots(iceeq) 
    return(x2)
##############################################################################
##############################################################################
    
    

V = 0.00875
ho = 200.
isv = 334.e3
Lt = 0.25
Di0 = 0.008
Af = np.pi*Di0*Lt
Tfs = -3.
cpa = 1005.
Tini = 5
RHini = 0.7
N = 11

T = np.zeros(N)
T[0] = Tini
rho1 = rho(T[0])
W = np.zeros(N)
W[0] = vm.vapourmass(Tini,RHini)
RH = np.zeros(N)
RH[0] = vm.relhumid(Tini,W[0])
moisturedeposit = np.zeros(N)
qlat = np.zeros(N)
qsen = np.zeros(N)
Tdew = np.zeros(N)
rho_frost = np.zeros(N)



for i in np.arange(1,N):
    rho1 = rho(T[i-1]) 
    T[i] = Tii(ho,Af,rho1,cpa,V,Tfs,T[i-1])
    W[i] = wii(ho,Af,rho1,cpa,V,Tfs,T[i-1],W[i-1],vm.vapourmass(Tfs,1),Le(Tfs))
    RH[i] = vm.relhumid(T[i],W[i])
    moisturedeposit[i] = W[i-1] - W[i]
    qlat[i] = moisturedeposit[i]*V*isv
    qsen[i] = (T[i-1]-T[i])*cpa*V
    Tdew[i] = Tdp([T[i]],(RH[i]*100))
    rho_frost[i] = rho_f(Tfs,Tdew[i])
    
    
min =180
iter = min*60    
mfrost = np.zeros([iter,N])
frost_thick = np.zeros([iter,N])
for t in np.arange(1,iter):
    # calculate grams per pass accumulative
    
    for i in np.arange(1,N):    
        mfrost[t,i] = mfrost[t-1,i] + moisturedeposit[i]*V
        frost_thick[t,i] = frostbuild(mfrost[t,i],rho_frost[i],Lt,Di0)
    
    

plt.plot(T,'x-')
plt.plot([0,N],[Tfs]*2,'g-')  
plt.xlabel('Pass',fontsize = 18)
plt.ylabel('Temp',fontsize = 18)
plt.tick_params(axis='both', labelsize = 14)
plt.tight_layout()
plt.savefig('./pptemp.pdf',dpi = 400)

plt.figure()
plt.plot(W,'x-')  
plt.xlabel('Pass',fontsize = 18)
plt.ylabel('H (kgv/kgair)',fontsize = 18)
plt.tick_params(axis='both', labelsize = 14)
plt.tight_layout()
plt.savefig('./ppabs.pdf',dpi = 400)

plt.figure()
plt.plot(RH,'x-')  
plt.xlabel('Pass',fontsize = 18)
plt.ylabel('RH (%)',fontsize = 18)
plt.tick_params(axis='both', labelsize = 14)
plt.tight_layout()
plt.savefig('./ppRH.pdf',dpi = 400)


plt.figure()
plt.plot((frost_thick[-1,1:]*1000),'x-', rasterized = True)  
plt.tick_params(axis='both', labelsize = 14)
plt.xlabel('Pass',fontsize = 18)
plt.ylabel('$\delta t_{frost}$ (mm)',fontsize = 18)
plt.tight_layout()
plt.savefig('./perpassthick.pdf',dpi = 400)


plt.figure()
for i in np.arange(1,11):
    
    plt.plot(np.arange(1,iter)/60,mfrost[1:,i]*1000,'x' , rasterized = True, label = 'Pass %s' % i)

plt.xlabel('Time (min)',fontsize = 18)
plt.ylabel('Frost mass (g)',fontsize = 18)
plt.annotate('Total mass = %s g' %round(sum(mfrost[-1,:]*1000)), xy = (40,max(mfrost[:,1]*1000-2)),fontsize = 18)
plt.legend(loc =2)
plt.tick_params(axis='both', labelsize = 14)
plt.tight_layout()
plt.savefig('./fmass.pdf',dpi = 400)

plt.figure()
for i in np.arange(1,11):
    
    plt.plot(np.arange(1,iter)/60,frost_thick[1:,i]*1000,'x', rasterized = True, label = 'Pass %s' % i)

plt.xlabel('Time (min)',fontsize = 18)
plt.ylabel('Frost Thickness',fontsize = 18)
plt.annotate('Total mass = %s g' %round(sum(mfrost[-1,:]*1000)), xy = (40,max(mfrost[:,1]*1000)))
plt.legend(loc =2)
plt.tick_params(axis='both', labelsize = 14)
plt.tight_layout()
plt.savefig('./fthick.pdf',dpi = 400)
    
    


    

