import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
from datetime import datetime as dt
import dash_table


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])

app.layout = html.Div([

    dbc.Row([
        # Dataset dropdown
        dbc.Col(html.Div(
            dcc.Dropdown(
                id="dataset-dropdown",
                options=[
                    {"label": "Set One", "value": "set1"},
                    {"label": "Set Two", "value": "set2"},
                ],
                value="set1",
            ),
        )),
        # New dataset button
        dbc.Col(html.Div(
            dbc.Button(
                "New Dataset",
                id="new-dataset-button",
                n_clicks=0
            ),
        )),

    ]),

    dbc.Row([
        # Dataset value name
        dbc.Col(html.Div(
            dbc.Input(
                id="dataset-value-name-input",
                placeholder="Dataset Value Name",
                type="text",
            ),
        )),

        # Goal text
        dbc.Col(html.Div(
            "Goal:"
        )),

        # Goal value
        dbc.Col(html.Div(
            dbc.Input(
                id="goal-value-input",
                placeholder="Goal Value",
                type="number",
            ),
        )),

        # Per text
        dbc.Col(html.Div(
            "per"
        )),

        # Timeframe value
        dbc.Col(html.Div(
            dcc.Dropdown(
                id="timeframe-value-dropdown",
                options=[
                    {"label": "Day", "value": "day"},
                    {"label": "Week", "value": "week"},
                    {"label": "Month", "value": "month"},
                    {"label": "Year", "value": "year"},
                ],

            ),
        )),

        # Save dataset button
        dbc.Col(html.Div(
            dbc.Button(
                "Save Dataset",
                id="save-dataset-button",
                n_clicks=0
            )
        )),

    ]),

    dbc.Row([
        # Input value
        dbc.Col(html.Div(
            dbc.Input(
                id="value-input",
                placeholder="Value",
                type="text",
            ),
        )),

        # Input Date
        dbc.Col(html.Div(
            dcc.DatePickerSingle(
                id='date-input',
                min_date_allowed=dt(2019, 1, 1),
                max_date_allowed=dt.now(),
                date=str(dt.now().date()),
                display_format='DD/MM/YYYY',
                month_format='DD/MM/YYYY',
            ),
        )),
        # Input time box
        dbc.Col(html.Div(
            dbc.Input(
                id="time-input",
                value="%s:%s" % (dt.now().time().hour, dt.now().time().minute),
                type="time",
            ),
            "Input time box"
        )),

        # Input save button
        dbc.Col(html.Div(
            dbc.Button(
                "Save Data",
                id="input-save-button",
                n_clicks=0,
            ),
        )),

        # New row button
        dbc.Col(html.Div(
            dbc.Button(
                "New Row",
                id="new-row-button",
                n_clicks=0,
            ),
        )),

    ]),

    dbc.Row([
        # Graph
        dbc.Col(html.Div(
            dcc.Graph(
                id='graph',
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'scatter', 'name': 'Goal'},
                        {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'scatter', 'name': 'Data'},
                    ],
                },
            )
        )),

        # Table
        dbc.Col(html.Div(
            dash_table.DataTable(
                id='table',
                columns=[
                    {"name": "One", "id": "one"},
                    {"name": "Two", "id": "two"},
                ],
                data=[
                    {"one": 1, "two": 3},
                    {"one": 2, "two": 4},
                ],
            )
        )),

    ]),

    dbc.Row([
        dbc.Col(html.Div(
            html.P(
                "FirstDate"
            )
        )),

        # Date filter slider
        dbc.Col(html.Div(
            dcc.RangeSlider(
                id="date-filter-slider",
                min=0,
                max=24,
                value=[6, 18]
            )
        )),
        dbc.Col(html.Div(
            html.P(
                "LastDate"
            )
        )),

    ]),
], style={"width": "95vw"})


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
