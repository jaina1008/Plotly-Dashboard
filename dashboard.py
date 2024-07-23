import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title='Superstore', page_icon=":bar_chart:", layout="wide")
st.title(":bar_chart: Sample SuperStore EDA")
st.markdown('<style>div.block-container{padding-top:1.8rem;}</style>', unsafe_allow_html=True)

# # Browser or Upload Data
# file = st.file_uploader(':file_folder: Upload a file', type=(['csv', 'txt','xlsx','xls']))
# if file is not None:
#     fileName = file.name
#     st.write(fileName)
#     df = pd.read_csv(fileName)
# else:
#     os.chdir(f"./data")
#     df = pd.read_csv()
