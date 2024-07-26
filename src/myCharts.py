import os
import sys
from dataclasses import dataclass
from src.exception import CustomException
from src.codes import code
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

print(os.getcwd())
@dataclass
class sourceConfig:
    DATA_SOURCE: str= os.path.join('src','storeData.csv')

class dataLoader:
    def __init__(self):
        self.SOURCE=sourceConfig()
        self.data=None
    
    def load_data(self):
        try:
            file_extension=self.SOURCE.split('.')[-1].lower()
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
        return pd.read_csv(self.SOURCE)
    
    def _load_txt(self):
        with open(self.SOURCE, 'r') as obj:
            content=obj.read()
        return content
    
    def _load_excel(self):
        return pd.read_excel(self.SOURCE)


dataFrame=dataLoader().load_data()

# SOURCE_PATH: str= os.path.join('data', 'storeData.csv')
# dataFrame=pd.read_csv(SOURCE_PATH)
# dataFrame['Order Date'] = pd.to_datetime(dataFrame['Order Date'])
# df = pd.DataFrame(dataFrame)


# Set Options based on app callbacks
def set_state_options(selected_region):
    state_df=df.copy()
    states=[]
    if selected_region:
        state_df= state_df[state_df['Region'].isin(selected_region)]
        states= state_df['State'].unique()
    else:
        states= state_df['State'].unique()
    return [{'label': states, 'value': states} for states in states]


def set_city_options(selected_state):
    city_df=df.copy()
    cities=[]
    if selected_state:
        city_df= city_df[city_df['State'].isin(selected_state)]
        cities= city_df['City'].unique()
    else:
        cities= city_df['City'].unique()
    return [{'label': cities, 'value': cities} for cities in cities]



### 3. Plotly Function
def category_sales_chart(region, state, city):
    # Create a copy of the dataframe
    filtered_df = df.copy()
    # Filter by region, state, and city if provided
    if region:
        filtered_df = filtered_df[filtered_df['Region'].isin(region)]
    if state:
        filtered_df = filtered_df[filtered_df['State'].isin(state)]
    if city:
        filtered_df = filtered_df[filtered_df['City'].isin(city)]
    
    # Group by category and sum the sales
    agg_df = filtered_df.groupby('Category', as_index=False)['Sales'].sum()
    
    # Create the figure using Plotly Express
    fig = px.bar(agg_df, x='Category', y='Sales')
    return fig


def subCategory_sales_chart(region, state, city):
    # Create a copy of the dataframe
    filtered_df = df.copy()
    # Filter by region, state, and city if provided
    if region:
        filtered_df = filtered_df[filtered_df['Region'].isin(region)]
    if state:
        filtered_df = filtered_df[filtered_df['State'].isin(state)]
    if city:
        filtered_df = filtered_df[filtered_df['City'].isin(city)]
    
    # Group by category and sum the sales
    agg_df = filtered_df.groupby('Sub-Category', as_index=False)['Sales'].sum()
    
    # Create the figure using Plotly Express
    fig = px.bar(agg_df, x='Sub-Category', y='Sales')
    return fig


def create_choropleth_map(region, state):
    # Create a copy of the dataframe
    filtered_df = df.copy()
    # Filter by region, state, and city if provided
    if region:
        filtered_df = filtered_df[filtered_df['Region'].isin(region)]
    if state:
        filtered_df = filtered_df[filtered_df['State'].isin(state)] 
    filtered_df['Code'] = filtered_df['State'].map(code)
    filtered_df = filtered_df.groupby('Code', as_index=False)['Sales'].sum().round(2)

    # Create a choropleth map
    fig = px.choropleth(filtered_df, locations='Code', color='Sales', color_continuous_scale='spectral_r', hover_name='Code', locationmode='USA-states', labels={'State Sales'}, scope='usa')

    # Update layout for better display
    fig.update_layout(
        title_text='Sales by US State',
        geo=dict( scope='usa', lakecolor='rgb(255, 255, 255)', showlakes=True, showland=True, landcolor='rgb(217, 217, 217)', subunitcolor='rgb(255, 255, 255)'),
        margin=dict(l=10,r=10,t=50,b=10))
    return fig
