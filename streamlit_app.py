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

st.title("DJ COEFF ver 0.2")
st.image('https://raw.githubusercontent.com/bmgmri/DJ_coef/main/Smoke-01.png', width=100 )

uploaded_file = st.file_uploader("Choose a file")
st.info(       f"""
                👆 Upload a .xlsx excel file with an histogram in the first 2 columns
                """
        )
if uploaded_file is not None:
    #x, y   = np.genfromtxt( uploaded_file,  delimiter="\t", unpack=True)
    #st.write(x, y)
    
    import pandas as pd
    WS = pd.read_excel(uploaded_file)
    WS_array = np.array(WS)
    x=WS_array[:,0]
    y=WS_array[:,1]
    
##------------------------------------------------------------------
## FIT with initial shape  DATA 1 GAUSSIAN
##------------------------------------------------------------------
    def Gaussian(x, mean, h1 , sd ):
        return  h1 * np.exp(-0.5*((x-mean)/sd)**2)  

## get x of max
 
    smoothed= savgol_filter(y, 31, 3)
    
 
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
    
    fig, ax = plt.subplots()
    plt.title('Smooth line check')
    ax.fill_between(x, y, 0, alpha=0.7)
    ax.plot(x, smoothed,  lw=2, c='k')
    plt.vlines(x0, 0, 1.2*ymax, colors='gray', linestyles='dashed')
    st.pyplot(fig)
    #print(idmax, x0,ymax)

    guess = [x0, ymax, x[-1]/10 ]
    popt , pcov  = curve_fit(  Gaussian, colax, colay, p0=guess , bounds=([x0, 0, 0], np.inf))

    fig, ax = plt.subplots()
    plt.title('Fitting of half gaussian')
    ax.plot(colax, colay,  lw=2, c='k')
    ax.plot(colax , Gaussian(colax, *popt), label='0 DFO', lw=2, c='r')
    plt.savefig('curves.png', dpi=200 )
    st.pyplot(fig)

    fig, ax = plt.subplots()
    plt.title('Final plot:  Gaussian vs total')
    #ax.plot(x, y,  lw=2, c='k')
    ax.fill_between(x, y, 0, alpha=0.7)
    ax.plot(x , Gaussian(x, *popt), label='0 DFO', lw=2, c='r')
    #ax.plot(x , y - Gaussian(x, *popt), label='0 DFO', lw=2, c='k')
    plt.savefig('fit.png', dpi=200 )
    st.pyplot(fig) 

    st.success('FITTING FINISHED, CHECK RESULTS: ')
    
    st.write()
    st.write("--------------------------------")
    st.write("   Fit Results : ")    
    st.write("Center    = ",'{:10.3f}'.format(popt[0]) )
    st.write("Amplitude = ",'{:10.3f}'.format(popt[1]) )
    st.write("SD        = ",'{:10.3f}'.format(popt[2]) )
    st.write("--------------------------------")
    
    # CALCULATE INTEGRALS

    totalarea=trapz(y, x)
    gaussarea=trapz(Gaussian(x, *popt),x)
    percentage=100*gaussarea/totalarea
    djcoeff=gaussarea/totalarea
    
    st.write()
    st.write(" GAUSS AREA =  "         , '{:18.3f}'.format(gaussarea) )
    st.write(" TOTAL AREA =  "         , '{:18.3f}'.format(totalarea) )
    st.write(" PERCENTAGE_GAUSS % =  " , '{:18.3f}'.format(percentage) )
    st.write(" DJ COEFF           =  gaussarea/totalarea = " , '{:18.3f}'.format(djcoeff) )
    
    st.write("--------------------------------")
    
    st.success('NORMAL TERMINATION -> Agur !')

 
