# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
from datetime import datetime as dt

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(id='input-1-state', type='text', value=''),
    dcc.DatePickerSingle(
        id='input-2-date-state',
        min_date_allowed=dt(2019, 1, 1),
        max_date_allowed=dt.now(),
        date=str(dt.now().date()),
        display_format='DD/MM/YYYY',
        month_format='DD/MM/YYYY'),
    dcc.Input(
        id='input-3-time-state',
        type='number',
        value=dt.now().strftime("%H%M"),
        min=00, max=2359, maxLength=4,
        style={'width': 80}
    ),
    html.Button(id='submit-button-input', n_clicks=0, children='Submit'),
    html.Div(id='output-state')
])


@app.callback(Output('output-state', 'children'),
              [Input('submit-button-input', 'n_clicks')],
              [State('input-1-state', 'value'),
               State('input-2-date-state', 'date'),
               State('input-3-time-state', 'value')])
def update_output(n_clicks, input1, input2date, input3time):
    if not ((input1 == "") | (input2date is None) | (input3time is None)):
        df = pd.read_csv('juggling.csv')
        newrow = [input1, input2date, input3time]
        newrowdf = pd.DataFrame([newrow])
        newrowdf.columns = df.columns
        df = pd.concat([df, newrowdf], ignore_index=True)
        df.to_csv('juggling.csv', index=False)
        return (html.P('Saved:'),
                html.P('{} minutes done at {}, {}'.format(input1, input3time, input2date)))





if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
