
from dash import dcc, html, Dash, callback, Input, Output
import src.myCharts as myCharts

app = Dash(name='Sales Store Analysis')
app.layout = html.Div([
    html.Div([ html.H1('Sales Store Analysis', className="text-center fw-bold m-2"), html.Br(),
    html.Div([
        html.Label('REGION'),
        dcc.Dropdown(
            id='region-dropdown',
            options=myCharts.regions,
            multi=True
        ),
    ]),
    html.Div([
        html.Label('STATE'),
        dcc.Dropdown(
            id='state-dropdown',
            # options=[{'label': state, 'value': state} for state in myCharts.states],
            options=myCharts.states,
            multi=True
        ),
    ]),
    html.Div([
        html.Label('CITY'),
        dcc.Dropdown(
            id='city-dropdown',
            options=myCharts.cities,
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
        Output('state-dropdown', 'options'), Input('region-dropdown', 'value'))
def state_options(selected_region):
    return myCharts.set_state_options(selected_region)

@app.callback(
        Output('city-dropdown', 'options'), Input('state-dropdown', 'value'))
def city_option(selected_state):
    return myCharts.set_city_options(selected_state)


@app.callback(
        Output('Chart1', 'figure'), [Input('region-dropdown', 'value'), Input('state-dropdown', 'value'), Input('city-dropdown', 'value')])
def update_chart_one(region, state, city):
    return myCharts.category_sales_chart(region, state, city)

@app.callback(
        Output('Chart2', 'figure'), [Input('region-dropdown', 'value'), Input('state-dropdown', 'value'), Input('city-dropdown', 'value')])
def update_chart_two(region, state, city):
    return myCharts.subCategory_sales_chart(region, state, city)

@app.callback(
        Output('Chart3', 'figure'), [Input('region-dropdown', 'value'), Input('state-dropdown', 'value')])
def update_chart_three(region, state):
    return myCharts.create_choropleth_map(region, state)



if __name__ == '__main__':
    app.run_server(debug=True)