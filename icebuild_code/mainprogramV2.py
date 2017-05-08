import geometry as geom
import fancurvemodel as fan
import airproperties as air
import frostproperties as frost
import controlvolume as cor
import heatandfriction as jf
import numpy as np
import matplotlib.pylab as plt


### Initial parameters
Te = -10  # Evap surface temperature
Treturn = -5  # Return air temperature
RHreturn = 0.7 # Relative humidity of return air
frostx = 10e-6  # Non zero frost thickness starting condition
dt = 1          # Seconds 
targetminerrorTfs = 0.01 # maximum difference between assumed and calculated frost surface temperature
dperror = 0.1
maxtime = 24 # hours

### Evap geometry Unit m
Passes = 4 
Finpitch = [  0.01, .009 ,.008, 0.007]
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
mdottrace = np.zeros(seconds)
dptotal = np.zeros(seconds)

ftrace = np.zeros((seconds,Passes))
fxtrace = np.zeros((seconds,Passes))
htrace = np.zeros((seconds,Passes))

surfacearea = np.zeros((seconds,Passes))
minxsection = np.zeros((seconds,Passes))
dpperpass = np.zeros((seconds,Passes))


T = np.zeros(Passes+1) # +1 To allow for the inlet control volume
Ts = np.zeros(Passes)
Ts = Te # update to reflect frost surface temperature
w = np.zeros(Passes+1)
w[0] = air.vapourmass(Treturn,RHreturn)
frostx = np.zeros(Passes)


### Fan curve
nofrost_resistancecurve = 0. # update!
dpevap = 6.   # assume initial pressure drop to get initial mass flow rate
dptotal[t] = nofrost_resistancecurve + dpevap

while dptotal[t] < pmax:
    
    t = t + dt      # increment time
    dptrace[t] = dptotal[t]
    mdot = fan.fancurve(dptotal[t])
    mdottrace[t] = mdot
       
    i = 0
    surfaceareatotal = 0 
    Tair = Treturn
    RH = RHreturn
    dptimestep = 0
    T[0] = Treturn
    
    
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
        Cp_air  = air.cp(Tair)
        Lewis   = air.Le(Tair)
        alp     = air.alpha(Tair)
        
        ## Frost Properties
        rho_f   = frost.rho_f(Ts,Tdp)
        kfrost = frost.kf(rho_f)
        
        ## Flow Regime and Properties
        Vmax = mdot/(rho_air*minxsection[t,i])
        
        Vmean = mdot/(rho_air*Width*(0.025))
        Re   = rho_air*Vmax*(TubeDiameter)/visc
        
        ## Heat transfer and pressure drop
        j, f, Dh= jf.jffactors(Finpitch[i],tubepitch,0.05,TubeDiameter+frostx[i]*2,1,Re,control_vol_h,minxsection[t,i],surfacearea[t,i])
        h = j*rho_air*Vmax*Cp_air/(Pr**0.66)

        
        dpperpass[t,i] = f * control_vol_h/Dh*2*rho_air*Vmax**2
        
        ftrace[t,i] = f 
        htrace[t,i] = h
        
        ## Control volume interfaces
        T[i+1] = cor.Tii(h,surfacearea[t,i],mdot,Cp_air,Ts,T[i])
        w[i+1] = cor.wii(h,surfacearea[t,i],mdot,Cp_air,Ts,T[i],w[i],air.vapourmass(Ts,1),Lewis)
        qsens =  cor.qsens(T[i],T[i+1],mdot,Cp_air)
        qlat  = cor.qlat(w[i],w[i+1],mdot)
        frostmass = (w[i]-w[i+1])*mdot
        frostvol = frostmass/rho_f/30
        frostlayer = geom.dfpersegment(frostvol, TubeDiameter,Finpitch[i])
        frostx[i] = frostx[i] + frostlayer
        ## Evaporator totals
        fxtrace[t,i] = frostx[i]
        dptotal[t] = np.sum(dpperpass[t,0:Passes])
                        
 
        i += 1
        
        
####### PLOT RESULTS #########################################################
startat = 0
endat = t 
###
plt.figure()
for i in np.arange(0,Passes):
    plt.plot(minxsection[startat:endat,i],label = 'pas %s' %i)
    plt.xlabel('Time [s]')
    plt.ylabel('Min cross sectional [m^2]')
plt.legend()
###
plt.figure()
for i in np.arange(0,Passes):
    plt.plot(surfacearea[startat:endat,i],label = 'pas %s' %i)
    plt.xlabel('Time [s]')
    plt.ylabel('Wetted surface area [m^2]')
plt.legend()
###
plt.figure()
for i in np.arange(0,Passes):
    plt.plot(dpperpass[startat:endat,i],label = 'pas %s' %i)
    plt.xlabel('Time [s]')
    plt.ylabel('Pressure [Pa]')
plt.legend()
###
plt.figure()
plt.plot(dptotal[:t])
plt.xlabel('Time [s]')
plt.ylabel('Total Pressure [Pa]')
###
plt.figure()
for i in np.arange(0,Passes):
    plt.plot(ftrace[startat:endat,i],label = 'pas %s' %i)
    plt.xlabel('Time [s]')
    plt.ylabel('friction factor [-]')
plt.legend()
###
plt.figure()
for i in np.arange(0,Passes):
    plt.plot(htrace[startat:endat,i],label = 'pas %s' %i)
    plt.xlabel('Time [s]')
    plt.ylabel('h [W/k]')
plt.legend()



