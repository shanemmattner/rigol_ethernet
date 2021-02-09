
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div(id='status_indicator',
        children='GEN3 V2 cycle testing', style={'fontSize':50}),
    html.Button('RUN', id='btn_run', n_clicks=0, style={'padding':'100px 100px', 'fontSize':50}),
    html.Button('STOP', id='btn_stop', n_clicks=0, style={'padding':'100px 100px', 'fontSize':50}),
    dcc.Interval(
        id='interval-component',
        interval=1*1000, # in milliseconds
        n_intervals=0
        ),
    html.Div(id='null_1'),
    html.Div(id='null_2'),
    html.Div(id='null_3'),

    
])


@app.callback(
    dash.dependencies.Output('null_1', 'children'),
    [dash.dependencies.Input('btn_run', 'n_clicks')])
def update_output(n_clicks):

    if not n_clicks:
        raise PreventUpdate

    f = open('run_testing.txt', 'w')
    f.write('1')
    f.close()
    raise PreventUpdate
    
@app.callback(
    dash.dependencies.Output('null_2', 'children'),
    [dash.dependencies.Input('btn_stop', 'n_clicks')])
def update_output(n_clicks):

    if not n_clicks:
        raise PreventUpdate
    f = open('run_testing.txt', 'w')
    f.write('0')
    f.close()
    raise PreventUpdate

@app.callback(dash.dependencies.Output('status_indicator', 'children'),
              dash.dependencies.Input('interval-component', 'n_intervals'))
def update_metrics(n):
    f = open('run_testing.txt','r')
    msg = f.read()
    f.close()
    try:
        run = int(msg[0])
    except:
        f = open('run_testing.txt', 'w')
        f.write('0')
        f.close()
        run = 0

    if run==1:
        return "GEN3 V2 Cycle Test:  RUNNING"
    else:
        return "GEN3 V2 Cycle Test:  STOPPED"



if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
