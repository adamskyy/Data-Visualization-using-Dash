from dash import Dash, dcc, html, Input, Output, dash_table, callback
import pandas as pd
import dash_bootstrap_components as dbc
import dash_daq as daq
from . import data_import as dt
import plotly.express as px

page2 = dbc.Container(
    [
        dcc.Markdown("# Univariate Variable Analysis", className="text-center"),
        html.Hr(),
        dcc.Markdown(
            """
            - Categorical Variables: Survived, Sex, Pclass, Embarked, Cabin, Name, Ticket, Sibsp and Parch,
            """,
            className="text-dark",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label("Select variable:"),
                        survived_checklist := dcc.RadioItems(
                            id="radio",
                            options=[
                                x
                                for x in dt.df.columns
                                if x
                                not in [
                                    "Fare",
                                    "Age",
                                    "PassengerId",
                                    "Cabin",
                                    "Name",
                                    "Ticket",
                                ]
                            ],
                            labelStyle={"display": "block"},
                            value="Survived",
                        ),
                    ],
                    width=2,
                    className="card bg-light border-warning",
                ),
                dbc.Col([dcc.Graph(id="graph")]),
            ]
        ),
        html.Br(),
        dcc.Markdown(
            """
            - Numerical Variable: Fare, age and passengerId
            """,
            className="text-dark",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label("Select variable:"),
                        survived_checklist := dcc.RadioItems(
                            id="radio-2",
                            options=[
                                x
                                for x in dt.df.columns
                                if x
                                in [
                                    "Fare",
                                    "Age",
                                ]
                            ],
                            labelStyle={"display": "block"},
                            value="Age",
                        ),
                        daq.NumericInput(
                            id="numeric-input-1",
                            value=50,
                            label="Histogram bins:",
                            labelPosition="top",
                            min=10,
                            max=100,
                            className="mt-5",
                        ),
                        daq.BooleanSwitch(
                            on=False,
                            label="Show with survived",
                            id="button-2",
                            labelPosition="top",
                            color="#FF7300",
                            className="mt-5",
                        ),
                    ],
                    width=2,
                    className="card bg-light border-warning",
                ),
                dbc.Col([dcc.Graph(id="graph-2")]),
            ],
        ),
    ]
)


@callback(Output("graph", "figure"), Input("radio", "value"))
def update_bar_chart(value):
    # get feature
    var = dt.df[value]
    # count number of categorical variable(value/sample)
    varValue = var.value_counts()
    fig = px.bar(
        dt.df,
        x=varValue.index,
        y=varValue,
        labels={"x": "", "y": "Frequency"},
    )
    return fig


@callback(
    Output("graph-2", "figure"),
    Input("radio-2", "value"),
    Input("numeric-input-1", "value"),
    Input("button-2", "on"),
)
def update_hist_chart(value_radio, numeric_input_1, surv_bool_2):
    if surv_bool_2:
        fig = px.histogram(
            dt.df,
            x=value_radio,
            nbins=numeric_input_1,
            marginal="box",
            color="Survived",
        )
    else:
        fig = px.histogram(dt.df, x=value_radio, nbins=numeric_input_1, marginal="box")
    return fig
