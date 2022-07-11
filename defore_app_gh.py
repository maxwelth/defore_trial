import st_defore_utils as utils
import st_defore_main as mains

from datetime import date
import streamlit as st
from PIL import Image
import pandas as pd


coll1,coll2 = st.columns([1,1])
coll1.image(Image.open(r"./resources/sirclo_logo.png"))

st.title("Demand Forecasting Project")

"""
This app is an automated version of SIRCLO Data Intelligence's Demand Forecasting project.
Resources to get started (READ FIRST):
1. [WORKFLOW](https://www.nyan.cat/)
2. [QUERY TO GET SALES DATA](https://dashboard.srcli.xyz/queries/6077/)
FURTHER NOTE:
blank.
"""

uploaded_file = st.file_uploader("Upload data file:")

with st.sidebar.header('Set Parameters'):
    warehouse = st.sidebar.selectbox(
                 'Name of Warehouse:',
                 ('ALL BSD', 'ALL MITRA TOKOPEDIA', 'ALL LEGOK 10K', 'ALL LEGOK B6, A7', 'ALL SURABAYA',
                 'ALL FF', 'ALL PEMINJAMAN', 'ALL B2B', 'OTHERS'))
    pred_date = st.sidebar.date_input(
                 "Prediction Date")
    run = st.sidebar.button(label='Run Analysis',key=1)

if uploaded_file is not None:
    st.text('Upload successful!')
    
    demand_file = utils.load_data(uploaded_file)
    st.write(demand_file[demand_file['warehouse_agg']==warehouse].head())
    
    if run:
        results = mains.main(demand_file,warehouse, pred_date)
        st.write(f'Sales prediction result till {pred_date} + 3D') 
        st.dataframe(results)
        
else:
    '''
    No sales data uploaded, please upload and run.
    '''
    
    
    
    
