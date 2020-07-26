import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def serve_layout():
    return html.Div([
        dcc.Interval(id='refresh', interval=200),
        html.H1('The time is: ' + str(datetime.datetime.now()))
        ])


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=True)
