import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
from datetime import datetime as dt
import dash_table
import time
import os

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])

app.layout = html.Div([

    dbc.Row([
        # Dataset dropdown
        dbc.Col(html.Div(
            dcc.Dropdown(
                id="dataset-dropdown",
                options=[],
                value="",
            ),
        )),
        # Dataset Name
        dbc.Col(html.Div(
            dbc.Input(
                id="dataset-name-input",
                placeholder="Dataset Name",
                type="text",
            ),
        )),
        # Save dataset name button
        dbc.Col(html.Div(
            dbc.Button(
                "Save Dataset Name",
                id="save-dataset-name-button",
                n_clicks=0
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
        # Input value
        dbc.Col(html.Div(
            dbc.Input(
                id="value-input",
                placeholder="Value",
                type="number",
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
        # Goal value
        dbc.Col(html.Div(
            dbc.Input(
                id="goal-value-input",
                placeholder="Goal Value",
                type="number",
            ),
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
                row_selectable='single',
            ),
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
    html.Div(id='hidden-div-dropdown1', style={"display": "none"}),
    html.Div(id='hidden-div-dropdown2', style={"display": "none"}),
], style={"width": "95vw"})


# GLOBALS #

dropdown_input = ""


# FUNCTIONS #

# csv stuff
def load_data(dataset):
    df = pd.read_csv("Data\\" + dataset + ".csv")
    return df


def save_data(dataset, df):
    df.to_csv("Data\\" + dataset + ".csv", index=False)
    return True


def new_csv():
    if os.path.isfile("New Dataset.csv"):
        return False
    else:
        df = pd.DataFrame(columns=["value", "date", "time", "goal", "timeframe"])
        save_data("New Dataset", df)
        return True


# CALLBACKS #

# Dataset dropdown
@app.callback(Output("dataset-dropdown", "options"),
              [Input("dataset-dropdown", "value")])
def dataset_dropdown(value):
    datasets = load_data("datasets")
    options = [[] for i in range(len(datasets))]
    for i in range(len(datasets)):
        dataset = datasets.iloc[i, 0]
        options[i] = {"label": dataset, "value": dataset}
    return options


# Dataset name
@app.callback(Output("dataset-name-input", "value"),
              [Input("dataset-dropdown", "value")])
def dataset_name(value):
    return value


# Save dataset name
@app.callback(Output("hidden-div-dropdown1", "children"),
              [Input("save-dataset-name-button", "n_clicks")],
              [State("dataset-dropdown", "value"),
               State("dataset-name-input", "value")])
def save_dataset(n_clicks, oldname, newname):
    if n_clicks > 0:
        datasets = load_data("datasets")
        datasets[datasets["datasets"].str.match(oldname)] = newname
        save_data("datasets", datasets)
        global dropdown_input
        dropdown_input = newname
        os.rename("Data\\" + oldname+".csv", "Data\\" + newname+".csv")
        return ""


# Add new dataset
@app.callback(Output("hidden-div-dropdown2", "children"),
              [Input("new-dataset-button", "n_clicks")])
def new_dataset(n_clicks):
    if n_clicks > 0:
        if new_csv():
            datasets = load_data("datasets")
            newrow = ["New Dataset"]
            newrowdf = pd.DataFrame([newrow])
            newrowdf.columns = datasets.columns
            datasets = pd.concat([datasets, newrowdf], ignore_index=True)
            save_data("datasets", datasets)
            global dropdown_input
            dropdown_input = newrow[0]
            return ""


# Update dropdown
@app.callback(Output("dataset-dropdown", "value"),
              [Input("save-dataset-name-button", "n_clicks"),
               Input("new-dataset-button", "n_clicks")])
def update_dropdown(n_clicks_save, n_clicks_new):
    if n_clicks_save + n_clicks_new > 0:
        time.sleep(0.5)  # wait for global input to save
        global dropdown_input
        return dropdown_input


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
