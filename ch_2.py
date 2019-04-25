import dash 
import dash_core_components as dcc 
import dash_html_components as html 

import pandas as pd

from dash.dependencies import Input, Output

# Creates a table component
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

colors = {
    'background': '#D7D7D7',
    'text': '#4D4D4D'
}

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/'
    'c78bf172206ce24f77d6363a2d754b59/raw/'
    'c353e8ef842413cae56ae3920b8fd78468aa4cb2/'
    'usa-agricultural-exports-2011.csv')

# Can write text using markdown + Markdown component 
markdown_text = '''
### This is a Markdown Header

Sample _fancy_ **markdown** ~~words~~ text :)   
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
'''

# __name__ to ensure right path when loading from assets folder
# external_stylesheets/external_scripts, assets_external_path to load from CDN
# assets_ignored to prevent loading files
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Layout is a tree structure of components
# children property: inputs and outputs are properties of components
# children is first argument and can be omitted
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

    # Using the Markdown component to format text
    dcc.Markdown(children=markdown_text),

    # Not all components are pure HTML, can be built with React
    html.Div(
        children='A Sample Bar Chart',
        style={
            'textAlign' : 'center',
            'color' : colors['text']
        }
        ),

    # Graph uses Plotly https://plot.ly/python/reference/
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
    ),

    html.H4(
        children='Sample Table - US Agriculture Exports (2011)',
        style={
            'textAlign' : 'center',
            'color' : colors['text']
        }
    ),

    # Create the table
    html.Div(
        children=generate_table(df),
        style={
            'margin' : '0 auto',
            'width' : '75%',
            'overflow' : 'scroll'
        }
    ),

    # Inputs/Outputs are properties of components
    dcc.Input(id='my-input', value='initial value', type='text'),
    html.Div(id='my-div')

])

# Input is value property of component with id my-input 
# Output is children property of component with id my-div
# When input property changes function wrapped with @app.callback decorator is called
# When app starts all callbacks called to populate output components with initial values
@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-input', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)

if __name__ == '__main__':
    app.run_server(debug=True)