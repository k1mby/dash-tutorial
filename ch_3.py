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

# Slider and dropdown to update a scatter plot
app.layout = html.Div([
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
    )
])

# Callback does not modify the data, creates copies of the dataframe
# Don't change variables outside their scope, avoid expensive downloads/queries in callbacks
# We can have multiple inputs - slider and dropdown here 
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


if __name__ == '__main__':
    app.run_server(debug=True)