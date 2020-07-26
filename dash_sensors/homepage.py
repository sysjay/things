import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


from navbar import Navbar
nav = Navbar()
RPi_href = "https://s3.us-east-2.amazonaws.com/jtcsoftware.com/pisensors.html"

sqlstr = '''
select sensortbl.*
    from (select device, devtyp, value from sensotbl as


'''


body = dbc.Container(
    [
       dbc.Row(
           [
               dbc.Col(
                  [
                     html.H2("Jay's Things"),
                     html.A("Raspberry Pi GPIO notes\n",
                            href=RPi_href,
                            target="_blank"),


                     dbc.Button("View details", color="secondary"),
                   ],
                  md=4,
               ),
               dbc.Col(
                 [
                     html.H2("Graph"),
                     dcc.Graph(
                         figure={"data": [{"x": [1, 2, 3], "y": [1, 4, 9]}]}
                            ),
                        ]
                     ),
                ]
            )
       ],
    className="mt-4"
)


def Homepage():
    layout = html.Div([
        nav,
        body
    ])
    return layout


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
app.layout = Homepage()
if __name__ == "__main__":
    app.run_server()
