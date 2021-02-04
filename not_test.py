
import dash
import dash_html_components as html
import dash_core_components as dcc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div(id='container-button-basic',
             children='Enter a value and press submit'),
    html.Button('btn1', id='add', n_clicks=0),
    html.Button('btn2', id='subtract', n_clicks=0),
    dcc.Interval(
        id='interval-component',
        interval=1*1000, # in milliseconds
        n_intervals=0
        ),
    html.Div(id='null_1'),
    html.Div(id='null_2'),

    
])


@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('add', 'n_clicks')])
def update_output(n_clicks):
    return 'The button has been clicked {} times'.format(
        n_clicks
    )

@app.callback(
    dash.dependencies.Output('null_2', 'children'),
    [dash.dependencies.Input('subtract', 'n_clicks')])
def update_output(n_clicks):
    return 'The button has been clicked {} times'.format(
        n_clicks
    )

@app.callback(dash.dependencies.Output('null_1', 'children'),
              dash.dependencies.Input('interval-component', 'n_intervals'))
def update_metrics(n):

    return [
        n
    ]


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
