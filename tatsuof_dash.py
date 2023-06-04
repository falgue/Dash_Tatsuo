from tatsuof import *
import dash
import base64
from dash import dcc
import Scripts.utils.dash_reusable_components as drc
import dash_bootstrap_components as dbc
from dash import html
import plotly.graph_objects as go
import numpy as np
from dash.dependencies import Input, Output
es=['C:/Users/usuario/AppData/Local/Programs/Python/Python310/Scripts/assets/assets.custom-styles.css']
app=dash.Dash(__name__,external_stylesheets=[dbc.themes.SPACELAB, dbc.icons.FONT_AWESOME],)
dia_png = 'dia.png'
dia_base64 = base64.b64encode(open(dia_png, 'rb').read()).decode('ascii')
app.layout=dbc.Container([
    dbc.Row([
        dbc.Col(
            [html.H1('Microstrip Finite Element Method', style={'textAlign': 'center'})],align="center",width=6
            ),
        dbc.Col([
            html.Img(src='data:image/png;base64,{}'.format(dia_base64),height="center",style={'height':'82%', 'width':'82%'})
        ],width=6)
    ]),
    dbc.Row([
        dbc.Col([dcc.Loading(id="ff",
            className="graph-wrapper",
            children=dcc.Graph(id="Zs",figure={})
            )],width=6),
        dbc.Col([dcc.Loading(id="fa",
            className="graph-wrapper",
            children=dcc.Graph(id="vp",figure={})
            )],width=6)]),
    dbc.Row([
        dbc.Col(html.H6('NYA'),width=2),
        dbc.Col(html.H6('NYB'),width=2),
        dbc.Col(html.H6('NY'),width=2),
        dbc.Col(html.H6('NX'),width=2),
        dbc.Col(html.H6('NS'),width=2),
    ]),
    dbc.Row([
        dbc.Col([dbc.Input(id="NYA",type="number",value=4,min=4,max=35,step=1)],width=2),
        dbc.Col([dbc.Input(id="NYB",type="number",value=6,min=6,max=35,step=1)],width=2),
        dbc.Col([dbc.Input(id="NY",type="number",value=8,min=8,max=35,step=1)],width=2),
        dbc.Col([dbc.Input(id="NX",type="number",value=9,min=9,max=35,step=1)],width=2),
        dbc.Col([dbc.Input(id="NS",type="number",value=3,min=3,max=35,step=1)],width=2)
        ]),
    dbc.Row([
        dbc.Col([drc.NamedSlider(id="SP_1",name="er1",min=1,max=15,value=1,step=0.5,marks={
            str(i):str(i) for i in range(2,14,3)})],width=2),

        dbc.Col([drc.NamedSlider(id="SP_2",name="er2",min=1,max=15,value=1,step=0.5,marks={
            str(i):str(i) for i in range(2,14,3)})],width=2),

        dbc.Col([drc.NamedSlider(id="SP_3",name="er3",min=1,max=15,value=1,step=0.5,marks={
            str(i):str(i) for i in range(2,14,3)})],width=2),

        dbc.Col([drc.NamedSlider(id="SP_4",name="Y1",min=4,max=35,value=1,step=1,marks={
            str(i):str(i) for i in range(4,34,3)})],width=2),

        dbc.Col([drc.NamedSlider(id="SP_5",name="Y2",min=6,max=35,value=1,step=1,marks={
            str(i):str(i) for i in range(6,34,4)})],width=2),

        dbc.Col([drc.NamedSlider(id="SP_6",name="Y3",min=8,max=35,value=1,step=1,marks={
            str(i):str(i) for i in range(8,34,5)})],width=2)
        ])],fluid=True)

            
@app.callback(
    Output(component_id='Zs', component_property='figure'),
    Output(component_id='vp', component_property='figure'),
    Input(component_id='SP_4', component_property='value'),
    Input(component_id='SP_5', component_property='value'),
    Input(component_id='SP_6', component_property='value'),
    Input(component_id='SP_1', component_property='value'),
    Input(component_id='SP_2', component_property='value'),
    Input(component_id='SP_3', component_property='value'),
    Input(component_id='NYA', component_property='value'),
    Input(component_id='NYB', component_property='value'),
    Input(component_id='NY', component_property='value'),
    Input(component_id='NX', component_property='value'),
    Input(component_id='NS', component_property='value')
)
def update(YL1,YL2,YL3,EP1,EP2,EP3,NYA,NYB,NY,NX,NS):
    XZ0=np.arange(1,31)/(YL2+YL3)
    YZ0=np.zeros(29)
    YZ1=np.zeros(29)
    vp1=np.zeros(29)
    for i in range(1,30):
        C0,C1,Z0,Z1,vp=tatsuo(YL1,YL2,YL3,EP1,EP2,EP3,30,i,NYA,NYB,NY,NX,NS)
        YZ0[i-1]=Z0
        YZ1[i-1]=Z1
        vp1[i-1]=vp
    fig1 = go.Figure()
    fig2 = go.Figure()
    fig1.add_trace(go.Scatter(x=XZ0,y=YZ0,mode='lines',name='Z0'))
    fig1.add_trace(go.Scatter(x=XZ0,y=YZ1,mode='lines',name='Z1'))
    fig1.update_layout(xaxis_title='WS/H',yaxis_title='characteristic impedance')
    fig2.add_trace(go.Scatter(x=XZ0,y=vp1,mode='lines',name='vp'))
    fig2.update_layout(xaxis_title='WS/H',yaxis_title='velocity propagation')
    return fig1,fig2
if __name__=='__main__':
    app.run_server(debug=True,port='7080')
