import sys
import pandas as pd
import numpy as np
import streamlit as st
import io

st.set_page_config(page_title='Lapangbola XML Generator for Video Tagging', layout='wide')
st.header('XML File Generator')
st.markdown('Created by: Prana - R&D Division Lapangbola.com')

sys.path.append("listfungsi.py")
from listfungsi import datacleaner

buffer = io.BytesIO()

with st.expander("BACA INI DULU."):
    st.write("Upload file timeline yang telah selesai di-QC!")
    
col1, col2 = st.columns(2)
with col1:
    tl_data = st.file_uploader("Upload file timeline excel!")
    try:
        tl = pd.read_excel(tl_data, skiprows=[0])
        c_data = datacleaner(tl)
        st.write(c_data)

        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            c_data.to_excel(writer, sheet_name='Sheet1', index=False)
            download2 = st.download_button(
                label="Download data as Excel",
                data=buffer,
                file_name='file-excel.xlsx',
                mime='application/vnd.ms-excel')
            
    except ValueError:
        st.error("Please upload the timeline file")

'''
pn = plot_PN(pass_between, min_pass, filter, menit[0], menit[1], match, gw)
st.pyplot(pn)

with open('pnet.jpg', 'rb') as img:
    fn = 'PN_'+filter+'.jpg'
    btn = st.download_button(label="Download Passing Network", data=img, file_name=fn, mime="image/jpg")
'''
