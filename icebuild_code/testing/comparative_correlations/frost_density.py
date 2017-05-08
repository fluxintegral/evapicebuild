# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 11:16:58 2017

@author: pretorj
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 15:28:27 2017

@author: pretorj
Frost Growth model
   
"""

import numpy as np
import matplotlib.pylab as plt
import tdewp

RH = 100
Tair =np.array( [5])

##################################################################
#[1] First Principle modeling of frost accumulation on fan-supplied tube-fin
#    evaporators, D.L. Da Silva,CJ.L. Hermes, C Melo,
#    Applied Thermal Engineering, 2011, vol 30, 2616-2621.
a = 494
b = 0.11
c = -0.06

Tf1 = np.arange(0, -33,-0.05)
Tdew_i = tdewp.Tdp(Tair,RH)
rho_f1 = a*np.exp(b*Tf1+c*Tdew_i)  #[1]
##################################################################
#[2] Study of frost formation based on a theoretical model of the frost layer,
#    Hayashi Y., Aoki A., Yuhara H., Heat Transfer-Japanese Research,
#    1977, vol. 6 pp, 79-94 

Tf2 = np.arange(-18.6,-5,0.05)
rho_f2 = 650*np.exp(0.277*Tf2)   #[2] tested in 2m/s to 6m/s airflow

##################################################################
#[3] A dimensionless correlation for the frost density, C.J.L Hermes,
#    V.S do Nascimento Jr. F.R. de Loyola, 22nd International Conference
#    of mechanical engineering (COBEM 2013), Nov 3-7,2013, Ribeirao Preto,
#    Brazil, pp 2649-2654


a = 207
b = 0.266
c = -0.0615
Tf3 = np.arange(-15, -5,0.05)
Tdew_i = tdewp.Tdp(Tair,RH)
rho_f3 = a*np.exp(b*Tf3+c*Tdew_i)  #[3]
##################################################################
#[4] Wang et al, 2012


Tdew = tdewp.Tdp(Tair,RH)
c1=0.70132-0.11346*Tdew-0.00203*Tdew**2
c2=1.4333-0.17389*Tair-0.00722*Tair**2
Tf4 = np.arange(-15,-5,0.05)
rho_f4 = 650*np.exp(0.277*Tf4)*c1*c2   #[2] tested in 2m/s to 6m/s airflow

##################################################################
#[5] In-situ study of frosting and defrosting processes in tube-fin
#    evaporators of household refrigerating appliances, International Journal
#    of refrigeration ,vol 34, 2011, pp 2031-2041, F.T. Knabben, C.J.L. Hermes,
#    C. Melo


Tdew = tdewp.Tdp(Tair,RH)
Tf5 = np.arange(-15,-5,0.05)
rho_f5 = 492.95*np.exp(-0.053*(Tdew-Tf5))

##################################################################

#[6] A Dimensionless correlation for the frost density,International congress
# of mechanical engineering COBEM 2013, C.J.L. Hermes, V.S. do Nascimento Jr.
# F.R. de Loyola

Tdew = tdewp.Tdp(Tair,RH)
Tf5 = np.arange(-15,-5,0.05)
rho_f5 = 492.95*np.exp(-0.053*(Tdew-Tf5))

##################################################################


plt.figure()
plt.plot(Tf1,rho_f1, label =  'da Silva et al.')
plt.plot(Tf2,rho_f2,'k', label =  'Hayashi et al.')
plt.plot(Tf3,rho_f3,'r', label =  'do nascimento Jr. et al.')
plt.plot(Tf4,rho_f4,'k--', label =  'Wang et al.')
plt.plot(Tf5,rho_f5,'r--', label =  'Knabben et al.')

plt.xlabel('$T_{surf}$ [C]', fontsize = 18)
plt.ylabel(' $\\rho_{frost}$  ', fontsize = 18)
plt.tick_params(axis='both', labelsize = 14)
plt.legend(loc = 2)
plt.tight_layout()

#plt.savefig('./0to25_sensirion_pitot_capability.pdf')