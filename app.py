from dash import Dash, dcc, html, Input, Output, dash_table, callback
import pandas as pd
import dash_bootstrap_components as dbc

import pages.variable_description as pg1

app = Dash(external_stylesheets=[dbc.themes.LUX], suppress_callback_exceptions=True)
app.config.suppress_callback_exceptions = True

df = pd.read_csv("train.csv")

df.info()

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "12rem",
    "padding": "2rem 1rem",
    "background-color": "#FF7300",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "12rem",
    "margin-right": "0rem",
    "padding": "2rem 1rem",
    "width": "auto",
    "background-color": "#939393",
}

sidebar = html.Div(
    [
        html.H1("Titanic dataset", style={"fontWeight": "bold"}),
        html.Hr(),
        html.P("Machine Learning from Disaster", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Variable Description", href="/", active="exact"),
                dbc.NavLink("Page 1", href="/page-1", active="exact"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)


app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return pg1.home
    elif pathname == "/page-1":
        return html.P("This is the content of page 1. Yay!")
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    app.run_server(debug=True, port=3070)
