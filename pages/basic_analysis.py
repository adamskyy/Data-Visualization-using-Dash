from click import style
from . import data_import as dt
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from dash import callback
import app


def surv_rate_by(column):
    data = dt.df.groupby(column).sum().reset_index()
    fig = px.pie(
        data,
        names=column,
        values="Survived",
        hole=0.4,
    )
    fig.update_layout(title=f"Survival rate by {column}", template="plotly")
    return fig


def violin_age_by(column):
    figure = px.violin(
        dt.df,
        x=column,
        y="Age",
        color="Survived",
        box=True,
        points="all",
        hover_data=dt.df.columns,
    )
    return figure


page3 = dbc.Container(
    [
        dcc.Markdown("# Basic Analysis", className="text-center"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label("Select variable:"),
                        survived_checklist := dcc.RadioItems(
                            id="radio-3",
                            options=[
                                x
                                for x in dt.df.columns
                                if x
                                not in [
                                    "Survived",
                                    "PassengerId",
                                    "Name",
                                    "Age",
                                    "Ticket",
                                    "Fare",
                                    "Cabin",
                                ]
                            ],
                            labelStyle={"display": "block"},
                            value="Sex",
                        ),
                    ],
                    width=2,
                    className="card bg-light border-warning",
                ),
                dbc.Col(dcc.Graph(id="graph-3", figure=surv_rate_by("Sex"))),
            ],
            className="mt-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label("Select variable:"),
                        survived_checklist := dcc.RadioItems(
                            id="radio-4",
                            options=[
                                x
                                for x in dt.df.columns
                                if x
                                not in [
                                    "Survived",
                                    "PassengerId",
                                    "Name",
                                    "Age",
                                    "Ticket",
                                    "Fare",
                                    "Cabin",
                                ]
                            ],
                            labelStyle={"display": "block"},
                            value="Sex",
                        ),
                    ],
                    width=2,
                    className="card bg-light border-warning",
                ),
                dbc.Col(
                    dcc.Graph(
                        id="graph-4",
                        figure=violin_age_by("Sex"),
                    )
                ),
            ],
            className="mt-3",
        ),
    ]
)


@callback(
    Output("graph-3", "figure"),
    Input("radio-3", "value"),
)
def update_pie_chart(value_radio_3):
    if value_radio_3:
        return surv_rate_by(value_radio_3)


@callback(
    Output("graph-4", "figure"),
    Input("radio-4", "value"),
)
def update_volin_chart(value_radio_4):
    if value_radio_4:
        return violin_age_by(value_radio_4)
