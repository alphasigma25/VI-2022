# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Marché du travail pour les futurs employés dans le secteur de l\'informatique'),
    dcc.Tabs(id="visualisations", value='T1', children=[
        dcc.Tab(label='Technologies à connaitre', value='T1'),
        dcc.Tab(label='Salaires et Postes', value='T2'),
        dcc.Tab(label='Santé mentale au travail', value='T3'),
    ]),
    html.Div(id='rootDiv')
])

# --------------- view2 : Salaires et Postes --------------- #
@app.callback(
    Output("graph", "figure"),
    Input("y-axis", "value"))
def display_area(y):
    df = pd.read_csv('salary_by_category.csv', index_col=0)
    # Display the histogram for the Data Scientists
    df['DevType'] = df['DevType'].fillna("")
    df_ds = df[df['DevType'].str.contains("Data scientist")]
    df_ds

    # Filter the salary to remove the outliers
    df_ds = df_ds.loc[df_ds['YearlySalary'] > df_ds.YearlySalary.quantile(0.1)]
    df_ds = df_ds.loc[df_ds['YearlySalary'] < df_ds.YearlySalary.quantile(0.9)]

    df_ds = df_ds.sort_values(by=['YearsCodePro'])
    df_exp = pd.DataFrame()
    df_exp["YearlySalary"] = [df_ds.loc[df_ds["YearsCodePro"] == 0]["YearlySalary"].mean(),
                            df_ds.loc[df_ds["YearsCodePro"].between(1, 4, inclusive="both")]["YearlySalary"].mean(),
                            df_ds.loc[df_ds["YearsCodePro"].between(5, 9, inclusive="both")]["YearlySalary"].mean(),
                            df_ds.loc[df_ds["YearsCodePro"].between(10, 19, inclusive="both")]["YearlySalary"].mean(),
                            df_ds.loc[df_ds["YearsCodePro"] >= 20]["YearlySalary"].mean()]

    df_exp.index = np.arange(0, 21, 5)
    df_exp["YearlySalary"] = df_exp["YearlySalary"].round(-3)

    fig = px.area(df_exp, y='YearlySalary', range_y=[80e3,160e3], line_shape='spline' ,title="Data Scientist<br><sup>Pay by experience</sup>", width=750, height=500)
    fig.update_traces(mode="lines", hovertemplate=None)
    fig.update_layout(hovermode="y",
        xaxis_title="Experience",
        yaxis_title="Yearly Salary [$]",)

    fig.update_layout(
        xaxis = dict(
            tickmode = 'array',
            tickvals = [0, 5, 10, 15, 20],
            ticktext = ['< 1 yr', '1-4 yr', '5-9 yr', '10-19 yr', '20+ yr',]
        )
    )
    return fig

view2 = html.Div([
            dcc.Dropdown(
                id='y-axis',
                options=['lifeExp', 'pop', 'gdpPercap'],
                value='gdpPercap'),
            dcc.Graph(id="graph")
        ])

@app.callback(Output('rootDiv', 'children'),
              Input('visualisations', 'value'))
def render_content(tab):
    if tab == 'T1':
        return view1.view
    elif tab == 'T2':
        return view2
    elif tab == 'T3':
        return view3.view

if __name__ == '__main__':
    app.run_server(debug=False)
