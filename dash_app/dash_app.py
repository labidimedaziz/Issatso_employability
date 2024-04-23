from tokenize import group
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd 
import plotly.express as px 
import dash_bootstrap_components as dbc
#external_stylesheets = ['https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/cyborg/bootstrap.min.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])
df = pd.read_csv('data_frame.csv')
df_map = pd.read_csv('bubble_map.csv')
mark_values = {
    2001 : '2001',
    2002 : '2002',
    2003 : '2003',
    2004 : '2004',
    2005 : '2005',
    2006 : '2006',
    2007 : '2007',
    2008 : '2008',
    2009 : '2009',
    2010 : '2010',
    2011 : '2011',
    2012 : '2012',
    2013 : '2013',
    2014 : '2014',
    2015 : '2015',
    2016 : '2016',
    2017 : '2017',
    2018 : '2018',
    2019 : '2019'
}

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([html.H2('Issat Sousse Employabilité', className='text-center mb-4')])

    ]),
    dbc.Row([
        dbc.Col([
                html.H5('Les Sections :',className=' mb-2' ),
                dcc.Checklist(
                    options=[
                    {'label': 'Ing INF', 'value': 'Ing INF'},
                    {'label': 'LA-EEA-LMD', 'value': 'LA-EEA-LMD'},
                    {'label': 'LA-EM-LMD', 'value': 'LA-EM-LMD'},
                    {'label': 'LA-Energ-LMD', 'value': 'LA-Energ-LMD'},
                    {'label': 'LA-GC-LMD', 'value': 'LA-GC-LMD'},
                    {'label': 'LA-GM-LMD', 'value': 'LA-GM-LMD'},
                    {'label': 'LA-Inf-II-LMD', 'value': 'LA-Inf-II-LMD'},
                    {'label': 'LF-SI-LMD', 'value': 'LF-SI-LMD'},
                    {'label': 'MP-ENG', 'value': 'MP-ENG'},
                    {'label': 'MP-GM', 'value': 'MP-GM'},
                    {'label': 'MR-INF', 'value': 'MR-INF'},
                    {'label': 'MR-MSEE', 'value': 'MR-MSEE'}
                    ],
                    value=['Ing INF'],
                    id='checkbox',
                    className='mb-4'
                                ),
                    html.H5('Les Années Universitaires :',className=' mb-2' ),
                    dcc.RangeSlider(id='year_slider',
                    min = df['year'].min(),
                    max = df['year'].max(),
                    value=[2010,2015],
                    marks=mark_values,
                    step=None
                                    )])

        ]),
     dbc.Row([
        dbc.Col([
                    dcc.Graph(id='pie',className=' mb-2')

                ]),
        dbc.Col([
                    dcc.Graph(id='bar',className=' mb-2')

                ])
        
            ]),
        dbc.Row([
        dbc.Col([
                dcc.Graph(id='map',className=' mb-2')


        ])])

    

 
])
@app.callback(
 [Output(component_id='pie', component_property='figure'),
 Output(component_id='bar', component_property='figure'),
 Output(component_id='map', component_property='figure')
 ],
 [Input(component_id='checkbox', component_property='value'),
 Input(component_id='year_slider', component_property='value')])
def update_output_div(checkbox_value,slider_value):
    dff = df[df['diplm_IntituleCourt'].isin(checkbox_value) & (df['year']>=slider_value[0]) & (df['year']<=slider_value[1])]
    
    pie = px.pie(
        data_frame=dff,
        names=dff['job_status'],
        color_discrete_sequence=["black", "darkgray"],
        title="Graphe 1 : Pourcentage d'employabilité" ,
    
     )
    pie.update_traces(textposition='outside', textinfo='percent+label',
                        marker=dict(line=dict(color='#000000', width=4)),
                         pull=[0, 0, 0.2, 0], opacity=0.7, rotation=180)
    bar_chart = px.bar(
                data_frame=dff,
                x='job_title_graph',
                y='1',
                barmode="group",
                color_discrete_sequence=["Silver"],
                title='Graphe 2 : Titres'
    )
    bar_chart.update_traces(textposition='outside',
                        marker=dict(line=dict(color='#000000', width=4)),
                         opacity=0.7)
    map_chart = px.scatter_geo(df_map, locations="iso_alpha",
    size="count",
                     hover_name="Country",
                     projection="natural earth",
                     color="continent",
                     
                     title="Graphe 3 : Distribution des diplomés de l'issat dans le monde"
                     )

    return (pie ,bar_chart,map_chart)

if __name__ == '__main__':
 app.run_server(debug=True)