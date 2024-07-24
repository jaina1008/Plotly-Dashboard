import pandas as pd
import os
import sys
from dataclasses import dataclass
from dash import dcc, html, Dash, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import matplotlib
from src.codes import code
from src.exception import CustomException
from src.logger import logging
import warnings
warnings.filterwarnings('ignore')

bgColor="#e5ecf6"
margin=dict(l=10,r=10,t=50,b=10)
height=600
font=dict(size=10)


@dataclass
class SourceConfig:
    SOURCE_PATH: str= os.path.join('data', 'storeData.csv')

class DashConfig:
    def __init__(self):
        self.SOURCE=SourceConfig()
        self.CSS=["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css", ]
        self.NAME='TOGETHER DASHBOARD'

class DashChartsConfig:
    def __init__(self, bgColor, margin, height, font, dataFrame):
        self.bgColor=bgColor
        self.margin=margin
        self.height=height
        self.font=font
        self.dataFrame=dataFrame

    def create_table(self):
        dataFrame=self.dataFrame.head(10)
        fig = go.Figure(data=[go.Table(
            header=dict(values=dataFrame.columns, align='left'),
            cells=dict(values=dataFrame.values.T, align='left'))
        ])
        fig.update_layout(paper_bgcolor=self.bgColor,
                          margin=self.margin,
                          height=self.height,
                          font=dict(size=8),
                          autosize=True)
        return fig
    
    
    def category_sales_chart(self):
        df=self.dataFrame.groupby(by = ['Category'], as_index=False)['Sales'].sum().round(2)
        fig = px.bar(df, x='Category', y='Sales', text=['${:,.2f}'.format(x) for x in df['Sales']],
                    template='seaborn')
        fig.update_layout(paper_bgcolor=self.bgColor, height=self.height, font=self.font, autosize=True)
        return fig


    def SubCategory_sales_chart(self):
        df= self.dataFrame.groupby(by = ['Sub-Category'], as_index=False)['Sales'].sum().round(2)
        fig = px.bar(df, x='Sub-Category', y='Sales', text=['${:,.2f}'.format(x) for x in df['Sales']],
                template='seaborn')
        fig.update_layout(paper_bgcolor=self.bgColor, height=self.height, font=self.font, autosize=True)
        return fig


    def create_choropleth_map(self):
        df=self.dataFrame.groupby(by = ['State'], as_index=False)['Sales'].sum().round(2)    
        df['Code'] = df['State'].map(code)

        # Create a choropleth map
        fig = px.choropleth(df,
                    locations='Code',
                    color='Sales',
                    color_continuous_scale='spectral_r',
                    hover_name='State',
                    locationmode='USA-states',
                    labels={'State Sales'},
                    scope='usa')

        # Update layout for better display
        fig.update_layout(
            title_text='Sales by US State',
            geo=dict(
                scope='usa',
                lakecolor='rgb(255, 255, 255)',
                showlakes=True,
                showland=True,
                landcolor='rgb(217, 217, 217)',
                subunitcolor='rgb(255, 255, 255)'
            ), margin=self.margin)
        return fig


if __name__=="__main__":

    dashboard=DashConfig()
    file=dashboard.SOURCE.SOURCE_PATH

    df=pd.read_csv(file)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    charts=DashChartsConfig(bgColor=bgColor, margin=margin, height=height, font=font, dataFrame=df)

    region=df['Region'].unique()
    state=df['State'].unique()
    city=df['City'].unique()

# ##################### WIDGETS ###################################
    region_picker=dcc.Dropdown(id='region', options=region, clearable=False)
    state_picker=dcc.Dropdown(id='state', options=state, clearable=False)
    city_picker=dcc.Dropdown(id='city', options=city, clearable=False)
    date_picker= dcc.DatePickerRange(
        id='date_range',
        start_date=df['Order Date'].min().date(),
        end_date=df['Order Date'].max().date(),
        display_format='MM-DD-YYYY'  # Date format
    )

# ##################### APP LAYOUT ####################################
    app = Dash(name=dashboard.NAME, external_stylesheets=dashboard.CSS) 
    app.layout = html.Div([
    html.Div([
        html.H1("Sales Store Analysis", className="text-center fw-bold m-2"),
        html.Br(),
        dcc.Tabs(id='All Tabs', children=[
            dcc.Tab(children=[html.Br(),
                     dcc.Graph(id="Data", figure=charts.create_table())], label="Dataset"),

            dcc.Tab(children=[html.Br(), "DATE RANGE", html.Div(date_picker),
                     "REGION", region_picker, "STATE", state_picker,"CITY", city_picker, html.Br(),
                     dcc.Graph(id="Chart1", figure=charts.category_sales_chart())], label="Sales By Category"),

            dcc.Tab([html.Br(), "DATE RANGE", html.Div(date_picker), "REGION", region_picker, "STATE", state_picker,"CITY", city_picker, html.Br(),
                     dcc.Graph(id="Chart2", figure=charts.SubCategory_sales_chart())], label="Sales By Sub-Category"),

            dcc.Tab([html.Br(), "DATE RANGE", html.Div(date_picker), "REGION", region_picker, "STATE", state_picker,"CITY", city_picker, html.Br(),
                     dcc.Graph(id="Chart3", figure=charts.create_choropleth_map())], label="Sales Choropleth")
                     ])
                     ], className="col-8 mx-auto"),
                     ], style={"background-color": "#e5ecf6", "height": "150vh"})


    app.run(debug=True)


# ##################### CALLBACKS ####################################
# @callback(Output("Chart1", "figure"), [Input("cont_pop", "value"), Input("year_pop", "value"),])
# def update_population_chart(continent, year):
#     return create_population_chart(continent, year)

# @callback(Output("Chart2", "figure"), [Input("cont_gdp", "value"), Input("year_gdp", "value"),])
# def update_gdp_chart(continent, year):
#     return create_gdp_chart(continent, year)

# @callback(Output("Chart3", "figure"), [Input("cont_life_exp", "value"), Input("year_life_exp", "value"),])
# def update_life_exp_chart(continent, year):
#     return create_life_exp_chart(continent, year)

# @callback(Output("choropleth_map", "figure"), [Input("var_map", "value"), Input("year_map", "value"),])
# def update_map(var_map, year):
#     return create_choropleth_map(var_map, year)

# if __name__ == "__main__":
#     app.run(debug=True)