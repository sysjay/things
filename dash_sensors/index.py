import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

### local libraries
from sensorapp import SensorApp, build_graphs
from app import App, build_graph
from homepage import Homepage

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
                dcc.Location(id='url', refresh=False),
                html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    print("JJJJJJJJJJJJ")
    print(pathname)
    if pathname == '/time-series':
        return App()
    elif pathname == '/sensors':
        return SensorApp()
    else:
        return Homepage()


@app.callback(
    Output('sensor_output', 'children'),
    [Input('sensor_dropdown', 'value')])
def update_graph(city):
    graph = build_graphs(city)
    return graph


@app.callback(
    Output('output', 'children'),
    [Input('pop_dropdown', 'value')])
def update_graph(city):
    graph = build_graphs(city)
    return graph



if __name__ == '__main__':
    app.run_server(debug=True)
