# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
from datetime import datetime as dt
import dash_table

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('juggling.csv')

app.layout = html.Div([
    dash_table.DataTable(
        id='datatable',
        #editable=True,
        row_selectable='single'
    ),
    html.Button('Save Changes', id='save-button', n_clicks=0),
    html.Div(id='div-out')
])


@app.callback(
    [Output('datatable', 'data'),
     Output('datatable', 'columns')],
    [Input('save-button', 'n_clicks')],
    [State('datatable', 'data'),
     State('datatable', 'columns')]
)
def save_changes(n_clicks, data, columns):
    global df
    if n_clicks > 0:
        df = pd.DataFrame(data)
        df.to_csv('juggling.csv', index=False)
    df = pd.read_csv('juggling.csv')
    newdata = df.to_dict('records')
    newcolumns = [{"name": i, "id": i} for i in df.columns]
    return newdata, newcolumns


@app.callback(
    Output('div-out','children'),
    [Input('datatable', 'selected_rows')])
def check_selected_rows(selected_rows):
    return selected_rows

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
