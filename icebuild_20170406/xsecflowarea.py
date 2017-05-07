# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 15:49:13 2017

@author: pretorj
"""

def axpsec(dfrost,dtube=0.008 ,finpitch = 0.01 , finwidth = 0.025, finheight = 0.025, finthickness = 0.0002, gap = 0.0):
    ''' This function returns the cross sectional flow area per section of evap'''
    ax = 2*(finpitch/2-dfrost - finthickness/2)*(finwidth/2-dtube/2-dfrost)+2*gap*finpitch/2
    
    return(ax)