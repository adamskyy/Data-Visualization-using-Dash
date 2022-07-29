from dash import Dash, dcc, html, Input, Output, dash_table, callback
import dash_bootstrap_components as dbc

from pages import variable_analysis, variable_description, basic_analysis


app = Dash(external_stylesheets=[dbc.themes.LUX], suppress_callback_exceptions=True)
app.config.suppress_callback_exceptions = True


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "14rem",
    "padding": "2rem 1rem",
    "background-color": "#FF7300",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "14rem",
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
                dbc.NavLink(
                    "Univariate Variable Analysis", href="/var_analysis", active="exact"
                ),
                dbc.NavLink("Basic Analysis", href="/basic_analysis", active="exact"),
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
        return variable_description.page1
    elif pathname == "/var_analysis":
        return variable_analysis.page2
    elif pathname == "/basic_analysis":
        return basic_analysis.page3
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    app.run_server(debug=False)
