import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title='Superstore', page_icon=":bar_chart:", layout="wide")
st.title(":bar_chart: Sample SuperStore EDA")
st.markdown('<style>div.block-container{padding-top:1.8rem;}</style>', unsafe_allow_html=True)

# Browser or Upload Data

file = st.file_uploader(':file_folder: Upload a file', type=(['csv', 'txt','xlsx','xls']))
if file is not None:
    fileName = file.name
    st.write(fileName)
    df = pd.read_csv(fileName)
else:
    df = pd.read_csv("data/storeData.csv")

col1, col2 = st.columns(2)
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Getting minimum and maximum date
startDate = pd.to_datetime(df['Order Date']).min()
endDate = pd.to_datetime(df['Order Date']).max()

with col1:
    date1 = pd.to_datetime(st.date_input('Start Date', startDate))
with col2:
    date2 = pd.to_datetime(st.date_input('End Date', endDate))

df = df[(df['Order Date'] >= date1) & (df['Order Date'] <= date2)].copy()


# Filter selection by user
st.sidebar.header('Choose your filter: ')
region = st.sidebar.multiselect('Pick your region', df['Region'].unique())
