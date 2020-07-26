'''
Created on Jun 20, 2020

@author: jay
Dash Layout  tutorial from https://dash.plotly.com/layout

'''
# -*- coding: utf-8 -*-
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output


import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="sensors",
    password="password",
    database="sensordata"
)

import random
import datetime

sql = "SELECT * FROM sensortbl WHERE devtype = 'TempC'"
#sql = "SELECT * FROM sensortbl"
df = pd.read_sql(sql, con=mydb)


#from padas.io.json import json_normalize
colors = {
        'background': '#111111',
        'text': '#7FDBFF'
}



def charts(fld,default='Y'):
#    fig1 = px.bar(data,x='ts2',y=fld)
    sql = "SELECT * FROM sensortbl WHERE devtype = '" + fld + "'"
    print("SQL:", sql)
    data = pd.read_sql(sql, con=mydb)
    #data = pd.read_csv('~/workspace-sensors2/esp8266/sensors.csv')
    print("rows     :",len(data))
    fig = px.scatter(data, x="ts2", y="value", color="device")
    fig.update_layout(plot_bgcolor=colors['background'], paper_bgcolor=colors['background'],
                      legend=dict(
                          font=dict(
                              size=16,
                              color=colors['text'])))
    fig.update_yaxes(tickfont=dict(color=colors['text'],size=16),title_font=dict(size=18),color=colors['text'])
    fig.update_xaxes(tickfont=dict(color=colors['text'],size=16),title_font=dict(size=18),color=colors['text'])
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


def main():
    print("inside")
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app2 = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app3 = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app2.layout = html.Div([
    html.Label('Dropdown'),
    dcc.Dropdown(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': u'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='MTL'
    ),

    html.Label('Multi-Select Dropdown'),
    dcc.Dropdown(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': u'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value=['MTL', 'SF'],
        multi=True
    ),

    html.Label('Radio Items'),
    dcc.RadioItems(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': u'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='MTL'
    ),

    html.Label('Checkboxes'),
    dcc.Checklist(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': u'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value=['MTL', 'SF']
    ),

    html.Label('Text Input'),
    dcc.Input(value='MTL', type='text'),

    html.Label('Slider'),
    dcc.Slider(
        min=0,
        max=9,
        marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(1, 6)},
        value=5,
    ),
], style={'columnCount': 2})





#     app6 = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#
#     app6.layout = html.Div(
#         style={'backgroundColor': colors['background']},
#         children=[
#
#             html.H1(
#                 children='HELLO Jay',
#                 style={
#                         'textAlign': 'center',
#                         'color': colors['text']
#                     }
#             ),
#
#             html.Div(className='row', children=[
#             html.H2(children='Charts'),
#             html.Div(
#                 style={
#                     'textAlign':'center',
#                     'color': colors['text'],
#                     'width':'30%',
#                     'display':'inline-block'
#                 },
#
#
#                     html.Div([
#                         html.H3('Colomn 1'),
#                         dcc.Graph(id="temp chart",figure=charts('temperature'))
#                     ],className = 'six columns'),
#
#
#                     html.Div([
#                         html.H3('Colomn 2'),
#                         dcc.Graph(id="humidity chart", figure=charts('humidity'))
#                     ],className = 'six columns')
#
#             ),
#             ]
#             )
#         ]
#     )

    app7 = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app7.layout = html.Div([
        html.Div(

            style={'backgroundColor': colors['background']},

            children=[
            html.Div([
                html.H3(children='Temperature',
                        style={
                                'textAlign': 'center',
                                'color': colors['text']
                                }                        ),
                dcc.Graph(id='g1', figure=charts('temperature'))
            ], className="six columns"),

            html.Div([
                html.H3(children='Humidity',
                        style={
                                'textAlign': 'center',
                                'color': colors['text']
                                }
                ),
                dcc.Graph(id='g2', figure=charts('humidity'))
            ], className="six columns"),
        ], className="row")
    ])




    app3.layout = html.Div([
        dcc.Input(id='my-id', value='initial value', type='text'),
        html.Div(id='my-div')
    ])


    @app3.callback(
        Output(component_id='my-div', component_property='children'),
        [Input(component_id='my-id', component_property='value')]
    )
    def update_output_div(input_value):
        return "text entered:    {}".format(input_value)


    app5 = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    styles = {
        'pre': {
            'border': 'thin lightgrey solid',
            'overflowX': 'scroll'
        }
    }

    df = pd.DataFrame({
        "x": [1,2,1,2],
        "y": [1,2,3,4],
        "customdata": [1,2,3,4],
        "fruit": ["apple", "apple", "orange", "orange"]
    })

    fig = px.scatter(df, x="x", y="y", color="fruit", custom_data=["customdata"])

    fig.update_layout(clickmode='event+select')

    fig.update_traces(marker_size=20)

    app5.layout = html.Div([
        dcc.Graph(
            id='basic-interactions',
            figure=fig
        ),

        html.Div(className='row', children=[
            html.Div([
                dcc.Markdown("""
                    **Hover Data**

                    Mouse over values in the graph.
                """),
                html.Pre(id='hover-data', style=styles['pre'])
            ], className='three columns'),

            html.Div([
                dcc.Markdown("""
                    **Click Data**

                    Click on points in the graph.
                """),
                html.Pre(id='click-data', style=styles['pre']),
            ], className='three columns'),

            html.Div([
                dcc.Markdown("""
                    **Selection Data**

                    Choose the lasso or rectangle tool in the graph's menu
                    bar and then select points in the graph.

                    Note that if `layout.clickmode = 'event+select'`, selection data also
                    accumulates (or un-accumulates) selected data if you hold down the shift
                    button while clicking.
                """),
                html.Pre(id='selected-data', style=styles['pre']),
            ], className='three columns'),

            html.Div([
                dcc.Markdown("""
                    **Zoom and Relayout Data**

                    Click and drag on the graph to zoom or click on the zoom
                    buttons in the graph's menu bar.
                    Clicking on legend items will also fire
                    this event.
                """),
                html.Pre(id='relayout-data', style=styles['pre']),
            ], className='three columns')
        ])
    ])


    @app.callback(
        Output('hover-data', 'children'),
        [Input('basic-interactions', 'hoverData')])
    def display_hover_data(hoverData):
        return json.dumps(hoverData, indent=2)


    @app.callback(
        Output('click-data', 'children'),
        [Input('basic-interactions', 'clickData')])
    def display_click_data(clickData):
        return json.dumps(clickData, indent=2)


    @app.callback(
        Output('selected-data', 'children'),
        [Input('basic-interactions', 'selectedData')])
    def display_selected_data(selectedData):
        return json.dumps(selectedData, indent=2)


    @app.callback(
        Output('relayout-data', 'children'),
        [Input('basic-interactions', 'relayoutData')])
    def display_relayout_data(relayoutData):
        return json.dumps(relayoutData, indent=2)






    app7.run_server(debug=True)

if __name__ == '__main__':
    print("Starting..............")
    data = pd.read_csv('~/workspace-sensors2/esp8266/sensors.csv')
    print("rows     :",len(data))
    main()
    print("ended.................")
