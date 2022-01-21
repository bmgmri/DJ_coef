#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 14:27:27 2019

@author: mriuser
"""
import streamlit as st
import numpy as np
#import sys
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import trapz, simps
from scipy.signal import savgol_filter


## Read data  -> read Ascii file -> reshape
#datain=sys.argv[1]
#datain='50.dat'

def conv(x):
    return x.replace(',', '.').encode()

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    x, y   = np.genfromtxt( uploaded_file,  delimiter="\t", unpack=True)
    #st.write(x, y)

##------------------------------------------------------------------
## FIT with initial shape  DATA 1 GAUSSIAN
##------------------------------------------------------------------
    def Gaussian(x, mean, h1 , sd ):
        return  h1*(1/sd*np.sqrt(2*np.pi) ) * np.exp(-0.5*((x-mean)/sd)**2)  

## get x of max
    smoothed= savgol_filter(y, 31, 3)
    
    fig, ax = plt.subplots()
    plt.title('Smooth line check')
    ax.fill_between(x, y, 0, alpha=0.7)
    ax.plot(x, smoothed,  lw=2, c='k')
    st.pyplot(fig)
 
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

    
    st.write()
    st.write("--------------------------------")
    st.write("   Fit Results : ")    
    st.write("Center    = ",popt[0] )
    st.write("Amplitude = ",popt[1] )
    st.write("SD        = ",popt[2] )
    st.write("--------------------------------")
    
    # CALCULATE INTEGRALS

    totalarea=trapz(y, x)
    gaussarea=trapz(Gaussian(x, *popt),x)
    percentage=100*gaussarea/totalarea
    st.write()
    st.write(" GAUSS AREA = "         , '{:18.3f}'.format(gaussarea) )
    st.write(" TOTAL AREA = "         , '{:18.3f}'.format(totalarea) )
    st.write(" PERCENTAGE_GAUSS % = " , '{:18.3f}'.format(percentage) )
    
  

 
