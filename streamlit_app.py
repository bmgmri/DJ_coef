#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 14:27:27 2019

@author: mriuser
"""
import streamlit as st
import numpy as np
#import sys
from matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import trapz, simps
from scipy.signal import savgol_filter


## Read data  -> read Ascii file -> reshape
datain=sys.argv[1]
#datain='50.dat'
x, y   = np.genfromtxt( datain,  delimiter="\t", unpack=True)


##------------------------------------------------------------------
## FIT with initial shape  DATA 1 GAUSSIAN
##------------------------------------------------------------------

def Gaussian(x, mean, h1 , sd ):
    return  h1*(1/sd*np.sqrt(2*np.pi) ) * np.exp(-0.5*((x-mean)/sd)**2)  

## get x of max
smoothed= savgol_filter(y, 31, 3)
fig, ax = plt.subplots()
ax.plot(x, smoothed,  lw=2, c='k')

'''
idmax = np.argmax(smoothed)
ymax = np.amax(smoothed)
x0=x[idmax]
colax=x[idmax:]
colay=y[idmax:]

'''
## filtramos el primer 20% de datos para buscar el maximo
shift= x.shape[0] // 5
#print(x.shape)
# altura y posicion del maximo
idmax = np.argmax(smoothed[shift:])
ymax = np.amax(smoothed[shift:])
x0=x[shift+idmax]

# separamos la curva a partir del maximo
colax=x[shift+idmax:]
colay=y[shift+idmax:]

#print(idmax, x0,ymax)


guess = [x0, ymax, x[-1]/10 ]
popt , pcov  = curve_fit(  Gaussian, colax, colay, p0=guess , bounds=([x0, 0, 0], np.inf))

fig, ax = plt.subplots()
ax.plot(colax, colay,  lw=2, c='k')
ax.plot(colax , Gaussian(colax, *popt), label='0 DFO', lw=2, c='r')
plt.savefig('curves.png', dpi=200 )
st.pyplot(fig)

fig, ax = plt.subplots()
#ax.plot(x, y,  lw=2, c='k')
ax.fill_between(x, y, 0, alpha=0.7)
ax.plot(x , Gaussian(x, *popt), label='0 DFO', lw=2, c='r')
#ax.plot(x , y - Gaussian(x, *popt), label='0 DFO', lw=2, c='k')
plt.savefig('fit.png', dpi=200 )
st.pyplot(fig) 

'''
print()
print("--------------------------------")
print("   Fit Results DATA 0: ")
print("--------------------------------")
print("Mean    = ",popt[0] )
print("Amplitude  = ",popt[1] )
print("SD      = ",popt[2] )
'''
# CALCULATE INTEGRALS

totalarea=trapz(y, x)
gaussarea=trapz(Gaussian(x, *popt),x)
percentage=100*gaussarea/totalarea
print(datain, '{:18.3f}'.format(totalarea), '{:18.3f}'.format(gaussarea), '{:18.3f}'.format(percentage))

'''
print()
print("--------------------------------")
print("   Fit Results DATA 0: ")
print("--------------------------------")
print("Mean       = ",popt[0] )
print("Amplitude  = ",popt[1] )
print("SD         = ",popt[2] )
print("Mean    = ",popt[3] )
print("Amplitude  = ",popt[4] )
print("SD      = ",popt[5] )
print("Offset     = ",popt[6] )
'''
#print(datain, *popt)
