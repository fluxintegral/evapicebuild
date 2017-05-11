import geometry as geom
import fancurvemodel as fan
import airproperties as air
import frostproperties as frost
import controlvolume as cor
import heatandfriction as jf
import numpy as np
import matplotlib.pylab as plt


### Initial parameters
Te = -22.0  # Evap surface temperature
Treturn = -17  # Return air temperature
RHreturn = 0.8 # Relative humidity of return air
dt = 1          # Seconds 
targetminerrorTfs = 0.01 # maximum difference between assumed and calculated frost surface temperature
frostthick = 10e-6
maxtime = 24 # hours

### Evap geometry Unit m
Passes = 5
Finpitch = [0.008, .008, 0.008, 0.008, 0.008 ]
TubeDiameter = 0.008 
Width = 0.314 # endplate to endplate
tubepitch = 0.027
control_vol_h = 0.027


##################

pmax = 65   # maximum pressure drop desired or derived from max compartment temperature distribution requirement

## Initialise variables
t = 0           # Time 0s
Ts = Te         # Frost == Evap Surface Temp
seconds = np.round(maxtime*3600)
dptrace = np.zeros(seconds)
mdot = np.zeros(seconds)
qtotal = np.zeros(seconds)
dptotal = np.zeros(seconds)
h = np.zeros((seconds,Passes))
qtotalpp =np.zeros((seconds,Passes))
ftrace = np.zeros((seconds,Passes))
fxtrace = np.zeros((seconds,Passes))
htrace = np.zeros((seconds,Passes))
qsens = np.zeros((seconds,Passes))
qlat = np.zeros((seconds,Passes))
surfacearea = np.zeros((seconds,Passes))
minxsection = np.zeros((seconds,Passes))
dpperpass = np.zeros((seconds,Passes))
tau = np.zeros((seconds,Passes))
epsilon = np.zeros((seconds,Passes))
Tfs = np.zeros((seconds,Passes))
rho_f = np.zeros((seconds,Passes))
T = np.zeros((seconds,Passes+1)) # +1 To allow for the inlet control volume
Ts = np.zeros(Passes)
Cp_air = np.zeros(Passes)
Ts = Te # update to reflect frost surface temperature
w = np.zeros((seconds,Passes+1))
w[:,0] = air.vapourmass(Treturn,RHreturn)
frostx = np.zeros(Passes)

Tfs[0,:] = Te
epsilon[0,:]=1

### Fan curve
nofrost_resistancecurve = 0. # update!
dpevap = 12.   # assume initial pressure drop to get initial mass flow rate
dptotal[t] = nofrost_resistancecurve + dpevap

while dptotal[t] < pmax:
    
   t = t + dt      # increment time
   
   mdot[t] = fan.fancurve((dptotal[t-1]))
    
       
   i = 0
   surfaceareatotal = 0 
   Tair = Treturn
   RH = RHreturn
   T[:,0] = Treturn
    
    
   while i < Passes:
        
        ## Calculate geometric properties of pass        
        surfacearea[t,i] = geom.asurfperpass(frostx[i],TubeDiameter,Width,Finpitch[i])
        minxsection[t,i] = geom.axperpass(frostx[i],TubeDiameter,Width,Finpitch[i])
                
        ## Air properties
        visc    = air.mu(Tair)
        rho_air = air.rho(Tair)
        Pr      = 0.73
        k_air   = air.k(Tair)
        Tdp     = air.Tdp([Tair],RH)
        D       = air.Dab(Tair)
        Cp_air[i]  = air.cp(Tair)
        Lewis   = air.Le(Ts)
        alp     = air.alpha(Tair)
        
        rho_ice = 916.7
        
        ## Frost Properties
        rho_f[t,i]   = frost.rho_f(Ts,Tdp)
        kfrost = frost.kf(rho_f[t,i])
        isv = 2258e3
        ## Flow Regime and Properties
        Vmax = mdot[t]/(rho_air*minxsection[t,i])
        
        Vmean = mdot[t]/(rho_air*Width*(0.025))
        Re   = rho_air*Vmax*(TubeDiameter)/visc
        
        ## Heat transfer and pressure drop
        j, f, Dh= jf.jffactors(Finpitch[i],tubepitch,0.05,TubeDiameter+frostx[i]*2,1,Re,control_vol_h,minxsection[t,i],surfacearea[t,i])
        h[t,i] = j*rho_air*Vmax*Cp_air[i]/(Pr**0.66)
        
        epsilon[t,i] = (rho_f[t,i]-rho_ice)/(rho_air-rho_ice)
        
        tau[t,i] = epsilon[t,i]/(1. - (1.- epsilon[t,i])**0.5)
        
        Le_star = Lewis*tau[t,i]/epsilon[t,i]        
        dpperpass[t,i] = f * control_vol_h/Dh*2*rho_air*Vmax**2
        
        ftrace[t,i] = f 
        htrace[t,i] = h[t,i]
        
        ## Control volume interfaces
        
        
        T[t,i+1] = cor.Tii(h[t,i],surfacearea[t,i],mdot[t],Cp_air[i],Tfs[t-1,i],T[t,i])
        w[t,i+1] = cor.wii(h[t,i],surfacearea[t,i],mdot[t],Cp_air[i],Tfs[t-1,i],T[t,i],w[t-1,i],air.vapourmass(Ts,1),Le_star)
        qsens[t,i] =  cor.qsens(T[t,i],T[t,i+1],mdot[t],Cp_air[i])
        qlat[t,i]  = cor.qlat(w[t,i],w[t,i+1],mdot[t])
        qtotalpp[t,i] = qsens[t,i] + qlat[t,i]
        frostmass = (w[t,i]-w[t,i+1])*mdot[t]
        frostvol = frostmass/rho_f[t,i]
        frostlayer = geom.dfpersegment(frostvol, TubeDiameter,Finpitch[i])
        frostx[i] = frostx[i] + frostlayer
               
        ## Evaporator totals
        fxtrace[t,i] = frostx[i]
        Tfs[t,i] = Te + (qsens[t,i] +qlat[t,i])*fxtrace[t,i]/ \
        (kfrost*surfacearea[t,i]) - rho_air*air.vapourmass(Ts,1)*isv*D/\
        (kfrost*tau[t,i])*(np.cosh(air.vapourmass(Tfs[t-1,i],1)/air.vapourmass(Te,1))-1)
        dptotal[t] = np.sum(dpperpass[t,0:Passes])
        
        if dptotal[t] < dptotal[t-1]:
            dptotal[t]= dptotal[t-1]
        
        qtotal[t] = np.sum(qtotalpp[t,0:Passes])
        i += 1
 
    
        
####### PLOT RESULTS #########################################################
startat = 1
endat = t 

####
plt.figure()
for i in np.arange(0,Passes+1):
    plt.plot(w[startat:endat,i],label = 'pas %s' %i)
    plt.xlabel('Time [s]')
    plt.ylabel('abs humid [kg/kg]')
plt.legend()
####
plt.figure()
for i in np.arange(0,Passes+1):
    plt.plot(T[startat:endat,i],label = 'pas %s' %i)
    plt.xlabel('Time [s]')
    plt.ylabel('Tempcv [C]')
plt.legend()
####
plt.figure()
for i in np.arange(0,Passes):
    plt.plot(qlat[startat:endat,i],label = 'pas %s' %i)
    plt.xlabel('Time [s]')
    plt.ylabel('Qlatent [W]')
plt.legend()
####
plt.figure()
for i in np.arange(0,Passes):
    plt.plot(qsens[startat:endat,i],label = 'pas %s' %i)
    plt.xlabel('Time [s]')
    plt.ylabel('Qsens [W]')
plt.legend()
###
plt.figure()
for i in np.arange(0,Passes):
    plt.plot(qtotal[:t])
    plt.xlabel('Time [s]')
    plt.ylabel('QTotal [W]')

###
plt.figure()
for i in np.arange(0,Passes):
    plt.plot(minxsection[startat:endat,i],label = 'pas %s' %i)
    plt.xlabel('Time [s]')
    plt.ylabel('Min cross sectional [m^2]')
plt.legend()
####
#plt.figure()
#for i in np.arange(0,Passes):
#    plt.plot(surfacearea[startat:endat,i],label = 'pas %s' %i)
#    plt.xlabel('Time [s]')
#    plt.ylabel('Wetted surface area [m^2]')
#plt.legend()
####
#plt.figure()
#for i in np.arange(0,Passes):
#    plt.plot(dpperpass[startat:endat,i],label = 'pas %s' %i)
#    plt.xlabel('Time [s]')
#    plt.ylabel('Pressure [Pa]')
#plt.legend()
###
plt.figure()
plt.plot(dptotal[:t])
plt.grid()
plt.xlabel('Time [s]')
plt.ylabel('Total Pressure [Pa]')
###
plt.figure()
plt.plot(mdot[:t])
plt.grid()
plt.xlabel('Time [s]')
plt.ylabel('mdot [kg/s]')
###
plt.figure()
for i in np.arange(0,Passes):
    plt.plot(fxtrace[startat:endat,i],label = 'pas %s' %i)
    plt.xlabel('Time [s]')
    plt.ylabel('Frost Thickness [-]')
plt.legend()
####
#plt.figure()
#for i in np.arange(0,Passes):
#    plt.plot(ftrace[startat:endat,i],label = 'pas %s' %i)
#    plt.xlabel('Time [s]')
#    plt.ylabel('friction factor [-]')
#plt.legend()
####
#plt.figure()
#for i in np.arange(0,Passes):
#    plt.plot(htrace[startat:endat,i],label = 'pas %s' %i)
#    plt.xlabel('Time [s]')
#    plt.ylabel('h [W/k]')
#plt.legend()



