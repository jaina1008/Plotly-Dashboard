import streamlit as st
import plotly.express as px
import matplotlib
import pandas as pd
import os
import sys
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging
import warnings

warnings.filterwarnings('ignore')


@dataclass
class SourceConfig:
    source_data_path: str= os.path.join('data', 'storeData.csv')

class PageConfig:
    def __init__(self, total_cols):
        self.source_file= SourceConfig()
        self.PAGE_TITLE='TOGETHER DASHBOARD'
        self.DASH_TITLE='SALES DASHBOARD'
        self.COLUMN_NUM:list=[None]*total_cols
        self.SIDEBAR_HEADER='FILTER OPTIONS:'
        self.CURRENT_DATASET=" "
    
    def page_structure(self):
        try:
            st.set_page_config(page_title=self.PAGE_TITLE, page_icon=":bar_chart", layout='wide')
            st.title(":bar_chart: {0}".format(self.DASH_TITLE))
            st.markdown('<style>divblock-container{padding-top:1.8rem;}</style>', unsafe_allow_html=True)
            logging.info('Page Structure Configured')

        except Exception as e:
            raise CustomException(e, sys)
        
    def source_structure(self):
        # Load source file
        try:
            # Ask user for file
            file: str= st.file_uploader(':file_folder: If you have your own source CSV file, Please upload it below:')
            if file is not None:
                fileName = file.name
                st.write(fileName)
                df= pd.read_csv(fileName)
                logging.info('User given source file has been read')
            
            else:
                file: str= self.source_file.source_data_path
                df= pd.read_csv(file)
                logging.info('Local source file has been read')
        
            # Dividing page into two columns
            self.COLUMN_NUM[0], self.COLUMN_NUM[1] = st.columns(2)

            # Getting min max date from dataset
            df['Order Date'] = pd.to_datetime(df['Order Date'])
            startDate = pd.to_datetime(df['Order Date']).min()
            endDate = pd.to_datetime(df['Order Date']).max()

            with self.COLUMN_NUM[0]:
                date1 = pd.to_datetime(st.date_input('Start Date', startDate))
            with self.COLUMN_NUM[1]:
                date2 = pd.to_datetime(st.date_input('End Date', endDate))

            self.CURRENT_DATASET = df[(df['Order Date'] >= date1) & (df['Order Date'] <= date2)].copy()
        
        except Exception as e:
            raise CustomException(e, sys)
        

    def configure_filters(self):

        df = self.CURRENT_DATASET

        try:
            st.sidebar.header(self.SIDEBAR_HEADER)

            # Filter by Region
            region = st.sidebar.multiselect('Pick your region', df['Region'].unique())
            if not region:
                pass
            else:
                df = df[df['Region'].isin(region)]

            # Filter by State
            state = st.sidebar.multiselect('Pick your state', df['State'].unique())
            if not state:
                pass
            else:
                df = df[df['State'].isin(state)]

            # Filter by City
            city = st.sidebar.multiselect('Pick your city', df['City'].unique())
            if not city:
                pass
            else:
                df = df[df['City'].isin(city)]    

            self.CURRENT_DATASET = df        
        except Exception as e:
            raise CustomException(e, sys)
    
    def configure_charts(self):
        df= self.CURRENT_DATASET
        category_df= df.groupby(by = ['Category'], as_index=False)['Sales'].sum().round(2)
        region_df= df.groupby(by='Region', as_index=False)['Sales'].sum().round(2)
        subCategory_df=df.groupby(by = ['Sub-Category'], as_index=False)['Sales'].sum().round(2)

        # Bar chart
        with self.COLUMN_NUM[0]:
            st.subheader('Sales Per Category')
            fig = px.bar(category_df, x='Category', y='Sales', text=['${:,.2f}'.format(x) for x in category_df['Sales']],
                         template='seaborn')
            st.plotly_chart(fig, use_container_width=True, height=200)

            with st.expander('Download CSV: Sales Per Category'):
                st.write(category_df.style.background_gradient(cmap='Blues'))
                csv=category_df.to_csv(index=False)
                st.download_button('Download Data', data=csv, file_name='Category.csv', mime='text/csv',
                                    help='Click here to download selected data as a CSV file')

        # Pie chart
        with self.COLUMN_NUM[1]:
            st.subheader('Regional Sales')
            fig = px.pie(df, values='Sales', names='Region', hole=0.5)
            fig.update_traces(text=df['Region'], textposition='outside')
            st.plotly_chart(fig, use_container_width=200)

            with st.expander('Download CSV: Regional Sales'):
                st.write(region_df.style.background_gradient(cmap='Oranges'))
                csv=region_df.to_csv(index=False)
                st.download_button('Download Data', data=csv, file_name='Region.csv', mime='text/csv',
                                   help='Click here to download selected data as a CSV file')
        
        # Sub-Category chart
        st.subheader('Sales Per Sub-Category')
        fig = px.bar(subCategory_df, x='Sub-Category', y='Sales', text=['${:,.2f}'.format(x) for x in subCategory_df['Sales']],
                template='seaborn')
        st.plotly_chart(fig, use_container_width=True, height=200)

        with st.expander('Download CSV: Sales Per Sub-Category'):
            st.write(subCategory_df.style.background_gradient(cmap='Blues'))
            csv=subCategory_df.to_csv(index=False)
            st.download_button('Download Data', data=csv, file_name='Sub-Category.csv', mime='text/csv',
                                help='Click here to download selected data as a CSV file')
    
    




if __name__=="__main__":
    dashboard= PageConfig(total_cols=2)
    dashboard.page_structure()
    dashboard.source_structure()
    dashboard.configure_filters()
    dashboard.configure_charts()