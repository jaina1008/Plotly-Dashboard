import os
import sys
from dataclasses import dataclass
from src.exception import CustomException
from src.codes import code
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

@dataclass
class sourceConfig:
    DATA_SOURCE: str= os.path.join('data','storeData.csv')

class dataLoader:
    def __init__(self):
        self.SOURCE=sourceConfig()
        self.data=None
    
    def load_data(self):
        try:
            file_extension=self.SOURCE.DATA_SOURCE.split('.')[-1].lower()
            if file_extension=='csv':
                self.data=self._load_csv()
            elif file_extension=='txt':
                self.data=self._load_txt()
            elif file_extension in ['xls', 'xlsx']:
                self.data=self._load_excel()
        except Exception as e:
                raise CustomException(e, sys)
        
        return self.data
    
    def _load_csv(self):
        return pd.read_csv(self.SOURCE.DATA_SOURCE)
    
    def _load_txt(self):
        with open(self.SOURCE.DATA_SOURCE, 'r') as obj:
            content=obj.read()
        return content
    
    def _load_excel(self):
        return pd.read_excel(self.SOURCE.DATA_SOURCE)



# Returns unique values of columns
def uniqueValues(dataFrame, *args, **kwargs):
        return tuple(dataFrame[arg].unique() for arg in args)



# Load Dataframe
dataFrame=dataLoader().load_data()
regions,states,cities=uniqueValues(dataFrame, "Region","State","City")


# Set Options based on app callbacks
def set_state_options(selected_region):
    df=dataFrame.copy()
    states=[]
    if selected_region:
        df= df[df['Region'].isin(selected_region)]
        states= df['State'].unique()
    else:
        states=states
    return [{'label': states, 'value': states} for states in states]


def set_city_options(selected_state):
    df=dataFrame.copy()
    cities=[]
    if selected_state:
        df= df[df['State'].isin(selected_state)]
        cities= df['City'].unique()
    else:
        cities=cities
    return [{'label': cities, 'value': cities} for cities in cities]



### 3. Plotly Function
def category_sales_chart(region, state, city):
    # Create a copy of the dataframe
    df = dataFrame.copy()
    # Filter by region, state, and city if provided
    if region:
        df = df[df['Region'].isin(region)]
    if state:
        df = df[df['State'].isin(state)]
    if city:
        df = df[df['City'].isin(city)]
    
    # Group by category and sum the sales
    agg_df = df.groupby('Category', as_index=False)['Sales'].sum()
    # Create the figure using Plotly Express
    fig = px.bar(agg_df, x='Category', y='Sales')
    return fig


def subCategory_sales_chart(region, state, city):
    # Create a copy of the dataframe
    df = dataFrame.copy()
    # Filter by region, state, and city if provided
    if region:
        df = df[df['Region'].isin(region)]
    if state:
        df = df[df['State'].isin(state)]
    if city:
        df = df[df['City'].isin(city)]
    
    # Group by category and sum the sales
    agg_df = df.groupby('Sub-Category', as_index=False)['Sales'].sum()
    # Create the figure using Plotly Express
    fig = px.bar(agg_df, x='Sub-Category', y='Sales')
    return fig


def create_choropleth_map(region, state):
    # Create a copy of the dataframe
    df = dataFrame.copy()
    # Filter by region, state, and city if provided
    if region:
        df = df[df['Region'].isin(region)]
    if state:
        df = df[df['State'].isin(state)] 
    df['Code'] = df['State'].map(code)
    df = df.groupby('Code', as_index=False)['Sales'].sum().round(2)

    # Create a choropleth map
    fig = px.choropleth(df, locations='Code', color='Sales', color_continuous_scale='spectral_r', hover_name='Code', locationmode='USA-states', labels={'State Sales'}, scope='usa')

    # Update layout for better display
    fig.update_layout(
        title_text='Sales by US State',
        geo=dict( scope='usa', lakecolor='rgb(255, 255, 255)', showlakes=True, showland=True, landcolor='rgb(217, 217, 217)', subunitcolor='rgb(255, 255, 255)'),
        margin=dict(l=10,r=10,t=50,b=10))
    return fig

