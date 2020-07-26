# ## Data
import pandas as pd
# import pickle
# ## Graphing
import plotly.graph_objects as go
import plotly.express as px
# ## Dash
# import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
# import dash_bootstrap_components as dbc
# from dash.dependencies import Output, Input
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
# df = pd.read_sql("SELECT * FROM sensortbl" + " " + sqlwhen, mydb, "event_ts")
df = pd.read_sql("SELECT * FROM sensortbl" + " " + sqlwhen, mydb)
dg = df['devtype'].unique()
options = [{'label': i, 'value': i} for i in dg]
cur = mydb.cursor()
cur.execute("FLUSH TABLES;")

nav = Navbar()
header = html.H5(
    'Select the name of the Sensor!'
)

dropdown = html.Div(dcc.Dropdown(
    id='sensor_dropdown',
    options=options,
    value='TempC'
))

output = html.Div(
            id='sensor_output',
            children=[],
         )


def SensorApp():
    layout = html.Div([
        nav,
        header,
        dropdown,
        output
    ])
    return layout


bg_color = 'rgb(60, 60, 60)'
paper_bgcolor = bg_color
txt_color = 'white'
txt_font = 'Arial'
txt_size = 18

axis_style = {
            'family': txt_font,
            'color':  txt_color,
            'size':   txt_size
            }

plot_layout = {
    'font': axis_style,
    'paper_bgcolor': paper_bgcolor,
    'plot_bgcolor': bg_color
    }


def build_graphs(devtyp, chartyp='line'):
    header = html.H6(
        'Sensor graphs'
    )

    header2 = html.H6(
        'Sensor data'
    )

    print(plot_layout)
    filter = df["devtype"] == devtyp
    dfilter = df[filter]
    if chartyp == 'line':
        fig = px.line(dfilter, x="event_ts", y="value", color="device")
        fig.update_layout(plot_layout)
        graph = dcc.Graph(figure=fig)
    elif chartyp == "scatter":
        fig = px.scatter(dfilter,
                         x="event_ts",
                         y="value",
                         color="device",
                         symbol="sensor")
        fig.update_layout(font=axis_style)
        graph = dcc.Graph(figure=fig)
    else:
        data = [go.Scatter(x=dfilter.index,
                           y=dfilter['value'],
                           marker={'color': 'orange'}
                           )
                ]
        graph = dcc.Graph(
                    figure={
                        'data': data,
                        'layout': go.Layout(
                                    title='{} Change'.format(devtyp),
                                    yaxis={'title': devtyp},
                                    hovermode='closest'
                                    )
                            })

    tbl = dash_table.DataTable(
            id='table',
            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            fixed_rows={'headers': True},
            style_table={
                    'maxHeight': '200',
                    'height': 600,
                    'overflowY': 'scroll'
            },
            style_cell={
                'backgroundColor': bg_color,
                'font_size': str(txt_size) + 'px',
                'font': txt_font,
                'color': txt_color
            },
            columns=[{'name': i, 'id': i} for i in dfilter.columns],
            style_cell_conditional=[
                {
                    'if': {'column_id': c},
                    'textAlign': 'left'
                } for c in ['event_ts', 'capture_ts', 'sensor', 'devtype']
            ],
            data=dfilter.to_dict('records')
    )
    layout = html.Div([
            header,
            graph,
            header2,
            tbl
            ])
    return layout
