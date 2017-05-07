# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 12:06:10 2017

@author: pretorj
"""

from vapourmass import vapourmass

flowrate = 12.0  # L/s
rho = 1.3
mdot = flowrate/1000.0*rho # Convert L/s to kg/s

H = vapourmass(4,.8)-vapourmass(-5,1)  # kg water per kg/air

mwateraccum = mdot * H  # kg h2o per sec 
mwateraccum = mwateraccum*1000 # g/s
mwaterhour = mwateraccum*3600

Houtside = vapourmass(32,.85)-vapourmass(4,.8)  # kg water per kg/air

print ("Air L/s = {0:0.1f} \nAir kg/s = {1:0.3f} \nDH2O = {2:0.7f} g/s \nDH2O = {3:0.4f} g/h".format(flowrate,mdot,mwateraccum, mwaterhour))

