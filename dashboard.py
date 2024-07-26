import os
from dash import dcc, html, Dash, callback, Input, Output
from src.codes import code
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# bgColor="#e5ecf6"
# margin=dict(l=10,r=10,t=50,b=10)
# height=600
# font=dict(size=10)

SOURCE_PATH: str= os.path.join('data', 'storeData.csv')
CSS=["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css", ]
NAME='TOGETHER DASHBOARD'


dataFrame=pd.read_csv(SOURCE_PATH)
dataFrame['Order Date'] = pd.to_datetime(dataFrame['Order Date'])
df = pd.DataFrame(dataFrame)


app = Dash(NAME, external_stylesheets=CSS)
app.layout = html.Div([
    html.Div([ html.H1("Sales Store Analysis", className="text-center fw-bold m-2"), html.Br(),
    html.Div([
        html.Label('REGION'),
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': region, 'value': region} for region in df['Region'].unique()],
            multi=True
        ),
    ]),
    html.Div([
        html.Label('STATE'),
        dcc.Dropdown(
            id='state-dropdown',
            options=[{'label': state, 'value': state} for state in df['State'].unique()],
            multi=True
        ),
    ]),
    html.Div([
        html.Label('CITY'),
        dcc.Dropdown(
            id='city-dropdown',
            options=[{'label': city, 'value': city} for city in df['City'].unique()],
            multi=True
        ),
    ]),
    dcc.Tabs(id='allTabs', value='tabs', children=[
        dcc.Tab([dcc.Graph(id='Chart1')], label='Category Sales', value='tab_1'),
        dcc.Tab([dcc.Graph(id='Chart2')], label='Sub Category Sales', value='tab_2'),
        dcc.Tab([dcc.Graph(id='Chart3')], label='Choropleth Map', value='tab_3')
    ])
], className="col-8 mx-auto")
], style={"background-color": "#e5ecf6", "height": "150vh"})




### 2. Callback Definition
@app.callback(
        Output('state-dropdown', 'options'), Input('region-dropdown', 'value')
)
def set_state_options(selected_region):
    state_df=df.copy()
    states=[]
    if selected_region:
        state_df= state_df[state_df['Region'].isin(selected_region)]
        states= state_df['State'].unique()
    else:
        states= state_df['State'].unique()
    return [{'label': states, 'value': states} for states in states]


@app.callback(
        Output('city-dropdown', 'options'), Input('state-dropdown', 'value')
)
def set_city_options(selected_state):
    city_df=df.copy()
    cities=[]
    if selected_state:
        city_df= city_df[city_df['State'].isin(selected_state)]
        cities= city_df['City'].unique()
    else:
        cities= city_df['City'].unique()
    return [{'label': cities, 'value': cities} for cities in cities]



@app.callback(
        Output('Chart1', 'figure'), [Input('region-dropdown', 'value'), Input('state-dropdown', 'value'), Input('city-dropdown', 'value')])
def update_chart_one(region, state, city):
    return category_sales_chart(region, state, city)

@app.callback(
        Output('Chart2', 'figure'), [Input('region-dropdown', 'value'), Input('state-dropdown', 'value'), Input('city-dropdown', 'value')])
def update_chart_two(region, state, city):
    return subCategory_sales_chart(region, state, city)

@app.callback(
        Output('Chart3', 'figure'), [Input('region-dropdown', 'value'), Input('state-dropdown', 'value')])
def update_chart_three(region, state):
    return create_choropleth_map(region, state)




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

if __name__ == '__main__':
    app.run_server(debug=True)
