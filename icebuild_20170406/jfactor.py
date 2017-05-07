# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 16:00:47 2017

@author: pretorj
"""
import numpy as np

def j(Red,N,Pt,Ac,Ao,Fp,D,L):
    "(Reynolds number, Number of passes, Transverse tube pitch,   )
    fin_thick = 0.0002
    Dc = D + 2*fin_thick
    Dh = 4*Ac*L/Ao
    P1 = 1.9 - 0.23*np.log(Red)
    P2 = -0.236 + 0.126*np.log(Red)
    P3 = - 0.361 - 0.042*N/(np.log(Red))+0.158*np.log(N*(Fp/Dc)**0.41)
    P4 = - 1.224 - 0.076*((P1/Dh)**1.42)/np.log(Red)
    P5 = -0.083 + 0.058*N/np.log(Red)
    P6 = - 5.735 + 1.21*np.log(Red/N)
    
    j = 0.086*Red**P3*N**P4*(Fp/Dc)**P5*(Fp/Dh)**P6*(Fp/Pt)**(-0.93)
    
    
    return(j)