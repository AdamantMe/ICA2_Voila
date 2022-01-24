import os
import pandas as pd
import numpy as np
import folium
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

# print(countries_confirmed_df.head(3))

sorted_combined_df=combined_df.loc[:,["Confirmed","Deaths"]].sort_values("Confirmed",ascending=False)
sorted_combined_df['Country']=sorted_combined_df.index
combined_df.loc[:,["Confirmed","Deaths"]].sort_values("Confirmed",ascending=False).style.background_gradient(cmap='Blues',subset=["Confirmed"]).background_gradient(cmap='Reds',subset=["Deaths"]).background_gradient(cmap='Green',subset=["Recovered"])

# sorted_df = pd.DataFrame(sorted, columns=['A'])
# confirmed_df_cleared = confirmed_df.filter(['Country', 'Continent Code', 'Continent', '1/21/22'])
# combined_rows = confirmed_df.groupby(['Continent Code', 'Continent', 'Long', 'Lat']).sum()
# combined_rows1 = confirmed_df.groupby(['Continent Code', 'Continent']).sum()
# combined_rows = confirmed_df.groupby(['Continent Code', 'Continent']).sum()
# new_col_Longtitude = [100.6197, 9.0000, 105.2551, 34.5085, 140.0188]  # can be a list, a Series, an array or a scalar   
# new_col_Latitude = [34.0479, 53.0000, 54.5260, 8.7832, 22.7359]  # can be a list, a Series, an array or a scalar   
# combined_rows.insert(loc=0, column='Long', value=new_col_Longtitude)
# combined_rows.insert(loc=0, column='Lat', value=new_col_Latitude)
# print(combined_rows.head())
    
combined_rows = confirmed_df.groupby(['Continent Code', 'Continent'], as_index=False).sum()
if (True):
    idx = 0
    new_col_Longtitude = [100.6197, 9.0000, -105.2551, 34.5085, 140.0188]  # can be a list, a Series, an array or a scalar   
    new_col_Latitude = [34.0479, 53.0000, 54.5260, 8.7832, 22.7359]  # can be a list, a Series, an array or a scalar   
    combined_rows.insert(loc=idx, column='Long', value=new_col_Longtitude)
    combined_rows.insert(loc=idx, column='Lat', value=new_col_Latitude)

# combined_rows = confirmed_df.reset_index()
combined_regions = confirmed_df.filter(['Region Code', 'Region', 'Lat', 'Long', '1/21/22'])

combined_regions['Long'] = combined_regions['Long'].fillna(0.0).astype(float)
combined_regions['Long'] = combined_regions['Long'].fillna(0.0).astype(int)
combined_regions['Lat'] = combined_regions['Lat'].fillna(0.0).astype(float)
combined_regions['Lat'] = combined_regions['Lat'].fillna(0.0).astype(int)
d = {'1/21/22':'Confirmed', 'Lat':'Lat','Long':'Long'}
combined_regions = combined_regions.groupby(['Region', 'Region Code']).agg({'1/21/22':'sum', 'Lat':'mean','Long':'mean'}).rename(columns=d)

combined_regions = combined_regions.reset_index()

asd = combined_regions
    
# fig = go.Figure(data=go.Scattergeo(
#         lon = combined_rows['Long'],
#         lat = combined_rows['Lat'],
#         text = combined_rows['Continent'],        
#         mode = 'markers',
#         marker=dict(color=list(range(702)),
#                     colorscale='viridis',
#                     size=combined_rows['1/21/22'] / 500000)
#         ))

# fig.update_layout(
#         title = 'COVID19',
#         geo_scope='world',
#     )

# fig.show()


app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='COVID19'),

    dcc.RadioItems(
        options=[
            {'label': 'Continent', 'value': 'Continent'},
            {'label': 'Region', 'value': 'Region'},
            {'label': 'Country', 'value': 'Country'}
        ],
        value='Continent',
        id='radio_space'
    ),
    dcc.Graph(id='map_world', figure={}),
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
    )
])

@app.callback(
    Output(component_id='graph_confirmed_death', component_property='figure'),
    [Input(component_id='radio_data_shown', component_property='value')])
def update_bar(radio_choice):
    figure = px.bar(
    sorted_combined_df.head(10),
    x = "Country",
    y = radio_choice,
    title= "Top 10 worst affected Countries", # the axis names
    color_discrete_sequence=["Orange"], 
    height=500,
    width=800
    )

    return figure

@app.callback(
Output(component_id='map_world', component_property='figure'),
[Input(component_id='radio_space', component_property='value')])
def update_graph(option_slctd):
    dff = confirmed_df.copy()
    
    combined_rows = confirmed_df.groupby(['Continent Code', 'Continent'], as_index=False).sum()
    combined_rows = combined_rows.reset_index()
    if (True):
        idx = 0
        new_col_Longtitude = [100.6197, 9.0000, 105.2551, 34.5085, 140.0188]  # can be a list, a Series, an array or a scalar   
        new_col_Latitude = [34.0479, 53.0000, 54.5260, 8.7832, 22.7359]  # can be a list, a Series, an array or a scalar   
        combined_rows.insert(loc=idx, column='Long', value=new_col_Longtitude)
        combined_rows.insert(loc=idx, column='Lat', value=new_col_Latitude)

    fig = go.Figure(data=go.Scattergeo(
        lon = combined_rows['Long'],
        lat = combined_rows['Lat'],
        text = combined_rows['Continent'],
        mode = 'markers',
        marker=dict(color=list(range(1275)),
                    colorscale='viridis',
                    size=combined_rows['1/21/22'] / 2000000)
        ))

    fig.update_layout(
        title = 'COVID19',
        geo_scope='world',
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)