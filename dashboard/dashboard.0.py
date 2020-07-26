'''
Created on Jun 20, 2020

@author: jay
Dash Layout  tutorial from https://dash.plotly.com/layout

'''
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
jsonstr = '{"pressure": "1003.28", "humidity": "34.03", "ts2": "2020/06/21 01:22:06.056734", "uid": "3c71bf62", "ts": "(2020, 6, 21, 6, 1, 22, 6, 56734)", "temp": "24.62"}'
dframe = pd.read_json(jsonstr, orient='index')
jsonstr = '{"pressure": "1003.43", "humidity": "33.85", "ts2": "2020/06/21 01:24:56.046621", "uid": "3c71bf62", "ts": "(2020, 6, 21, 6, 1, 24, 56, 46621)", "temp": "24.55"}'
dframe.append(pd.read_json(jsonstr, orient='index'))
jsonstr = '{"pressure": "1003.42", "humidity": "33.89", "ts2": "2020/06/21 01:26:20.051181", "uid": "3c71bf62", "ts": "(2020, 6, 21, 6, 1, 26, 20, 51181)", "temp": "24.54"}'
dframe.append(pd.read_json(jsonstr, orient='index'))
jsonstr = '{"pressure": "1003.40", "humidity": "33.71", "ts2": "2020/06/21 01:27:02.053625", "uid": "3c71bf62", "ts": "(2020, 6, 21, 6, 1, 27, 2, 53625)", "temp": "24.55"}'
dframe.append(pd.read_json(jsonstr, orient='index'))
jsonstr = '{"pressure": "1003.43", "humidity": "33.72", "ts2": "2020/06/21 01:27:44.058348", "uid": "3c71bf62", "ts": "(2020, 6, 21, 6, 1, 27, 44, 58348)", "temp": "24.54"}'
dframe.append(pd.read_json(jsonstr, orient='index'))


app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)