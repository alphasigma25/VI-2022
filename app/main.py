# Run this app with `python main.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
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
        dcc.Graph(id='techs-graphic')
    ]),
    html.Div([
        html.Div([
            dcc.Dropdown(
                data_util.DevType,
                data_util.DevType[0],
                id='devType_t',
                clearable=False
            )
        ]),
        html.Div([
            dcc.Dropdown(
                data_util.EdLevel,
                data_util.EdLevel[0],
                id='edLevel_t',
                clearable=False
            )
        ]),
        html.Div([
            dcc.Dropdown(
                data_util.Employment,
                data_util.Employment[0],
                id='employment_t',
                clearable=False
            )
        ]),
        html.Div([
            dcc.Dropdown(
                data_util.Age,
                data_util.Age[0],
                id='age_t',
                clearable=False
            )
        ]),
        html.Div([
            dcc.Dropdown(
                data_util.tech_selected_columns[6:],
                data_util.tech_selected_columns[6],
                id='outputName_t',
                clearable=False
            )
        ]),
    ], style={'display': 'flex', 'flex-direction': 'column', 'width': '40%'})
], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'center', 'align-items': 'center'})

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
                 hover_name="techs", text="techs", size='Number', size_max=10,
                 title=f"{devType}<br><sup>10 most used technologies</sup>", width=750, height=500)

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 40, 'r': 40}, hovermode='closest')
    fig.update_xaxes(title="Years of Experience", showspikes=True)
    fig.update_yaxes(title="Salary", showspikes=True)
    fig.update_traces(hovertemplate=None, textposition='top center')
    return fig

# --------------- salary_layout : Salaires et Postes --------------- #

salary_layout = html.Div([
    dcc.Graph(id="salary-graphic"),
    html.Div([
        html.Div([
            dcc.Dropdown(
                data_util.DevType,
                data_util.DevType[0],
                id='devType_s',
                clearable=False)
        ]),
        html.Div([
            dcc.Dropdown(
                data_util.EdLevel,
                data_util.EdLevel[0],
                id='edLevel_s',
                clearable=False)
        ]),
        html.Div([
            dcc.Dropdown(
                data_util.OrgSize,
                data_util.OrgSize[0],
                id='orgSize_s',
                clearable=False)
        ]),
        html.Div([
            dcc.Dropdown(
                data_util.countries,
                data_util.countries[0],
                id='country_s',
                clearable=False)
        ])
    ], style={'display': 'flex', 'flex-direction': 'column', 'width': '40%'})
], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'center', 'align-items': 'center'})


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
    round_scale = 20e3
    min_range = df_exp["YearlySalary"].min()
    min_range = int(np.floor(min_range / round_scale) * round_scale)
    max_range = df_exp["YearlySalary"].max()
    max_range = int(np.ceil(max_range / round_scale) * round_scale)
    # min_range = 80e4
    # max_range = 160e4

    fig = px.area(df_exp, y='YearlySalary', range_y=[min_range, max_range], line_shape='spline' ,title=f"{devType}<br><sup>Pay by experience</sup>", width=750, height=500)
    fig.update_traces(mode="lines", hovertemplate=None)
    fig.update_layout(hovermode="y",
        xaxis_title="Experience",
        yaxis_title="Yearly Salary [$]")

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
        dcc.Graph(id="mental-health-graphic")
    ], style={'width':'80%', 'display': 'inline-block'}),
    html.Div([
        html.Div([
            html.P('Sort by'),
            dcc.Dropdown(
                ['Anxiety','Depression'],
                'Depression',
                id='sort_type',
                clearable=False),
        ], style={'width': '20%', 'display': 'flex', 'flex-direction': 'column'}),
        html.Div([
            dcc.RangeSlider(
                data_util.MIN_SALARY,
                data_util.MAX_SALARY,
                value=[data_util.MIN_SALARY, data_util.MAX_SALARY],
                tooltip={"placement": "bottom", "always_visible": True},
                marks=None,
                id='salary')
        ], style={'width': '80%', 'display': 'inline-box'})
    ], style={'width': '80%', 'display': 'flex', 'flex-direction': 'row', 'justify-content': 'center'}),
], style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'align-items': 'center'})

df_health = pd.read_csv('mental_health.csv', index_col=0)

@app.callback(
    Output("mental-health-graphic", "figure"),
    [Input("salary", "value")],
    Input('sort_type', "value"))
def update_mental_health(salary, sort_type):
    df_d = data_util.getHealthOutput(df_health, salary[0], salary[1], 'Depression')
    df_a = data_util.getHealthOutput(df_health, salary[0], salary[1], 'Anxiety')
    if sort_type == "Depression":
        df_d = df_d.sort_values(by=['Depression'])
        df_a = df_a.reindex(df_d.index)
        df_d = df_d.reset_index(drop=True)
        df_a = df_a.reset_index(drop=True)
    else:
        df_a = df_a.sort_values(by=['Anxiety'])
        df_d = df_d.reindex(df_a.index)
        df_d = df_d.reset_index(drop=True)
        df_a = df_a.reset_index(drop=True)
    fig = make_subplots(rows=1, cols=2, subplot_titles=('Depression', 'Anxiety'))
    fig.append_trace(go.Bar(x=df_d["Depression"], y=df_d["DevType"], orientation='h'), row=1, col=1)
    fig.append_trace(go.Bar(x=df_a["Anxiety"], y=df_a["DevType"], orientation='h'), row=1, col=2)
    fig.update_xaxes(autorange='reversed', col=1)
    fig.update_yaxes(col=1, nticks=df_d.shape[0])
    fig.update_yaxes(col=2, showticklabels=False)
    fig.update_layout(polar = dict(radialaxis = dict(showticklabels = False)))
    fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=20, b=20))
    fig.update_layout(bargap=0.1)
    return fig


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
