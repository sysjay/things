# ## Data
import pandas as pd
import pickle
# ## Graphing
import plotly.graph_objects as go
# ## Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
# ## Navbar
from navbar import Navbar


import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="sensors",
    password="password",
    database="sensordata"
    )

# TODO test the groupby versus unique for performance
#  dg = df.groupby({"devtyp"}).count()

sqlwhen = "where event_ts >= now() - INTERVAL 48 HOUR"
df = pd.read_sql("SELECT * FROM sensortbl" + " " + sqlwhen, mydb,"event_ts")
dg = df['devtype'].unique()
options=[{'label': i, 'value': i} for i in dg]

nav = Navbar()
header = html.H3(
    'Select the name of the Sensor!'
)

dropdown = html.Div(dcc.Dropdown(
    id = 'sensor_dropdown',
    options = options,
    value = 'Humidity'
))

output = html.Div(id = 'sensor_output',
                children = [],
                )

def SensorApp():
    layout = html.Div([
        nav,
        header,
        dropdown,
        output
    ])
    return layout

# from padas.io.json import json_normalize
colors = {
        'background': '#111111',
        'text': '#7FDBFF'
}


def build_graphs(devtyp):
    filter = df["devtype"]==devtyp
    dfilter = df[filter]
    data = [go.Scatter(x = dfilter.index,
                       y = dfilter['value'],
                       marker = {'color': 'orange'})]
    graph = dcc.Graph(
                figure = {
                    'data': data,
                    'layout': go.Layout(
                                title = '{} Population Change'.format(devtyp),
                                yaxis = {'title': 'Population'},
                                hovermode = 'closest'
                                  )
                        })
    return graph
