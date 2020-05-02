# https://www.youtube.com/playlist?list=PLQVvvaa0QuDfsGImWNt1eUEveHOepkjqt
import dash
# from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1('Hello test'),
    dcc.Graph(id='example',
              figure ={
                  'data': [
                      {'x':[1,2,3,4,5], 'y':[5,6,7,2,11], 'type':'line', 'name':'boats'},
                      {'x':[1,2,3,4,5], 'y':[4,5.5,10,1,0], 'type':'bar', 'name':'cars'},
                  ],
                  'layout': {
                      'title':'Basic Dash Example'
                    }
              })
    ])

if __name__ == '__main__':
    app.run_server(debug=True)

