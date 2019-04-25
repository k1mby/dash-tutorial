import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/'
    'datasets/master/gapminderDataFiveYear.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([

    # Multiple Inputs example - slider and dropdown to update a scatter plot
    html.H3('Multiple Inputs Example'),
    html.Div('Minimum GDP'),
    dcc.Dropdown(
        id='gdp-dropdown',
        options=[{'label': i, 'value': i} for i in range(0, 11000, 1000)],
        value=0
    ),
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()}
    ),

    # Multiple outputs example - input number and table values
    html.H3('Multiple Outputs Example', style={'padding-top':'50px'}),
    html.Div([
        dcc.Input(
        id='num',
        type='number',
        value=5
        ),
        html.Table([
            html.Tr([html.Td(['x', html.Sup(2)]), html.Td(id='square')]),
            html.Tr([html.Td(['x', html.Sup(3)]), html.Td(id='cube')]),
            html.Tr([html.Td([2, html.Sup('x')]), html.Td(id='twos')]),
            html.Tr([html.Td([3, html.Sup('x')]), html.Td(id='threes')]),
            html.Tr([html.Td(['x', html.Sup('x')]), html.Td(id='x^x')]),
        ])
    ])
])

# Callback does not modify the data, creates copies of the dataframe
# Don't change variables outside their scope, avoid expensive downloads/queries in callbacks

# Multiple Inputs callback:
@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value'), Input('gdp-dropdown', 'value')])
def update_figure(selected_year, selected_gdp):
    filtered_df = df[df.year == selected_year]
    filtered_df = filtered_df[filtered_df.gdpPercap >= selected_gdp]
    
    traces = []
    
    for i in filtered_df.continent.unique():
        df_by_continent = filtered_df[filtered_df['continent'] == i]
        traces.append(go.Scatter(
            x=df_by_continent['gdpPercap'],
            y=df_by_continent['lifeExp'],
            text=df_by_continent['country'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type': 'log', 'title': 'GDP Per Capita'},
            yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }

# Multiple outputs callback:
@app.callback(
    [Output('square', 'children'),
     Output('cube', 'children'),
     Output('twos', 'children'),
     Output('threes', 'children'),
     Output('x^x', 'children')],
    [Input('num', 'value')])
def callback_a(x):
    return x**2, x**3, 2**x, 3**x, x**x


if __name__ == '__main__':
    app.run_server(debug=True)