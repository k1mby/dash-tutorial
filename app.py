import dash 
import dash_core_components as dcc 
import dash_html_components as html 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# __name__ to ensure right path when loading from assets folder
# external_stylesheets/external_scripts, assets_external_path to load from CDN
# assets_ignored to prevent loading files
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Defining colors to use in styles
colors = {
    'background': '#D7D7D7',
    'text': '#4D4D4D'
}

# Layout is a tree structure of components
# children property: inputs and outputs are properties of components
# children is first argument and can be omitted
# We have an outer div with H1, div and graph inside
app.layout = html.Div(children=[

    # Component class for every HTML tag and keywords for all attributes (camelCase)
    # Style is given as dictionary, class is className
    html.H1(
        children='Dash Demo',
        style={
            'textAlign' : 'center',
            'color' : colors['text']
        }
    ),

    # Not all components are pure HTML, can be built with React
    html.Div(
        children='A Sample Bar Chart',
        style={
            'textAlign' : 'center',
            'color' : colors['text']
        }
        ),

    # figure argument is same figure from Plotly
    # https://plot.ly/python/reference/
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization',
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)