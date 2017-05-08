# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 10:47:07 2017

@author: pretorj
Conductivity of frost 
K.S. Lee, W.S. Kim, T.H. Lee, A one-dimensional model for frost formation on a 
cold flat surface, International Journal of Heat and Mass Transfer 40 (1997),
4359-4365.

rho_f defined in 1D sense as rho_f = m_frost/(Thickness*Area)

"""
import numpy as np
import matplotlib.pylab as plt

def kfrost(rho_f):
    
    rho_f = np.array(rho_f)
    kf = 0.132 + 3.13*10**(-4)*rho_f + 1.6*10**(-7)*rho_f**2


    return(kf)     

def kdusen(rho_f):
    # Van Dusen (1929) valid for 243K < T < 273K, Correlation known for providing the lower bound in general
    # via Kadula (2011) pp 11
    
    rho_f = np.array(rho_f)
    k = 0.029 + 0.403*10.**-3.*rho_f+0.2367*10.**-8.*rho_f**3.
    
    return(k)
    
def kyonko(rho_f):
    
    rho_f = np.array(rho_f)
    k = 0.024248 + 0.731*10.**-3.*rho_f+0.1183*10.**-5.*rho_f**2.    
    
    return(k)
    
def kostin(rho_f):
    
    rho_f = np.array(rho_f)
    
    k = -8.71*10**-3. + 4.39*10.**-4.*rho_f + 1.05*10.**-6.*rho_f**2.    
    
    return(k)



# Begin development checks
compare = [kfrost(range(50,500)), kdusen(range(50,500)), kyonko(range(50,500)), kostin(range(50,500))  ]  

plt.plot(range(50,500),compare[0][:], label = 'lee')
plt.plot(range(50,500),compare[1][:], label = 'dunsen')
plt.plot(range(50,500),compare[2][:], label = 'yonko')
plt.plot(range(50,500),compare[3][:], label = 'ostin')
plt.ylabel('$k_{frost}$', fontsize = 18 )
plt.xlabel('$ \\rho_{frost}$', fontsize = 18)
plt.tick_params(axis='both', labelsize = 14)
plt.legend(loc = 2)
plt.tight_layout()
# End development checks


