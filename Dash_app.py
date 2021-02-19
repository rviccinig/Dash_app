# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 14:25:41 2020

@author: rvicc
"""


# JLL Operational Cost Index App 2020

#Importing all the needed Packages
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import json
import base64
import numpy as np
from numpy import random
import plotly.express as px
#import dash_table_experiments as dt
import dash_table
from plotly.io import to_image
import dash_auth



#authentication

USERNAME_PASSWORD_PAIRS=[['username','password'],['reinaldo','123']]


#elements for the map
df=pd.read_excel('Dashboard_data.xlsx')
token = "pk.eyJ1IjoicnZpY2NpbmlnIiwiYSI6ImNrZGh3ZmdreTJqZDEyeHQxbXRqd3g1OHUifQ.55KcWKwVw2cqY8IoIhEnWg"
px.set_mapbox_access_token(token)
df['Label']=df['Bldg Name']+' '+'$' +df['OpEx & Taxes'].astype(str)+' p.s.f'


#Images and Logos

def encode_image(image_file):
    encoded = base64.b64encode(open(image_file, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded.decode())


JLL_Logo=encode_image('./Jll_logo2.png')

#Variables for Table

Table_Vars=['Bldg Name','Address', 'Bldg Class','Submarket','OpEx & Taxes','Parking Ratio','Build Year','Bldg Size']

#Creating App Instance
app=dash.Dash()
auth=dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)

app.layout=html.Div(children=[
    html.Div([html.Img(id='JLL-Logo',src=JLL_Logo,
                             style={'height': '10%',
                                    'width': '10%',
                                    'float':'left',
                                    'position':'relative',
                                    'padding-top':0})],style={'padding': 15}),
    html.Div([],style={'height': '80px'}),
    html.Div(id='My_title',children="JLL Calgary's Op.Cost Index 2018-2020",style={'font-family':'arial','font-size':'18px','font-weight':'bold','padding': 15}),
    html.Div([],style={'height': '10px'}),
    html.Div(id='My_title2',children="Customize you own Dashboard",style={'font-family':'arial','font-size':'18px','padding': 15}),
    html.Div([],style={'height': '0px'}), 
    html.Div([dcc.Markdown('''
                 We have created this Op.Cost app so our clients can easily
                 interact with our data. Go ahead and filter by area of the city,
                 building class and year built. Visualize the data in a map, look at the table
                 of comparable buildings and download your personalized report. Our goal is 
                 to **help** landlords remain competitive in the difficult times we are living.
                 Tenants can also look for the properties that might better suite them
                 and reduce their expenses.After filtering the data you need, click in the button
                 to download the full report.
                 ''')],style={'padding': 15,'font-family':'arial','font-size':'14px'}),
    html.Div([],style={'height': '20px'}),
    html.Div(id='first Square',children=[
            
                                html.Div(children='Select your options for your building list',style={'padding': 15,'font-family':'arial','font-size':'18px','font-weight':'bold'}),
                                html.Div(children='Select Operational Cost Range',style={'padding': 15,'font-family':'arial','font-size':'14px'}),                                                 
                                html.Div([dcc.RangeSlider(id='My-Range-Slider',
                                                min=0,
                                                max=40,
                                                step=4,
                                                value=[df['OpEx & Taxes'].min(),df['OpEx & Taxes'].max()],
                                                marks={i: '{}'.format(i) for i in range(0,40 ,2)})],style={'padding': 15,'font-family':'arial'}),
                                html.Div([],style={'height': '5px'}),
                                html.Div(children='Select Building Class',style={'padding': 15,'font-family':'arial','font-size':'14px'}),
                                html.Div([dcc.Checklist(id='class-building',options=[{'label': 'A', 'value': 'A'},
                                                                                             {'label': 'B', 'value': 'B'},
                                                                                             {'label': 'C', 'value': 'C'}
                                                                                             ],
                                                                                    value=['A', 'B','C'],
                                                                                    labelStyle={'display': 'inline-block'})],style={'padding': 15,'font-family':'arial','font-size':'14px'}),
                                html.Div([],style={'height': '5px'}), 
                                html.Div(children='Select Submarket',style={'padding': 15,'font-family':'arial','font-size':'14px'}),
                                html.Div([dcc.Dropdown(id='Submarket',options=[
                                                                    {'label': 'Beltline', 'value': 'Beltline'},
                                                                    {'label': 'South', 'value': 'South'},
                                                                    {'label': 'Northeast', 'value': 'Northeast'},
                                                                    {'label': 'Northwest', 'value': 'Northwest'}],
                                                                    multi=True,
                                                                    value=['Beltline', 'South','Northeast','Northwest'])],style={'padding': 15,'font-family':'arial'})],style={'background-color':'#F0F0F0'}),
                                html.Div([],style={'height': '40px'}),
    html.Div(children='Report Summary',style={'padding': 15,'font-family':'arial','font-size':'18px','font-weight':'bold'}),
    html.Div(children=[
            html.Div(id='Sample_Mean',children=[],style={'width':'33%','font-size':26,'text-align':'center','display': 'inline-block','float':'left'}),
            html.Div(id='Median',children=[],style={'width':'33%','font-size':26,'text-align':'center','display': 'inline-block','float':'right'}),
            html.Div(id='Number_Buildings',children=[],style={'width':'33%','font-size':26,'text-align':'center','display': 'inline-block','float':'right'})],style={'padding': 15,
                                                                                                                                                'font-family':'arial',
                                                                                                                                                'font-size':'14px',
                                                                                                                                                'font-weight':'bold'}),
    html.Div([],style={'height': '60px'}),        
    html.Div(children='Building List',style={'padding': 15,'font-family':'arial','font-size':'18px','font-weight':'bold'}),
    html.Div([dash_table.DataTable(id='table-paging-and-sorting',
                             columns=[{'name': i, 'id': i, 'deletable': True} for i in Table_Vars],
                             fixed_rows={'headers': True},
                             page_current=0,
                             page_size=300,
                             page_action='custom',
                             sort_action='custom',
                             sort_mode='single',
                             sort_by=[],
                             style_table={'height': '1200px','overflowY': 'auto'},
                             row_deletable=True,
                             style_cell={'textAlign': 'left','font-family':'arial'})],style={'padding': 15,'font-family':'arial'}),
    
   # dcc.Graph(id='Data-Table'),
    html.Div([],style={'height': '0px'}),
    html.Div(children='Building Locations',style={'padding': 15,'font-family':'arial','font-size':'18px','font-weight':'bold'}),
    html.Div([dcc.Graph(id='Map-Properties')],style={'padding': 15}),
    html.Div(children='Historical Data',style={'padding': 15,'font-family':'arial','font-size':'18px','font-weight':'bold'}),
    html.Div([dcc.Graph(id='Histogram-1')],style={'padding': 15}),
    html.Div([],style={'width': '20px'}),
    html.Div([dcc.Textarea(placeholder='Enter comments...',value='Enter Additional Comments',style={'width': '100%','font-family':'arial'})],style={'padding': 15,'font-family':'arial'}),
    html.Div([],style={'height': '20px'}),
    html.Div([dcc.Loading(html.A(id="img-download",href="", 
                       children=[html.Button("Download Full Report", id="download-btn")], 
                       target="_blank",
                       download="JLL_Calgary_OpCost_2020.pdf"
                       ))],style={'padding': 15}),
    
    
    # testing data table
   


    # end of the app
    ],style={'padding': 25})
                 
                 
#Call back data datble

@app.callback(
    Output('table-paging-and-sorting', 'data'),
    [Input('My-Range-Slider','value'),
     Input('class-building','value'),
     Input('Submarket','value'),
     Input('table-paging-and-sorting', "page_current"),
     Input('table-paging-and-sorting', "page_size"),
     Input('table-paging-and-sorting', 'sort_by')])
def update_table(dataf,bclass,submarket,page_current, page_size, sort_by):
    df2=df.loc[(df['OpEx & Taxes']>dataf[0]) & (df['OpEx & Taxes']<dataf[1])]
    df3=df2.loc[(df['Bldg Class'].isin(bclass)) ]
    df4=df3.loc[(df['Submarket'].isin(submarket)) ]
    if len(sort_by):
        dff = df4.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=False
        )
    else:
        # No sort is applied
        dff = df4

    return dff.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')                 
                 

#Call Back from the Map

@app.callback(Output('Map-Properties','figure'),
               [Input('My-Range-Slider','value'),Input('class-building','value'),Input('Submarket','value')])

def filter_Map(dataf,bclass,submarket):
    df.sort_values(by='OpEx & Taxes', ascending=True)
    df2=df.loc[(df['OpEx & Taxes']>dataf[0]) & (df['OpEx & Taxes']<dataf[1])]
    df3=df2.loc[(df['Bldg Class'].isin(bclass)) ]
    df4=df3.loc[(df['Submarket'].isin(submarket)) ]
    df4.sort_values(by='OpEx & Taxes', ascending=True)
    figure2= px.scatter_mapbox(df4, lat="Latitude", lon="Longitude" , 
                               color="OpEx & Taxes",size="OpEx & Taxes",
                               text='Label',zoom=11,size_max=15,
                               center={"lat":51.038200,"lon":-114.072115})
    
    return figure2

#Call Back from the Histogram
@app.callback(Output('Histogram-1','figure'),
               [Input('My-Range-Slider','value'),Input('class-building','value'),Input('Submarket','value')])

def filter_Histogram(dataf,bclass,submarket):
    df.sort_values(by='OpEx & Taxes', ascending=True)
    df2=df.loc[(df['OpEx & Taxes']>dataf[0]) & (df['OpEx & Taxes']<dataf[1])]
    df3=df2.loc[(df['Bldg Class'].isin(bclass)) ]
    df4=df3.loc[(df['Submarket'].isin(submarket)) ]
    df4.sort_values(by='OpEx & Taxes', ascending=True)
    figure3= go.Figure(px.histogram(df4, x="OpEx & Taxes",
                   title='',
                   labels={'total_bill':'total bill'}, # can specify one label per df column
                   opacity=0.8,
                   log_y=True, # represent bars with log scale
                   color_discrete_sequence=['indianred'] # color of histogram bars
                   ))
    
    return figure3    

#Call Back for the mean
@app.callback(Output('Sample_Mean','children'),
               [Input('My-Range-Slider','value'),Input('class-building','value'),Input('Submarket','value')])

def Sample_mean(dataf,bclass,submarket):
    df.sort_values(by='OpEx & Taxes', ascending=True)
    df2=df.loc[(df['OpEx & Taxes']>dataf[0]) & (df['OpEx & Taxes']<dataf[1])]
    df3=df2.loc[(df['Bldg Class'].isin(bclass)) ]
    df4=df3.loc[(df['Submarket'].isin(submarket)) ]
    df4.sort_values(by='OpEx & Taxes', ascending=True)   
    mean1=round(df4['OpEx & Taxes'].mean(),1)
    return 'Mean: ${} '.format(mean1)     


#Call Back for the number of buildings
@app.callback(Output('Number_Buildings','children'),
               [Input('My-Range-Slider','value'),Input('class-building','value'),Input('Submarket','value')])

def number_buildings(dataf,bclass,submarket):
    df.sort_values(by='OpEx & Taxes', ascending=True)
    df2=df.loc[(df['OpEx & Taxes']>dataf[0]) & (df['OpEx & Taxes']<dataf[1])]
    df3=df2.loc[(df['Bldg Class'].isin(bclass)) ]
    df4=df3.loc[(df['Submarket'].isin(submarket)) ]
    df4.sort_values(by='OpEx & Taxes', ascending=True)   
    number_buildings=len(df4['OpEx & Taxes'])    
    return 'Buildings: {} '.format(number_buildings) 

#Call Back for the Median
#Call Back for the number of buildings
@app.callback(Output('Median','children'),
               [Input('My-Range-Slider','value'),Input('class-building','value'),Input('Submarket','value')])

def number_median(dataf,bclass,submarket):
    df.sort_values(by='OpEx & Taxes', ascending=True)
    df2=df.loc[(df['OpEx & Taxes']>dataf[0]) & (df['OpEx & Taxes']<dataf[1])]
    df3=df2.loc[(df['Bldg Class'].isin(bclass)) ]
    df4=df3.loc[(df['Submarket'].isin(submarket)) ]
    df4.sort_values(by='OpEx & Taxes', ascending=True)   
    medvalue=len(df4['OpEx & Taxes'])//2 
    median=df4['OpEx & Taxes'][medvalue]
    return 'Median: ${} '.format(median)  






#Call Back for Report
    
@app.callback(Output('img-download', 'n_clicks'),
              [Input('Map-Properties', 'figure')])
def make_image(figure):
    """ Make a picture """

    fmt = "pdf"
    mimetype = "application/pdf"
    data = base64.b64encode(to_image(figure, format=fmt)).decode("utf-8")
    pdf_string = 'data:{};base64,{}'.format(mimetype,data)

    return pdf_string

if __name__ == '__main__':
    app.run_server(debug=False)











#Running the Application                                                               

if __name__=='__main__':
    app.run_server()


