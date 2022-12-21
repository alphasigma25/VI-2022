# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import data_util

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


# ------------- tech_layout : Technologies plus utilisées ---------- #

techs_layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                data_util.DevType,
                data_util.DevType[0],
                id='devType_t',
                clearable=False
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                data_util.EdLevel,
                data_util.EdLevel[0],
                id='edLevel_t',
                clearable=False
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                data_util.Employment,
                data_util.Employment[0],
                id='employment_t',
                clearable=False
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                data_util.Age,
                data_util.Age[0],
                id='age_t',
                clearable=False
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                data_util.tech_selected_columns[6:],
                data_util.tech_selected_columns[6],
                id='outputName_t',
                clearable=False
            )
        ], style={'width': '48%', 'display': 'inline-block'}),
    ]),

    dcc.Graph(id='techs-graphic')
])

df_techs = pd.read_csv('tech_data.csv')

@app.callback(
    Output('techs-graphic', 'figure'),
    Input('devType_t', 'value'),
    Input('edLevel_t', 'value'),
    Input('employment_t', 'value'),
    Input('age_t', 'value'),
    Input('outputName_t', 'value'))
def update_techs(devType, edLevel, employment, age, outputName):
    data = data_util.getTechOutput(df_techs, devType, edLevel, employment, age, outputName)
    data.dropna()

    fig = px.scatter(data, x="YearsCodePro", y="CompTotal",
                 hover_name="techs", text="techs", size='Number', size_max=10)

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    fig.update_xaxes(title="Years of Experience")
    fig.update_yaxes(title="Salary")
    fig.update_traces(textposition='top center')
    return fig

# --------------- salary_layout : Salaires et Postes --------------- #

salary_layout = html.Div([
    html.Div([
        html.Div([
        dcc.Dropdown(
            data_util.DevType,
            data_util.DevType[0],
            id='devType_s',
            clearable=False
        )
    ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                data_util.EdLevel,
                data_util.EdLevel[0],
                id='edLevel_s',
                clearable=False
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                data_util.OrgSize,
                data_util.OrgSize[0],
                id='orgSize_s',
                clearable=False
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                data_util.countries,
                data_util.countries[0],
                id='country_s',
                clearable=False
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        dcc.Graph(id="salary-graphic")
    ])
])


df_salary = pd.read_csv('salary_by_category.csv', index_col=0)

@app.callback(
    Output("salary-graphic", "figure"),
    Input("devType_s", "value"),
    Input("edLevel_s", "value"),
    Input("orgSize_s", "value"),
    Input("country_s", "value"))
def display_area(devType, edLevel, orgSize, country):
    df_exp = data_util.getAreaOutput(df_salary, devType, edLevel, orgSize, country)

    # Compute the range of the data, then floor/ceil it to the nearest 20e4 number
    # round_scale = 20e4
    # min_range = df_exp["YearlySalary"].min()
    # min_range = int(np.floor(min_range / round_scale) * round_scale)
    # max_range = df_exp["YearlySalary"].max()
    # max_range = int(np.ceil(min_range / round_scale) * round_scale)
    min_range = 80e4
    max_range = 160e4

    fig = px.area(df_exp, y='YearlySalary', range_y=[min_range, max_range], line_shape='spline' ,title=f"{devType}<br><sup>Pay by experience</sup>", width=750, height=500)
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

# ------------------------ Mental Health --------------------------- #

health_layout = html.Div([
    html.Div([
        dcc.Graph(id="mood-graphic"),
        dcc.Graph(id="anxiety-graphic")
    ], style={'width': '48%', 'display': 'inline-block'}),
    html.Div([
        dcc.RangeSlider(
            data_util.MIN_SALARY,
            data_util.MAX_SALARY,
            value=[data_util.MIN_SALARY, data_util.MAX_SALARY],
            marks=None,
            id='salary'
        )
    ], style={'width': '48%', 'display': 'inline-block'}),
])

df_health = pd.read_csv('mental_health.csv', index_col=0)

def update_mental_health(df, mental_health_type):
    fig = px.bar(df, x='DevType', y=mental_health_type, orientation='h')
    fig.update_layout(hovermode="y",
        xaxis_title="Dev Type",
        yaxis_title=f"% people with {mental_health_type} disorder")
    return fig

@app.callback(
    Output("mood-graphic", "figure"),
    [Input("salary", "value")])
def update_mood(salary):
    df = data_util.getHealthOutput(df_health, salary[0],salary[1], 'Depression')
    return update_mental_health(df, 'Depression')

@app.callback(
    Output("anxiety-graphic", "figure"),
    [Input("salary", "value")])
def update_anxiety(salary):
    df = data_util.getHealthOutput(df_health, salary[0],salary[1], 'Anxiety')
    return update_mental_health(df, 'Anxiety')


# ----------------------------- main ------------------------------- #

@app.callback(Output('rootDiv', 'children'),
              Input('visualisations', 'value'))
def render_content(tab):
    if tab == 'T1':
        return techs_layout
    elif tab == 'T2':
        return salary_layout
    elif tab == 'T3':
        return health_layout

if __name__ == '__main__':
    app.run_server(debug=True)
