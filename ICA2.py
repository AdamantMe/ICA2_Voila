import os
import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

confirmed_df = pd.read_csv(os.path.join(os.path.dirname(__file__), "raw_data_files/confirmed_regions.csv"))
deaths_df = pd.read_csv(os.path.join(os.path.dirname(__file__), "raw_data_files/deaths_regions.csv"))

confirmed_df.set_index(confirmed_df['Country/Region'],inplace=True)
deaths_df.set_index(deaths_df['Country/Region'],inplace=True)

#Removing first row
confirmed_df = confirmed_df.iloc[1: , :]
deaths_df = deaths_df.iloc[1: , :]
confirmed_df = confirmed_df.astype({"1/21/22": int})
deaths_df = deaths_df.astype({"1/21/22": int})

#Renaming columns
confirmed_df.rename(columns={'Country/Region': 'Country', 'Region Name': 'Continent', 'Sub-region Name': 'Region', 'Region Code': 'Continent Code', 'Sub-region Code': 'Region Code'},inplace=True)
deaths_df.rename(columns={'Country/Region': 'Country', 'Region Name': 'Continent', 'Sub-region Name': 'Region', 'Region Code': 'Continent Code', 'Sub-region Code': 'Region Code'},inplace=True)

#Removing unnecessary columns & grouping by Country
confirmed_df=confirmed_df.drop(columns=['Province/State', 'ISO 3166-1 Alpha 3-Codes', 'Intermediate Region Code', 'Intermediate Region Name'])

countries_confirmed_df=confirmed_df.groupby(['Country']).sum().copy()
countries_deaths_df=deaths_df.groupby(['Country']).sum().copy()

combined_df=pd.DataFrame()
combined_df['Confirmed']=countries_confirmed_df[countries_confirmed_df.columns[-1]]
combined_df['Deaths']=countries_deaths_df[countries_deaths_df.columns[-1]]

sorted_combined_df=combined_df.loc[:,["Confirmed","Deaths"]].sort_values("Confirmed",ascending=False)
sorted_combined_df['Country']=sorted_combined_df.index
combined_df.loc[:,["Confirmed","Deaths"]].sort_values("Confirmed",ascending=False).style.background_gradient(cmap='Blues',subset=["Confirmed"]).background_gradient(cmap='Reds',subset=["Deaths"]).background_gradient(cmap='Green',subset=["Recovered"])

confirmed_countries = confirmed_df.filter(['Country', 'Lat', 'Long', '1/21/22'])
confirmed_countries['Long'] = confirmed_countries['Long'].fillna(0.0).astype(float)
confirmed_countries['Long'] = confirmed_countries['Long'].fillna(0.0).astype(int)
confirmed_countries['Lat'] = confirmed_countries['Lat'].fillna(0.0).astype(float)
confirmed_countries['Lat'] = confirmed_countries['Lat'].fillna(0.0).astype(int)
column_names = {'1/21/22':'Confirmed', 'Lat':'Lat','Long':'Long'}
# confirmed_countries = confirmed_countries.groupby(['Country']).agg({'1/21/22':'sum', 'Lat':'mean','Long':'mean'}).rename(columns=column_names)
# confirmed_countries = confirmed_countries.reset_index()

confirmed_regions = confirmed_df.filter(['Region Code', 'Region', 'Lat', 'Long', '1/21/22'])
confirmed_regions['Long'] = confirmed_regions['Long'].fillna(0.0).astype(float)
confirmed_regions['Long'] = confirmed_regions['Long'].fillna(0.0).astype(int)
confirmed_regions['Lat'] = confirmed_regions['Lat'].fillna(0.0).astype(float)
confirmed_regions['Lat'] = confirmed_regions['Lat'].fillna(0.0).astype(int)
column_names = {'1/21/22':'Confirmed', 'Lat':'Lat','Long':'Long'}
confirmed_regions = confirmed_regions.groupby(['Region', 'Region Code']).agg({'1/21/22':'sum', 'Lat':'mean','Long':'mean'}).rename(columns=column_names)
confirmed_regions = confirmed_regions.reset_index()

deaths_regions = deaths_df.filter(['Region Code', 'Region', 'Lat', 'Long', '1/21/22'])
deaths_regions['Long'] = deaths_regions['Long'].fillna(0.0).astype(float)
deaths_regions['Long'] = deaths_regions['Long'].fillna(0.0).astype(int)
deaths_regions['Lat'] = deaths_regions['Lat'].fillna(0.0).astype(float)
deaths_regions['Lat'] = deaths_regions['Lat'].fillna(0.0).astype(int)
column_names = {'1/21/22':'Deaths', 'Lat':'Lat','Long':'Long'}
deaths_regions = deaths_regions.groupby(['Region', 'Region Code']).agg({'1/21/22':'sum', 'Lat':'mean','Long':'mean'}).rename(columns=column_names)
deaths_regions = deaths_regions.reset_index()

confirmed_continents = confirmed_df.groupby(['Continent Code', 'Continent'], as_index=False).sum()
confirmed_continents = confirmed_continents.reset_index()
new_col_Longtitude = [100.6197, 9.0000, -75.2551, 34.5085, 125.0188]  
new_col_Latitude = [34.0479, 53.0000, 10, 8.7832, -10.7359]
confirmed_continents.insert(loc=0, column='Long', value=new_col_Longtitude)
confirmed_continents.insert(loc=0, column='Lat', value=new_col_Latitude)

app = dash.Dash()
server = app.server

app.layout = html.Div(children=[
    html.H1(children='Pandemic Data Visualisation'),

    html.Div(children=[
        dcc.RadioItems(
        options=[
            {'label': 'Country', 'value': 'Country'},
            {'label': 'Region', 'value': 'Region'},
            {'label': 'Continent', 'value': 'Continent'},
        ],
        value='Country',
        id='radio_space'
        ),
        dcc.Graph(id='map_world', figure={},
            style={
                'background-color':'#2B2A2A',
                "verticalAlign": "center",
                "horizontalAlign": "center",
                }),
        ], 
        style={
            'textAlign': 'center',
            'margin': 'auto',
            "margin-left": "20px",
            "verticalAlign": "top",
            "horizontalAlign": "center",
            'padding': 10, 
            'flex': 1
        }
    ),

    html.Div(children = [
    dcc.RadioItems(
        options=[
            {'label': 'Confirmed cases', 'value': 'Confirmed'},
            {'label': 'Deaths', 'value': 'Deaths'},
        ],
        value='Confirmed',
        id='radio_data_shown'
        ),
        dcc.Graph(
            id='graph_confirmed_death',
            style={'background-color':'#2B2A2A'}
        )
        ], 
        style={
            'textAlign': 'center',
            'align-items': 'center',
            'padding': 10, 
            'flex': 1
        }
    ),
], style={'vertical-align': 'center'})

@app.callback(
    Output(component_id='graph_confirmed_death', component_property='figure'),
    [Input(component_id='radio_data_shown', component_property='value')])
def update_bar(radio_choice):
    
    sorted_combined_df=combined_df.loc[:,["Confirmed","Deaths"]].sort_values(radio_choice,ascending=False)
    sorted_combined_df['Country']=sorted_combined_df.index

    figure = px.bar(
    sorted_combined_df.head(10),
    x = "Country",
    y = radio_choice,
    title= "Top 10 worst affected Countries", # the axis names
    color = radio_choice, 
    )

    figure.update_layout(paper_bgcolor = "rgb(43,42,42)")

    figure.update_xaxes(title_font=dict(size=18, family='Courier', color='#E6E6E6'), tickfont=dict(family='arial', color='#E6E6E6', size=14), ticks="outside", tickwidth=2, ticklen=10)
    figure.update_yaxes(title_font=dict(size=18, family='Courier', color='#E6E6E6'), tickfont=dict(family='arial', color='#E6E6E6', size=14))   
    figure.update_layout(title_font_color="white",
    plot_bgcolor = 'rgba(0, 0, 0, 0)',
    paper_bgcolor = 'rgba(0, 0, 0, 0)',)
    figure.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

    return figure

@app.callback(
Output(component_id='map_world', component_property='figure'),
[Input(component_id='radio_space', component_property='value')])
def update_map(option_slctd):
    if (option_slctd == "Country"):
        if 'Text' not in confirmed_countries.columns:
            confirmed_countries.insert(loc=0, column='Text', value="")
            confirmed_countries['Text'] = confirmed_countries['Country'] + " confirmed cases: " + confirmed_countries['1/21/22'].astype(str)
        fig = go.Figure(data=go.Scattergeo(
            lon = confirmed_countries['Long'],
            lat = confirmed_countries['Lat'],
            text = confirmed_countries['Text'],
            mode = 'markers',
            marker = dict(
            opacity = 0.8,
            symbol = 'triangle-up',
            colorscale = 'plasma',
            color=list(range(850)),
            cmax = 850,
            cmin = 30,
            size = confirmed_countries['1/21/22'] / 500000 + 10
            )))    
    elif (option_slctd == "Continent"):
        if 'Text' not in confirmed_continents.columns:
            confirmed_continents.insert(loc=0, column='Text', value="")
            confirmed_continents['Text'] = confirmed_continents['Continent'] + " confirmed cases: " + confirmed_continents['1/21/22'].astype(str)
        fig = go.Figure(data=go.Scattergeo(
            lon = confirmed_continents['Long'],
            lat = confirmed_continents['Lat'],
            text = confirmed_continents['Text'],
            mode = 'markers',
            marker = dict(
            opacity = 0.8,
            autocolorscale = True,
            symbol = 'star',
            colorscale = 'plasma',
            cmin = 0,
            color=list(range(140)),
            cmax = 140,
            size = confirmed_continents['1/21/22'] / 1000000 + 30
            )))
    elif (option_slctd == "Region"):
        if 'Text' not in confirmed_regions.columns:
            confirmed_regions.insert(loc=0, column='Text', value="")
            confirmed_regions['Text'] = confirmed_regions['Region'] + " confirmed cases: " + confirmed_regions['Confirmed'].astype(str)
        fig = go.Figure(data=go.Scattergeo(
            lon = confirmed_regions['Long'],
            lat = confirmed_regions['Lat'],
            text = confirmed_regions['Text'],
            mode = 'markers',
            marker = dict(
            opacity = 0.8,
            autocolorscale = False,
            symbol = 'diamond-dot',
            colorscale = 'icefire',
            color=list(range(80)),
            cmax = 80,
            cmin = 1,
            size = confirmed_regions['Confirmed'] / 1000000 + 10
            )))

    map_title = "Confirmed Covid-19 Cases By " + option_slctd

    fig.update_layout(
        title = map_title,
        title_font_color="#E6E6E6",
        title_x=0.5,
        geo = dict(
            scope='world',
            projection_type='orthographic',
            showland = True,
            landcolor = "rgb(250, 250, 250)",
            subunitcolor = "rgb(217, 217, 217)",
            countrycolor = "rgb(217, 217, 217)",
            bgcolor='rgb(43,42,42)',
            countrywidth = 0.5,
            subunitwidth = 0.5,
        ),
    )

    fig.update_geos(
    resolution=110,
    showcoastlines=True, coastlinecolor="Black",
    showland=True, landcolor="LightGreen",
    showocean=True, oceancolor="White",
    showlakes=True, lakecolor="LightBlue",
    showrivers=True, rivercolor="LightBlue"
    )
    
    fig.update_layout(height=700, paper_bgcolor = "rgb(43,42,42)")
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)