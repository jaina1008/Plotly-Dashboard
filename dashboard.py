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


@dataclass
class SourceConfig:
    SOURCE_PATH: str= os.path.join('data', 'storeData.csv')

class DashboardConfig:
    def __init__(self):
        self.SOURCE=SourceConfig()
        self.CSS=["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css", ]
        self.NAME='TOGETHER DASHBOARD'

    def create_table(self, dataFrame):
        dataFrame=dataFrame.head()
        fig = go.Figure(data=[go.Table(
            header=dict(values=dataFrame.columns, align='left'),
            cells=dict(values=dataFrame.values.T, align='left'))
        ])
        fig.update_layout(paper_bgcolor="#e5ecf6",
                          margin={"t":0, "l":0, "r":0, "b":0},
                          height=700,
                          font=dict(size=8),
                          autosize=True)
        return fig
    
    
    def category_sales_chart(self, dataFrame):
        category_df= dataFrame.groupby(by = ['Category'], as_index=False)['Sales'].sum().round(2)
        # filtered_df = filtered_df.sort_values(by="Population", ascending=False).head(15)

        fig = px.bar(category_df, x='Category', y='Sales', text=['${:,.2f}'.format(x) for x in category_df['Sales']],
                    template='seaborn')
        fig.update_layout(paper_bgcolor="#e5ecf6", height=600)
        return fig


    def SubCategory_sales_chart(self, dataFrame):
        subCategory_df= dataFrame.groupby(by = ['Sub-Category'], as_index=False)['Sales'].sum().round(2)
        fig = px.bar(subCategory_df, x='Sub-Category', y='Sales', text=['${:,.2f}'.format(x) for x in subCategory_df['Sales']],
                template='seaborn')
        fig.update_layout(paper_bgcolor="#e5ecf6", height=600)
        return fig


    def create_choropleth_map(self, dataFrame):
        df=dataFrame.groupby(by = ['State'], as_index=False)['Sales'].sum().round(2)    
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
            ),
            margin=dict(l=10, r=10, t=60, b=10))
        
        return fig


if __name__=="__main__":
    dashboard=DashboardConfig()
    app = Dash(name=dashboard.NAME, external_stylesheets=dashboard.CSS) 
    file=dashboard.SOURCE.SOURCE_PATH

    df=pd.read_csv(file)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    startDate = pd.to_datetime(df['Order Date']).min()
    endDate = pd.to_datetime(df['Order Date']).max()

    # dashboard.create_table(df)

    app.layout = html.Div([
    html.Div([
        html.H1("Sales Store Analysis", className="text-center fw-bold m-2"),
        html.Br(),
        dcc.Tabs([
            dcc.Tab([html.Br(),
                     dcc.Graph(id="dataset1", figure=dashboard.create_table(df))], label="Dataset"),
            dcc.Tab([html.Br(),
                     dcc.Graph(id="dataset2", figure=dashboard.category_sales_chart(df))], label="Sales By Category"),
            dcc.Tab([html.Br(),
                     dcc.Graph(id="dataset3", figure=dashboard.SubCategory_sales_chart(df))], label="Sales By Sub-Category"),
            dcc.Tab([html.Br(),
                     dcc.Graph(id="dataset4", figure=dashboard.create_choropleth_map(df))], label="Sales Choropleth")
                     ])
                     ], className="col-8 mx-auto"),
                     ], style={"background-color": "#e5ecf6", "height": "100vh"})



        
    app.run(debug=True)

# #################### CHARTS #####################################
# def create_table():
#     fig = go.Figure(data=[go.Table(
#         header=dict(values=gapminder_df.columns, align='left'),
#         cells=dict(values=gapminder_df.values.T, align='left'))
#     ]
#     )
#     fig.update_layout(paper_bgcolor="#e5ecf6", margin={"t":0, "l":0, "r":0, "b":0}, height=700)
#     return fig

# def create_population_chart(continent="Asia", year=1952, ):
#     filtered_df = gapminder_df[(gapminder_df.Continent==continent) & (gapminder_df.Year==year)]
#     filtered_df = filtered_df.sort_values(by="Population", ascending=False).head(15)

#     fig = px.bar(filtered_df, x="Country", y="Population", color="Country",
#                    title="Country {} for {} Continent in {}".format("Population", continent, year),
#                    text_auto=True)
#     fig.update_layout(paper_bgcolor="#e5ecf6", height=600)
#     return fig

# def create_gdp_chart(continent="Asia", year=1952):
#     filtered_df = gapminder_df[(gapminder_df.Continent==continent) & (gapminder_df.Year==year)]
#     filtered_df = filtered_df.sort_values(by="GDP per Capita", ascending=False).head(15)

#     fig = px.bar(filtered_df, x="Country", y="GDP per Capita", color="Country",
#                    title="Country {} for {} Continent in {}".format("GDP per Capita", continent, year),
#                    text_auto=True)
#     fig.update_layout(paper_bgcolor="#e5ecf6", height=600)
#     return fig

# def create_life_exp_chart(continent="Asia", year=1952):
#     filtered_df = gapminder_df[(gapminder_df.Continent==continent) & (gapminder_df.Year==year)]
#     filtered_df = filtered_df.sort_values(by="Life Expectancy", ascending=False).head(15)

#     fig = px.bar(filtered_df, x="Country", y="Life Expectancy", color="Country",
#                    title="Country {} for {} Continent in {}".format("Life Expectancy", continent, year),
#                    text_auto=True)
#     fig.update_layout(paper_bgcolor="#e5ecf6", height=600)
#     return fig

# def create_choropleth_map(variable, year):
#     filtered_df = gapminder_df[gapminder_df.Year==year]

#     fig = px.choropleth(filtered_df, color=variable, 
#                         locations="ISO Alpha Country Code", locationmode="ISO-3",
#                         color_continuous_scale="RdYlBu", hover_data=["Country", variable],
#                         title="{} Choropleth Map [{}]".format(variable, year)
#                      )

#     fig.update_layout(dragmode=False, paper_bgcolor="#e5ecf6", height=600, margin={"l":0, "r":0})
#     return fig

# ##################### WIDGETS ####################################
# continents = gapminder_df.Continent.unique()
# years = gapminder_df.Year.unique()

# cont_population = dcc.Dropdown(id="cont_pop", options=continents, value="Asia",clearable=False)
# year_population = dcc.Dropdown(id="year_pop", options=years, value=1952,clearable=False)

# cont_gdp = dcc.Dropdown(id="cont_gdp", options=continents, value="Asia",clearable=False)
# year_gdp = dcc.Dropdown(id="year_gdp", options=years, value=1952,clearable=False)

# cont_life_exp = dcc.Dropdown(id="cont_life_exp", options=continents, value="Asia",clearable=False)
# year_life_exp = dcc.Dropdown(id="year_life_exp", options=years, value=1952,clearable=False)

# year_map = dcc.Dropdown(id="year_map", options=years, value=1952,clearable=False)
# var_map = dcc.Dropdown(id="var_map", options=["Population", "GDP per Capita", "Life Expectancy"],
#                         value="Life Expectancy",clearable=False)

# ##################### APP LAYOUT ####################################
# app.layout = html.Div([
#     html.Div([
#         html.H1("Gapminder Dataset Analysis", className="text-center fw-bold m-2"),
#         html.Br(),
#         dcc.Tabs([
#             dcc.Tab([html.Br(),
#                      dcc.Graph(id="dataset", figure=create_table())], label="Dataset"),
#             dcc.Tab([html.Br(), "Continent", cont_population, "Year", year_population, html.Br(),
#                      dcc.Graph(id="population")], label="Population"),
#             dcc.Tab([html.Br(), "Continent", cont_gdp, "Year", year_gdp, html.Br(),
#                      dcc.Graph(id="gdp")], label="GDP Per Capita"),
#             dcc.Tab([html.Br(), "Continent", cont_life_exp, "Year", year_life_exp, html.Br(),
#                      dcc.Graph(id="life_expectancy")], label="Life Expectancy"),
#             dcc.Tab([html.Br(), "Variable", var_map, "Year", year_map, html.Br(),
#                      dcc.Graph(id="choropleth_map")], label="Choropleth Map"),
#         ])
#     ], className="col-8 mx-auto"),
# ], style={"background-color": "#e5ecf6", "height": "100vh"})

# ##################### CALLBACKS ####################################
# @callback(Output("population", "figure"), [Input("cont_pop", "value"), Input("year_pop", "value"),])
# def update_population_chart(continent, year):
#     return create_population_chart(continent, year)

# @callback(Output("gdp", "figure"), [Input("cont_gdp", "value"), Input("year_gdp", "value"),])
# def update_gdp_chart(continent, year):
#     return create_gdp_chart(continent, year)

# @callback(Output("life_expectancy", "figure"), [Input("cont_life_exp", "value"), Input("year_life_exp", "value"),])
# def update_life_exp_chart(continent, year):
#     return create_life_exp_chart(continent, year)

# @callback(Output("choropleth_map", "figure"), [Input("var_map", "value"), Input("year_map", "value"),])
# def update_map(var_map, year):
#     return create_choropleth_map(var_map, year)

# if __name__ == "__main__":
#     app.run(debug=True)