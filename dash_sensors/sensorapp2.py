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

import plotly.express as px

import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="sensors",
    password="password",
    database="sensordata"
    )

# TODO test the groupby versus unique for performance
#  dg = df.groupby({"devtyp"}).count()

sqlwhen = "where event_ts >= now() - INTERVAL 4 HOUR"
df = pd.read_sql("SELECT * FROM sensortbl" + " " + sqlwhen, mydb)
dg = df['devtype'].unique()
options=[{'label': i, 'value': i} for i in dg]
print (dg)

import multiprocessing
nav = Navbar()
header = html.H3(
    'Select from sensor database: ' + sqlwhen
)

dropdown = html.Div(dcc.Dropdown(
    id = 'sensor_dropdown',
    options = options,
    value = 'Humidity'
))

output = html.Div(id = 'sensor_output',
                children = [],
                )

tables = html.Div(id = 'sensor_tables',
                children = [],
                )

def SensorApp():
    layout = html.Div([
        nav,
        header,
        dropdown,
        output
#        tables
    ])
    return layout

# from padas.io.json import json_normalize
colors = {
        'background': '#111111',
        'text': '#7FDBFF'
}


def chartthis(data, xval="event_ts", yval="value", colorval="devtype"):
    fig = px.scatter(data, x=xval, y=yval,
                     color=colorval)

    fig.update_traces(marker=dict(size=6,
                                  line=dict(width=0.62,
                                            color='cyan')),
#     marker_symbol=33,
                      selector=dict(mode='markers'))
    fig.update_layout(plot_bgcolor=colors['background'],
                      paper_bgcolor=colors['background'],
                      legend=dict(
                      font=dict(
                            size=16,
                            color=colors['text'])))
    fig.update_yaxes(tickfont=dict(color=colors['text'],
                                   size=16),
                     title_font=dict(size=18),
                     color=colors['text'])
    fig.update_xaxes(tickfont=dict(color=colors['text'],
                                   size=16),
                     title_font=dict(size=18),
                     color=colors['text'])
    fig.update_yaxes(range=[0, 100])
    return fig


def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

def build_tables(devtyp):
    print("Enter:Build tables")
    filter = df["devtype"]==devtyp
    dfilter = df[filter]
    print("Exit :Build tables")
    return generate_table(df)

def build_graphs(devtyp):
    print("Enter:Build Graphs")
    filter = df["devtype"]==devtyp
    dfilter = df[filter]
    graph = dcc.Graph(figure=chartthis(df,colorval='device'))
    print("Exit :Build Graphs")

        #figure = {
        #            'data': data,
        #            'layout': go.Layout(
        #                        title = '{} Population Change'.format(devtyp),
        #                        yaxis = {'title': 'Population'},
        #                        hovermode = 'closest'
        #                          )
        #                })
    return graph
