''' Created on Jun 20, 2020

@author: jay Dash Layout  tutorial from https://dash.plotly.com/layout

'''
# -*- coding: utf-8 -*-
# import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import mysql.connector
# om plotly.validators.layout import modebar
# import random
# import datetime
from datetime import timedelta
from datetime import datetime
from tzlocal import get_localzone


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def dbconnect():
    return mysql.connector.connect(
        host="localhost",
        user="sensors",
        password="password",
        database="sensordata"
    )


mydb = dbconnect()

# from padas.io.json import json_normalize
colors = {
        'background': '#111111',
        'text': '#7FDBFF'
}


def sqlneeded(fld, sqlwhen):
    return ("select event, sensor, device, devtype, value, "
            "event_ts, DATE_FORMAT(event_ts,'%Y %m %d %T') as ts," +
            "capture_ts, DATE_FORMAT(capture_ts,'%Y %m %d %T')," +
            "DATE_FORMAT(now(),'%Y %m %d %T')" +
            " from sensortbl WHERE devtype = " +
            fld + " and " +
            sqlwhen)


def tempC2F(f):
    return (f * 9/5) + 32


def charts(
        xval='event_ts',
        yval='value',
        colorval='device',
        sqlstr="select * from sensotbl"
        ):
    millis = 1288483950000
    ts = millis * 1e-3
    local_dt = datetime.fromtimestamp(ts, get_localzone())
    utc_offset = local_dt.utcoffset()
    tz_hours_offset = utc_offset / timedelta(hours=1)
    print("SQL:", sqlstr)
    data = pd.read_sql(sqlstr, con=mydb)
    data['event_ts'] = data['event_ts'] - timedelta(hours=-1*tz_hours_offset)
#    data['TempC'] = data['TempC'].apply(tempC2F, axis=1)
    print("rows     :", len(data))
    cur = mydb.cursor()
    cur.execute("FLUSH TABLES;")

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
#


def myserver():

    config = {
        'displayModeBar': 'hover',
        'displaylogo': False
    }

    return html.Div([
        html.Div(style={
                    'backgroundColor': colors['background'],
                    'textAlign': 'center',
                    'color': colors['text']},
                 id="ts-header1"),

        html.Button('Submit', id='submit-val', n_clicks=0),
        dcc.Interval(
            id='interval-component',
            interval=10*1000,  # in milliseconds
            n_intervals=0
        ),
        html.Div(

            style={'backgroundColor': colors['background']},

            children=[
                html.Div([
                    html.H3(
                        children='Temperature',
                        style={
                            'textAlign': 'center',
                            'color': colors['text']
                            }
                    ),
                    dcc.Graph(id='graphg1', config=config),
                    ], className="six columns"
                ),


                html.Div([
                    html.H3(children='Humidity',
                            style={
                                    'textAlign': 'center',
                                    'color': colors['text']
                                    }
                            ),
                    dcc.Graph(id='graphg2', config=config),
                ], className="six columns"),
            ], className="row"),

        html.Div(

            style={'backgroundColor': colors['background']},

            children=[
                html.Div([
                    html.H3(
                        children="Data Table",
                        style={
                            'textAlign': 'center',
                            'color': colors['text']
                            }
                    )
                    # generate_table(df)
                ])
            ])
        ])

# def sqlneeded(fld, sqlwhen):
#   return "select * from sensortbl WHERE devtype = " + fld + " and " + sqlwhen


sqlwhen = "event_ts >= now() - INTERVAL 48 HOUR"


#
# Multiple components can update everytime interval gets fired.
#


@app.callback(
    Output('ts-header1', 'children'),
    [Input('interval-component', 'n_intervals')])
def gents(n):
    return html.Div([
        html.H3('Sensors'),
        html.H4(datetime.now().strftime("%c"))
    ])


@app.callback(
    Output('graphg1', 'figure'),
    [Input('interval-component', 'n_intervals')])
def gencharts1(n):
    return charts(
            'event_ts',
            yval='value',
            colorval='device',
            sqlstr=sqlneeded("'TempC'", sqlwhen))


@app.callback(
    Output('graphg2', 'figure'),
    [Input('interval-component', 'n_intervals')])
def gencharts2(n):
    return charts(
            'event_ts',
            yval='value',
            colorval='device',
            sqlstr=sqlneeded("'Humidity'", sqlwhen))


def mainpage():

    return html.Div([
        # represents the URL bar, doesn't render anything
        dcc.Location(id='url', refresh=False),

        dcc.Link('Navigate to "/"', href='/'),
        html.Br(),
        dcc.Link('Monitor Sensors', href='Sensors-myserver'),

        # content will be rendered in this element
        html.Div(id='page-content')
    ])


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):

    print("#################################")
    print("pathnam:", pathname)
    if pathname == 'Sensors-myserver':
        return myserver()
    else:
        return html.Div([
            html.H3('You are on page {}'.format(pathname))
        ])


app.layout = myserver

if __name__ == '__main__':
    print("Starting..............")
#    print("rows     :", len(data))
    app.run_server(debug=True)
