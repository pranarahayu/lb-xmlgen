import sys
import pandas as pd
import numpy as np
import streamlit as st
import io

import openpyxl, yattag
from openpyxl import load_workbook
from yattag import Doc, indent

st.set_page_config(page_title='Lapangbola XML Generator for Video Tagging', layout='wide')
st.header('XML File Generator')
st.markdown('Created by: Prana - R&D Division Lapangbola.com')

sys.path.append("listfungsi.py")
from listfungsi import datacleaner

with st.expander("CARA PAKAI."):
    st.write("1. Upload file timeline ke file uploader pertama./n2. Download as excel, upload excel ke file uploader kedua./n3. Download file XML")
    
col1, col2 = st.columns(2)
with col1:
    tl_data = st.file_uploader("Upload file timeline excel!")
    try:
        tl = pd.read_excel(tl_data, skiprows=[0])
        c_data = datacleaner(tl)

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            c_data.to_excel(writer, sheet_name='Sheet1', index=False)
        download = st.download_button(
            label="Download data as Excel",
            data=buffer.getvalue(),
            file_name='clean-data.xlsx',
            mime='application/vnd.ms-excel')
            
    except ValueError:
        st.error("Please upload the timeline file")

with col2:
    cl_data = st.file_uploader("Upload file clean-data.xlsx!")
    try:
        wb = load_workbook(cl_data)
        ws = wb.worksheets[0]
        doc, tag, text = Doc().tagtext()

        xml_header = ''
        xml_schema = ''

        doc.asis(xml_header)
        doc.asis(xml_schema)

        with tag('file'):
          doc.asis('<!--Generated by Lapangbola-->')
          with tag('ALL_INSTANCES'):
            for row in ws.iter_rows(min_row=2, max_row=1000, min_col=1, max_col=12):
                row = [cell.value for cell in row]
                with tag("instance"):
                    with tag("ID"):
                        text(row[0])
                    with tag("code"):
                        text(row[1])
                    with tag("start"):
                        text(row[2])
                    with tag("end"):
                        text(row[3])
                    with tag('label'):
                      with tag('group'):
                        text(row[4])
                      with tag('text'):
                        text(row[5])
                    with tag('label'):
                      with tag('group'):
                        text(row[6])
                      with tag('text'):
                        text(row[7])
                    with tag('label'):
                      with tag('group'):
                        text(row[8])
                      with tag('text'):
                        text(row[9])

        result = indent(doc.getvalue(), indentation = '    ',indent_text = True)
        with open("xml-data.xml", "w") as f:
            download1 = st.download_button(
                label="Download XML data",
                data=result,
                file_name='xml-data.xml',
                mime='text/csv')

    except ValueError:
        st.error("Please upload the clean-data")
