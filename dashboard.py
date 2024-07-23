import streamlit as st
import plotly.express as px
import matplotlib
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


# Create Filter Sidebar
st.sidebar.header('Choose your filter: ')

# Filter Region by user
region = st.sidebar.multiselect('Pick your region', df['Region'].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df['Region'].isin(region)]

# Filter State by user
state = st.sidebar.multiselect('Pick your state', df2['State'].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2['State'].isin(state)]

# Filter City by user
city = st.sidebar.multiselect('Pick your city', df3['City'].unique())

# Filter based on Region, State and City
if not region and not state and not city:
    filtered_df = df
elif not state and not city:
    filtered_df = df[df["Region"].isin(region)]
elif not region and not city:
    filtered_df = df[df["State"].isin(state)]
elif state and city:
    filtered_df = df3[df['State'].isin(state) & df3['City'].isin(city)]
elif region and city:
    filtered_df = df3[df['Region'].isin(region) & df3['City'].isin(city)]
elif region and state:
    filtered_df = df3[df['Region'].isin(region) & df3['State'].isin(state)]
elif city:
    filtered_df = df3[df3['City'].isin(city)]
else:
    filtered_df = df3[df3['Region'].isin(region) & df3['State'].isin(state) & df3['City'].isin(city)]


# Charts
category_df = filtered_df.groupby(by = ['Category'], as_index=False)['Sales'].sum()

# Bar chart
with col1:
    st.subheader('Category wise Sales')
    fig = px.bar(category_df, x='Category', y='Sales', text=['${:,.2f}'.format(x) for x in category_df['Sales']], template='seaborn')
    st.plotly_chart(fig, use_container_width=True, height=200)

# Pie chart
with col2:
    st.subheader('Region wise Sales')
    fig = px.pie(filtered_df, values='Sales', names='Region', hole=0.5)
    fig.update_traces(text=filtered_df['Region'], textposition='outside')
    st.plotly_chart(fig, use_container_width=200)


# Download Selected Data
cl1, cl2 = st.columns(2)
with cl1:
    with st.expander('Category_ViewData'):
        st.write(category_df.style.background_gradient(cmap='Blues'))
        csv=category_df.to_csv(index=False)
        st.download_button('Download Data', data=csv, file_name='Category.csv', mime='text/csv',
                           help='Click here to download selected data as a CSV file')

with cl2:
    with st.expander('Region_ViewData'):
        region= filtered_df.groupby(by='Region', as_index=False)['Sales'].sum()
        st.write(region.style.background_gradient(cmap='Oranges'))
        csv=region.to_csv(index=False)
        st.download_button('Download Data', data=csv, file_name='Region.csv', mime='text/csv',
                           help='Click here to download selected data as a CSV file')