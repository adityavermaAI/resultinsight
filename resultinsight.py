import pandas as pd
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Input, Output

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG], meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1, maximum-scale=1"}])
server = app.server

app.index_string = '''<!DOCTYPE html>
<html>
<head>
  <!-- Global site tag (gtag.js) - Google Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-SQV8P1GH6E"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-SQV8P1GH6E');
  </script>
  <!-- End Global Google Analytics -->
{%metas%}
<title>{%title%}</title>
{%favicon%}
{%css%}
</head>
<body>
{%app_entry%}
<footer>
{%config%}
{%scripts%}
{%renderer%}
</footer>
</body>
</html>
'''

students_df = pd.read_csv("el_cs_ee_21_students.csv")
subjects_df = pd.read_csv("el_cs_ee_21_subjects_unique.csv")
marks_df = pd.read_csv("el_cs_ee_21_marks.csv")

    
stu_marks_df = pd.merge(students_df, marks_df, on="roll_no", how="inner").drop(["name", "gender"], axis=1)

def get_branch(roll_no):

    el_branch_code = "30"
    cs_branch_code = "10"
    ee_branch_code = "20"
    civil_branch_code = "00"
    
    if len(roll_no) ==10:
        
        if roll_no[5:7] == el_branch_code:
            return("ELECTRONICS ENGINEERING")

        elif roll_no[5:7] == cs_branch_code:
            return("COMPUTER SCIENCE AND ENGINEERING")
            
        elif roll_no[5:7] == ee_branch_code:
            return("ELECTRICAL ENGINEERING")
            
        elif roll_no[5:7] == civil_branch_code:
            return("CIVIL ENGINEERING")
            
    elif len(roll_no) == 13:
        
        if roll_no[7:9] == el_branch_code:
            return("Electronics Branch")

        elif roll_no[7:9] == cs_branch_code:
            return("Computer Science Branch")
            
        elif roll_no[7:9] == ee_branch_code:
            return("Electrical Branch")
            
        elif roll_no[7:9] == civil_branch_code:
            return("civil Branch")

roll_nos = list(students_df["roll_no"])
names = list(students_df["name"])

sems = subjects_df["sem"].unique()

app.layout = dbc.Container([
    
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Select Roll Number"),
                    dcc.Dropdown(
                    id='roll_no-dropdown',
                    options=[
                        {'label': f'{i}  {j}', 'value': f'{i}'} for i,j in zip(roll_nos, names)
                    ],
                    value=f'{roll_nos[5]}'
                    )
                ])
                
            ]),

            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='graph',
                                # animate=True,
                                config={'displayModeBar': False}
                    )
                ],
                style={'margin-top':"10px"},
                xs=12,
                sm=12,
                md=12,
                lg=8,
                xl=8
                ),

                dbc.Col([
                    html.Div(id="total-marks")
                ],
                style={'margin-top':"10px"},
                xs=12,
                sm=12,
                md=12,
                lg=4,
                xl=4
                )
                
            ],
            # no_gutters=True
            )                      
        ],
        style={'margin-top':"10px"},
        xs=12,
        sm=12,
        md=12,
        lg=6,
        xl=6
        ),

        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Select Semester"),
                    dcc.Dropdown(
                        id='sem-dropdown',
                        options=[
                            {'label': f'{i}', 'value': f'{i}'} for i in sems
                        ],
                        value=f'{sems[-1]}'
                    )
                ])
                
            ]),

            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='all-polar',
                                # animate=True, #not uodating without interaction
                                config={'displayModeBar': False}
                    )
                ],
                style={'margin-top':"10px"},
                xs=12,
                sm=12,
                md=12,
                lg=8,
                xl=8
                ),
                
                dbc.Col([
                    html.Div(id="sem-card")
                ],
                style={'margin-top':"10px"},
                xs=12,
                sm=12,
                md=12,
                lg=4,
                xl=4
                )
                
            ],
            # no_gutters=True
            )
 
        ],
        style={'margin-top':"10px"},
        xs=12,
        sm=12,
        md=12,
        lg=6,
        xl=6
        )

    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='total-bar',
                        # animate=True,
                        config={'displayModeBar': False}
            )
        ],
        xs=12,
        sm=12,
        md=12,
        lg=4,
        xl=4),

        dbc.Col([
            dcc.Graph(id='external-bar',
                        # animate=True,
                        config={'displayModeBar': False}
            )
        ],
        xs=12,
        sm=12,
        md=12,
        lg=4,
        xl=4),

        dbc.Col([
            dcc.Graph(id='internal-bar',
                        # animate=True,
                        config={'displayModeBar': False}
            )
        ],
        xs=12,
        sm=12,
        md=12,
        lg=4,
        xl=4)

    ],
    style={'margin-top':"10px"} 
    # no_gutters=True
    )
]
)



@app.callback(
    [Output("total-marks", "children"),
    Output("sem-card", "children"),
    Output('graph', 'figure'),
    Output('all-polar', 'figure'),
    Output('total-bar', 'figure'),
    Output("external-bar", "figure"),
    Output("internal-bar", "figure")],
    [Input('roll_no-dropdown', 'value'),
    Input('sem-dropdown', 'value')])

def card(roll_no, sem):
    global stu_marks_df

    branch = get_branch(f"{roll_no}")

    marks_df=stu_marks_df.loc[stu_marks_df["branch"] == branch]

    filtered_marks_df=marks_df.loc[marks_df["roll_no"] == int(roll_no)]
    sub_fil_roll_marks_df=pd.merge(filtered_marks_df, subjects_df, on="sub_code", how="left")

    total_marks=sub_fil_roll_marks_df["total_marks"].sum()

    #Total Marks Card

    marks_df_gp_roll = marks_df.groupby("roll_no")

    roll_wise_sum_total_marks_dict = {}

    for g, df in marks_df_gp_roll:
        roll_wise_sum_total_marks_dict.update({g:df['total_marks'].sum()})
        

    total_class_avg = round(sum(roll_wise_sum_total_marks_dict.values()) / len(roll_wise_sum_total_marks_dict))

    roll_wise_sum_total_marks_dict_sorted = dict(sorted(roll_wise_sum_total_marks_dict.items(), key=lambda item: item[1], reverse=True))

    total_class_rank = list(roll_wise_sum_total_marks_dict_sorted.keys()).index(int(roll_no)) + 1

    total_marks_card = dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Center([
                                        html.H5(f"{total_marks}", className="card-title"),
                                        html.P("Total Marks"),
                                        html.H5(f"{total_class_avg}", className="card-title"),
                                        html.P("class Average Marks"),
                                        html.H5(f"{total_class_rank}", className="card-title"),
                                        html.P("Overall Rank")
                                    ])
                                    
                                ]
                            )
                        )

#############################################################################################################################################
    
    #Graphs

    sub_marks_df = pd.merge(marks_df, subjects_df, on="sub_code", how="left")

    sub_marks_df_gp_sem = sub_marks_df.groupby("sem")

    sem_wise_class_average_total_marks = []
    sems_all=[]

    for g, df in sub_marks_df_gp_sem:
       sem_wise_class_average_total_marks.append(round((df["total_marks"].sum())/df.roll_no.nunique()))
       sems_all.append(g)

    sub_fil_roll_marks_df_sem=sub_fil_roll_marks_df.groupby("sem")
    sems=[]
    sem_wise_sum_total_marks=[]

    for g, df in sub_fil_roll_marks_df_sem:
        sems.append(g)
        sem_wise_sum_total_marks.append(df["total_marks"].sum())

    #All Semesters Graph
    
    fig=go.Figure(
        data=[go.Scatter(x=sems, y=sem_wise_sum_total_marks, name="Your Marks", mode="lines"),
            go.Scatter(x=sems_all, y=sem_wise_class_average_total_marks, name="Class Average", mode="lines", line=dict(color='rgb(255, 255, 0)')),
             ]
    )

    fig.update_layout(legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1,
                                xanchor="right",
                                x=1,
                                font={"size":13}
                                ),
                                height=300,
                                dragmode=False,
                                paper_bgcolor="rgb(0,0,0)",
                                plot_bgcolor="rgb(0,0,0)",
                                margin_l=0, margin_t=0, margin_r=0, margin_b=0,
                                template="plotly_dark"
    )

    fig.update_xaxes(showgrid=False, color='white', title="Semesters", title_font=dict(color='white'))
    fig.update_yaxes(showgrid=False, color='white')

#############################################################################################################################################

    #Semester Marks Card

    sub_fil_roll_marks_fil_sem_df=(sub_fil_roll_marks_df.loc[sub_fil_roll_marks_df["sem"] == int(sem)]).drop(["sem", "roll_no"], axis=1)

    sub_marks_df_fil_sem = sub_marks_df.loc[sub_marks_df["sem"] == int(sem)]

    sub_marks_df_fil_sem_gp_roll = sub_marks_df_fil_sem.groupby("roll_no")

    roll_wise_sem_fil_sum_total_marks_dict = {}

    for g, df in sub_marks_df_fil_sem_gp_roll:
        roll_wise_sem_fil_sum_total_marks_dict.update({g:df['total_marks'].sum()})
        

    sem_avg = round(sum(roll_wise_sem_fil_sum_total_marks_dict.values()) / len(roll_wise_sem_fil_sum_total_marks_dict))

    roll_wise_sem_fil_sum_total_marks_dict_sorted = dict(sorted(roll_wise_sem_fil_sum_total_marks_dict.items(), key=lambda item: item[1], reverse=True))

    sem_rank = list(roll_wise_sem_fil_sum_total_marks_dict_sorted.keys()).index(int(roll_no)) + 1

    sem_card= dbc.Card(
                        dbc.CardBody(
                            [
                                html.Center([
                                    html.H5(f"{sub_fil_roll_marks_fil_sem_df['total_marks'].sum()}", className="card-title"),
                                    html.P("Semester Marks"),
                                    html.H5(f"{sem_avg}", className="card-title"),
                                    html.P("Class Average Marks"),
                                    html.H5(f"{sem_rank}", className="card-title"),
                                    html.P("Semester Rank")
                                ])
                                
                            ]
                        )
                    )
    
###########################################################################################################################

    total_marks = sub_fil_roll_marks_fil_sem_df["total_marks"].tolist()
    external_marks = sub_fil_roll_marks_fil_sem_df["external_marks"].tolist()
    internal_marks = sub_fil_roll_marks_fil_sem_df["internal_marks"].tolist()

    categories = sub_fil_roll_marks_fil_sem_df["sub_code"].tolist()
    subject_names = sub_fil_roll_marks_fil_sem_df["sub_name"].tolist()

    polar = go.Figure([go.Scatterpolar(
                        r=total_marks,
                        theta=categories,
                        mode = 'lines',
                        fill='toself',
                        name='Total'
                        ),
                        go.Scatterpolar(
                        r=external_marks,
                        theta=categories,
                        mode = 'lines',
                        fill='toself',
                        name='External'
                        ),
                        go.Scatterpolar(
                        r=internal_marks,
                        theta=categories,
                        mode = 'lines',
                        fill='toself',
                        name='Internal'
                        )
                ])

    polar.update_layout(
                            legend=dict(
                            # orientation="h",
                            yanchor="top",
                            y=1.23,
                            xanchor="right",
                            x=1.1
                            ),
                            height=300,
                            dragmode=False,
                            paper_bgcolor="rgb(0,0,0)",
                            template="plotly_dark",
                            margin_l=20, margin_t=50, margin_r=20, margin_b=10
    )

    polar.update_polars(bgcolor="rgb(0,0,0)",
                        radialaxis = dict(
                                        visible = False,
                                        range = [0, 100]
                                    ),
                        angularaxis_rotation=90,
                        angularaxis_showline=False
                    )
###########################################################################################################################

    #Total Marks Bar Graph

    total_graph = go.Figure([go.Bar(x=categories,
                                y=sub_fil_roll_marks_fil_sem_df["total_marks"].tolist(),
                                text=sub_fil_roll_marks_fil_sem_df["total_marks"].tolist(),
                                textposition='auto',
                                hovertext=subject_names)])

    total_graph.update_layout(
                                title={
                                    'text': "Total Marks",
                                    'y':0.9,

                                    'x':0.5,
                                    'xanchor': 'center',
                                    'yanchor': 'top'
                                    },
                                legend=dict(
                                    orientation="h",
                                    yanchor="bottom",
                                    y=1,
                                    xanchor="right",
                                    x=1
                                    ),
                                height=300,
                                dragmode=False,
                                paper_bgcolor="rgb(0,0,0)",
                                plot_bgcolor="rgb(0,0,0)",
                                margin_l=0, margin_t=60, margin_r=0, margin_b=0
    )

    total_graph.update_traces(marker_color='rgb(255,0,0)', marker_line_color='rgb(255,0,0)',marker_line_width=1.5, opacity=0.5)
    total_graph.update_xaxes(showgrid=False, linecolor='black')
    total_graph.update_yaxes(showgrid=False)


    #External Marks Bar Graph

    external_graph = go.Figure([go.Bar(x=categories,
                                    y=external_marks,
                                    text=external_marks,
                                    textposition='auto',
                                    hovertext=subject_names)])

    external_graph.update_layout(
                                title={
                                    'text': "External Marks",
                                    'y':0.9,
                                    'x':0.5,
                                    'xanchor': 'center',
                                    'yanchor': 'top'
                                    },
                                legend=dict(
                                    orientation="h",
                                    yanchor="bottom",
                                    y=1,
                                    xanchor="right",
                                    x=1
                                    ),
                                height=300,
                                dragmode=False,
                                paper_bgcolor="rgb(0,0,0)",
                                plot_bgcolor="rgb(0,0,0)",
                                margin_l=0, margin_t=60, margin_r=0, margin_b=0
    )

    external_graph.update_traces(marker_color='rgb(255,0,0)', marker_line_color='rgb(255,0,0)',marker_line_width=1.5, opacity=0.5)
    external_graph.update_xaxes(showgrid=False, linecolor='black')
    external_graph.update_yaxes(showgrid=False)


    #Internal Marks Bar Graph

    internal_graph = go.Figure([go.Bar(x=categories,
                                    y=internal_marks,
                                    text=internal_marks,
                                    textposition='auto',
                                    hovertext=subject_names)])

    internal_graph.update_layout(
                                title={
                                    'text': "Internal Marks",
                                    'y':0.9,
                                    'x':0.5,
                                    'xanchor': 'center',
                                    'yanchor': 'top'
                                    },
                                legend=dict(
                                    orientation="h",
                                    yanchor="bottom",
                                    y=1,
                                    xanchor="right",
                                    x=1
                                    ),
                                height=300,
                                dragmode=False,
                                paper_bgcolor="rgb(0,0,0)",
                                plot_bgcolor="rgb(0,0,0)",
                                margin_l=0, margin_t=60, margin_r=0, margin_b=0
    )

    internal_graph.update_traces(marker_color='rgb(255,0,0)', marker_line_color='rgb(255,0,0)',marker_line_width=1.5, opacity=0.5)
    internal_graph.update_xaxes(showgrid=False, linecolor='black')
    internal_graph.update_yaxes(showgrid=False)

    return total_marks_card, sem_card, fig, polar, total_graph, external_graph, internal_graph

if __name__ == '__main__':
    app.run_server()