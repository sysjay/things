import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import mysql.connector
# pip install pyorbital
from pyorbital.orbital import Orbital


def dbconnect():
    return mysql.connector.connect(
        host="localhost",
        user="sensors",
        password="password",
        database="sensordata"
        )


mydb = dbconnect()

satellite = Orbital('TERRA')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H4('TERRA Satellite Live Feed'),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000,  # in milliseconds
            n_intervals=0
        )
    ])
)


@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    lon, lat, alt = satellite.get_lonlatalt(datetime.datetime.now())
    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        html.Span('Longitude: {0:.2f}'.format(lon), style=style),
        html.Span('Latitude: {0:.2f}'.format(lat), style=style),
        html.Span('Altitude: {0:0.2f}'.format(alt), style=style)
    ]


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):

    def sqlneeded(fld, sqlwhen):
        return ("select event, sensor, device, devtype, value, "
                "event_ts, DATE_FORMAT(event_ts,'%Y %m %d %T') as ts," +
                "capture_ts, DATE_FORMAT(capture_ts,'%Y %m %d %T')," +
                "DATE_FORMAT(now(),'%Y %m %d %T')" +
                " from sensortbl WHERE devtype = " +
                fld + " and " +
                sqlwhen)

    sqlwhen = "event_ts >= DATE_SUB(UTC_TIMESTAMP(), INTERVAL 100 HOUR)"
    # #sqlwhen = "event_ts >= '2020-07-08 19:10:50'"
    sqlstr = sqlneeded("'TempC'", sqlwhen)
    print("####")
    print("SQL:", sqlstr)
    print("####")
    df = pd.read_sql(sqlstr, con=mydb)
    print(df)
    print("rows     :", len(df))

    fig = px.scatter(df, x="event_ts", y="value", color='device')
    cur = mydb.cursor()
    cur.execute("FLUSH TABLES;")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
