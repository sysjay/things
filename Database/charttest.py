import sys
sys.path.append("/home/jay/workspace-sensors2/FirstDashboard/tools")
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

import timing
import pandas as pd

from flask import Flask

import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="sensors",
    password="password",
    database="sensordata"
)

import random
import datetime

ts = datetime.datetime.now()
ts2 = ts
sql = "SELECT * FROM sensortbl WHERE devtype = 'TempC'"
#sql = "SELECT * FROM sensortbl"
df = pd.read_sql(sql, con=mydb)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
config = {
    'scrollZoom': False,
    'displayModeBar': True,
    'editable': True,
    'showLink':False,
    'displaylogo': False
    }
fig = px.scatter(df, x="capture_ts", y="value", color="device")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
       *** Dash:*** A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True,config=config)

#    app.run_server(debug=True, host ='0.0.0.0',port='5000')

