# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html
from dash.dependencies import Input, Output

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Marché du travail pour les futurs employers en informatique'),
    dcc.Tabs(id="visualisations", value='T1', children=[
        dcc.Tab(label='Technologies à connaitre', value='T1'),
        dcc.Tab(label='Salaires et Postes', value='T2'),
        dcc.Tab(label='Santé mentale au travail', value='T3'),
    ]),
    html.Div(id='rootDiv')
])

@app.callback(Output('rootDiv', 'children'),
              Input('visualisations', 'value'))
def render_content(tab):
    if tab == 'T1':
        return view1.view
    elif tab == 'T2':
        return view2.view
    elif tab == 'T3':
        return view3.view

if __name__ == '__main__':
    app.run_server(debug=False)
