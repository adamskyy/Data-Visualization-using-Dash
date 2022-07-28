from pydoc import classname
from dash import Dash, dcc, html, Input, Output, dash_table, callback
import pandas as pd
import dash_bootstrap_components as dbc
from app import df

descriptions_tab = [
    "unique id number to each passenger",
    "Survived: passenger survive(1) or died(0)",
    "passenger class",
    "name",
    "gender of passenger",
    "age of passenger",
    "number of siblings/spouses",
    "number of parents/children",
    "ticket number",
    "amount of money spent on ticket",
    "cabin category",
    "port where passenger embarked (C = Cherbourg, Q = Queenstown, S = Southampton)",
]

var_desc_tab = pd.DataFrame(
    zip(
        df.columns,
        descriptions_tab,
    ),
    columns=["Variable", "Description"],
)

home = dbc.Container(
    [
        dcc.Markdown(
            "# Variable Description",
            style={"textAlign": "center", "fontWeight": "bold"},
        ),
        dbc.Label("Show number of rows:"),
        row_drop := dcc.Dropdown(
            value=10,
            clearable=False,
            style={"width": "35%"},
            options=[10, 25, 50, 100],
        ),
        html.Br(),
        data_table := dash_table.DataTable(
            id="table",
            data=df.to_dict("records"),
            columns=[{"name": i, "id": i} for i in df.columns],
            style_table={
                "height": "400px",
                "minHeight": "200px",
                "width": "auto",
                "overflowY": "auto",
                "textOverflow": "ellipsis",
                "marginLeft": "auto",
                "marginRight": "auto",
            },
            sort_action="native",
            style_header={"backgroundColor": "#FF7300", "fontWeight": "bold"},
            style_data={"backgroundColor": "rgb(50, 50, 50)", "color": "white"},
            page_size=10,
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label("Survived:"),
                        survived_checklist := dcc.Checklist(
                            options={0: "not survived", 1: "survived"},
                            labelStyle={"display": "block"},
                        ),
                    ],
                    width=2,
                    className="card bg-light border-warning",
                ),
                dbc.Col(
                    [
                        dbc.Label("Select Pclass:"),
                        pClass_checklist := dcc.Checklist(
                            options=[x for x in sorted(df.Pclass.unique())],
                            labelStyle={"display": "block"},
                        ),
                    ],
                    width=2,
                    className="card bg-light border-warning",
                ),
                dbc.Col(
                    [
                        dbc.Label("Select sex:"),
                        sex_drop := dcc.Dropdown(
                            [x for x in sorted(df.Sex.unique())], multi=True
                        ),
                    ],
                    width=2,
                    className="card bg-light border-warning",
                ),
                dbc.Col(
                    [
                        dbc.Label("Select age:"),
                        age_slider := dcc.Slider(
                            0,
                            100,
                            1,
                            marks={"0": "0", "100": "100"},
                            tooltip={"placement": "bottom", "always_visible": True},
                        ),
                    ],
                    width=2,
                    className="card bg-light border-warning",
                ),
                dbc.Col(
                    [
                        dbc.Label("Amount of money spend on ticket:"),
                        fare_rangeslider := dcc.RangeSlider(
                            0,
                            int(max(df.Fare.unique())) + 1,
                            tooltip={"placement": "bottom", "always_visible": True},
                        ),
                    ],
                    width=4,
                    className="card bg-light border-warning",
                ),
            ],
            justify="between",
            className="mt-3 mb-4",
        ),
        var_table := dash_table.DataTable(
            data=var_desc_tab.to_dict("records"),
            columns=[{"name": i, "id": i} for i in var_desc_tab.columns],
            style_table={
                "height": "400px",
                "minHeight": "200px",
                "width": "auto",
                "overflowY": "auto",
                "textOverflow": "ellipsis",
                "marginLeft": "auto",
                "marginRight": "auto",
            },
            style_header={"backgroundColor": "#FF7300", "fontWeight": "bold"},
            style_data={"backgroundColor": "rgb(50, 50, 50)", "color": "white"},
            page_size=12,
        ),
    ]
)


@callback(
    Output(data_table, "data"),
    Output(data_table, "page_size"),
    Input(row_drop, "value"),
    Input(survived_checklist, "value"),
    Input(pClass_checklist, "value"),
    Input(sex_drop, "value"),
    Input(age_slider, "value"),
    Input(fare_rangeslider, "value"),
)
# def update_dropdown_options(survived_v, pClass_v, sex_v, age_v, row_v):
def update_dropdown_options(row_v, survived_v, pClass_v, sex_v, age_v, fare_range):
    dff = df.copy()

    if survived_v:
        surv_val = [int(x) for x in survived_v]
        dff = dff[dff.Survived.isin(surv_val)]

    if pClass_v:
        pClass_val = [int(x) for x in pClass_v]
        dff = dff[dff.Pclass.isin(pClass_val)]

    if sex_v:
        dff = dff[dff.Sex.isin(sex_v)]

    if age_v:
        dff = dff[(dff["Age"] >= 0) & (dff["Age"] < int(age_v))]

    if fare_range:
        dff = dff[
            (dff["Fare"] >= int(fare_range[0])) & (dff["Fare"] < int(fare_range[1]))
        ]

    return dff.to_dict("records"), row_v
