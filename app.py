import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import trapz, simps
from scipy.signal import savgol_filter

###################################
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode

###################################

from functionforDownloadButtons import download_button

###################################


def _max_width_():
    max_width_str = f"max-width: 1800px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )

st.set_page_config(page_icon="✂️", page_title="DJ COEFF v 0.01")

# st.image("https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/285/balloon_1f388.png", width=100)
st.image(
    "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/285/scissors_2702-fe0f.png",
    width=100,
)

st.title("DJ COEFF")


c29, c30, c31 = st.columns([1, 6, 1])

with c30:

    uploaded_file = st.file_uploader(
        "",
        key="1",
        help="To activate 'wide mode', go to the hamburger menu > Settings > turn on 'wide mode'",
    )

    if uploaded_file is not None:
        file_container = st.expander("Check your uploaded .csv")
        def conv(x):
            return x.replace(',', '.').encode()

        x, y   = np.genfromtxt( (conv(x) for x in open(uploaded_file)),  delimiter="\t", unpack=True)
        
        file_container.write(shows)

    else:
        st.info(
            f"""
                👆 Upload a valid file first. Sample to try:  )
                """
        )

        st.stop()

from st_aggrid import GridUpdateMode, DataReturnMode
fig, ax = plt.subplots()
ax.plot(x, y,  lw=2, c='k')

 

 

c29, c30, c31 = st.columns([1, 1, 2])

with c29:

    CSVButton = download_button(
        df,
        "File.csv",
        "Download to CSV",
    )

with c30:
    CSVButton = download_button(
        df,
        "File.csv",
        "Download to TXT",
    )
