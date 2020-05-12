import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_table
import pandas as pd
from datetime import datetime as dt
import time
import os
import numpy as np

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])

app.layout = html.Div([

    dbc.Row([
        # Dataset dropdown
        dbc.Col(html.Div(
            dcc.Dropdown(
                id="dataset-dropdown",
                options=[],
                value="",
                placeholder="Select Dataset",
                persisted_props=["value"],
                persistence_type="session",
                persistence=True
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
                id="date-input",
                min_date_allowed=dt(2019, 1, 1),
                max_date_allowed=dt.now().date(),
                display_format="DD/MM/YYYY",
                month_format="DD/MM/YYYY",
                placeholder="Date",
            ),
        )),
        # Input time box
        dbc.Col(html.Div(
            dbc.Input(
                id="time-input",
                type="time",
                placeholder="Time"
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
                    {"label": "Day", "value": "Day"},
                    {"label": "Week", "value": "Week"},
                    {"label": "Month", "value": "Month"},
                    {"label": "Year", "value": "Year"},
                ],
                placeholder="Timeframe"
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

    ]),

    dbc.Row([
        # Graph
        dbc.Col(html.Div(
            dcc.Graph(
                id="graph",
                figure={
                    "data": [
                        {"x": [], "y": [], "type": "scatter", "name": "Goal"},
                    ],
                },
                animate=False,
            )
        )),

        # Table
        dbc.Col(html.Div(
            dash_table.DataTable(
                id="table",
                columns=[],
                data=[],
                row_selectable="single",
                selected_rows=[0],
                page_size=12,
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
    html.Div(id="hidden-div-dropdown1", style={"display": "none"}),
    html.Div(id="hidden-div-dropdown2", style={"display": "none"}),
    html.Div(id="hidden-div-table", style={"display": "none"})
], style={"width": "95vw"})


# GLOBALS #

dropdown_input = ""


# FUNCTIONS #

# csv stuff
def load_data(dataset, sort=False):
    df = pd.read_csv("Data\\" + dataset + ".csv")

    if sort:
        # Sort data by date and time and keep empty lines on top
        df = df.sort_values(by=["date", "time"], ascending=[False, False])
        empties_mask = df["date"].isna()
        df = pd.concat([df[empties_mask], df[~empties_mask]])

    return df


def save_data(dataset, df):
    df.to_csv("Data\\" + dataset + ".csv", index=False)
    return True


def new_csv():
    if os.path.isfile("New Dataset.csv"):
        return False
    else:
        df = pd.DataFrame(columns=["value", "date", "time", "goal", "timeframe"])
        df = df.append(pd.Series(dtype="object"), ignore_index=True)
        save_data("New Dataset", df)
        return True


# CALLBACKS #


# Datasets #

# Dataset dropdown
@app.callback([Output("dataset-dropdown", "options"),
               Output("table", "selected_rows")],  # Done to start update chain
              [Input("dataset-dropdown", "value")])
def dataset_dropdown(value_chain):
    datasets = load_data("datasets")
    options = [[] for i in range(len(datasets))]
    for i in range(len(datasets)):
        dataset = datasets.iloc[i, 0]
        options[i] = {"label": dataset, "value": dataset}
    return options, [0]


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
        if oldname is not None:
            datasets = load_data("datasets")
            datasets[datasets["datasets"].str.match(oldname)] = newname
            save_data("datasets", datasets)
            global dropdown_input
            dropdown_input = newname
            os.rename("Data\\" + oldname+".csv", "Data\\" + newname+".csv")
            return ""
        else:
            return None
    else:
        return None


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
        else:
            return None
    else:
        return None


# Update dropdown
@app.callback(Output("dataset-dropdown", "value"),
              [Input("save-dataset-name-button", "n_clicks"),
               Input("new-dataset-button", "n_clicks")])
def update_dropdown(n_clicks_save, n_clicks_new):
    if n_clicks_save + n_clicks_new > 0:
        time.sleep(0.5)  # wait for global input to save
        global dropdown_input
        return dropdown_input
    else:
        return None


# Disable inputs
@app.callback([Output("value-input", "disabled"),
               Output("date-input", "disabled"),
               Output("time-input", "disabled"),
               Output("goal-value-input", "disabled"),
               Output("timeframe-value-dropdown", "disabled")],
              [Input("dataset-dropdown", "value")])
def disable_inputs(value):
    if value is None:
        return True, True, True, True, True
    else:
        return False, False, False, False, False


# Update table
@app.callback([Output("table", "columns"),
               Output("table", "data")],
              [Input("dataset-dropdown", "value"),
               Input("hidden-div-table", "children")])  # Done to allow update chain
def update_table(value, table_chain):
    if value is not None:
        data = load_data(value, sort=True)

        if not pd.isna(data["value"][0]):
            new_row = pd.DataFrame(columns=data.columns)
            new_row = new_row.append(pd.Series(dtype="object"), ignore_index=True)
            data = pd.concat([new_row, data]).reset_index(drop=True)
            save_data(value, data)

        columns = [{"name": i, "id": i} for i in data.columns]
        data = data.to_dict("records")
        return columns, data
    else:
        return [], []


# Edit table info
@app.callback([Output("value-input", "value"),
               Output("date-input", "date"),
               Output("time-input", "value"),
               Output("goal-value-input", "value"),
               Output("timeframe-value-dropdown", "value")],
              [Input("table", "selected_rows")],
              [State("dataset-dropdown", "value")])
def edit_table_info(selected_rows, dataset):
    if (dataset != "") & (dataset is not None) & (selected_rows is not None):
        data = load_data(dataset, sort=True)
        data = data.where(pd.notna(data), "")  # convert Nans to empty string to avoid persistence of values in inputs

        value = data.iloc[selected_rows, 0].iloc[0]  # iloc at the end of every statement so that it'll return strings
        date = data.iloc[selected_rows, 1].iloc[0]
        datatime = data.iloc[selected_rows, 2].iloc[0]
        goal = data.iloc[selected_rows, 3].iloc[0]
        timeframe = data.iloc[selected_rows, 4].iloc[0]

        # default date and time to now for new data
        if (date == "") | (datatime == ""):
            date = dt.now().date()
            datatime = dt.now().strftime("%H:%M")

        return value, date, datatime, goal, timeframe
    else:
        return None, None, None, None, None


# Save data
@app.callback(Output("hidden-div-table", "children"),
              [Input("input-save-button", "n_clicks")],
              [State("dataset-dropdown", "value"),
               State("table", "selected_rows"),
               State("value-input", "value"),
               State("date-input", "date"),
               State("time-input", "value"),
               State("goal-value-input", "value"),
               State("timeframe-value-dropdown", "value")])
def save_input(n_clicks, dataset, selected_rows, value, date, datatime, goal, timeframe):
    if n_clicks > 0:
        if (value != "") & (date is not None) & (datatime != ""):
            data = load_data(dataset, sort=True)
            data.iloc[selected_rows, 0] = value  # iloc at the end of every statement so that it'll return strings
            data.iloc[selected_rows, 1] = date
            data.iloc[selected_rows, 2] = datatime
            data.iloc[selected_rows, 3] = goal
            data.iloc[selected_rows, 4] = timeframe
            save_data(dataset, data)
            return ""
        else:
            return None
    else:
        return None


# Update graph
@app.callback(Output("graph", "figure"),
              [Input("dataset-dropdown", "value"),
               Input("input-save-button", "n_clicks")])  # Done to start update chain
def update_graph(dataset, n_clicks_chain):
    if dataset is not None:
        time.sleep(0.5)
        data = load_data(dataset, sort=True)
        data["datetime"] = pd.to_datetime(data["date"] + " " + data["time"])

        # Setting up goal data
        data["goal"] = data["goal"].fillna(method='bfill')
        data["timeframe"] = data["timeframe"].fillna(method='bfill')
        # This used to be here because I thought I needed to offset the datetime to the other direction, I don't :D
        # data["datetime_prev"] = pd.concat([pd.Series([None], dtype="object"), data["datetime"]]).reset_index(
        # drop=True)
        data["datetime_prev"] = data["datetime"].drop(0, axis=0).reset_index(drop=True)
        data["datetime_delta"] = data["datetime"] - data["datetime_prev"]
        data["day_delta"] = data["datetime_delta"]/np.timedelta64(1, "D")
        timeframe_conversion = dict(
            Day=1,
            Week=7,
            Month=30,
            Year=365,
        )
        data["timeframe_days"] = data["timeframe"].map(timeframe_conversion)
        data.loc[[len(data) - 1], ["day_delta"]] = 1
        data["goal_delta"] = data["goal"]/data["timeframe_days"]*data["day_delta"]
        data["goal_cumulative"] = data.loc[::-1, "goal_delta"].cumsum()[::-1]
        data["value_cumulative"] = data.loc[::-1, "value"].cumsum()[::-1]


        # defining axis
        x = data["datetime"]
        yvalue = data["value"]
        ycumulative = data["value_cumulative"]
        ygoal = data["goal_cumulative"]

    else:
        x = []
        yvalue = []
        ycumulative = []
        ygoal = []

    figure = {
        "data": [
            dict(
                x=x,
                y=yvalue,
                type="scatter",
                name="Instances",
            ),
            dict(
                x=x,
                y=ycumulative,
                type="scatter",
                name="Progress",
                line=dict(width=4),
                marker=dict(size=10)
            ),
            dict(
                x=x,
                y=ygoal,
                type="scatter",
                name="Goal",
            ),
        ]
    }
    return figure


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")
