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

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Dash'),

    html.Div(children='''
        Covid19 Data
    '''),
    dcc.Dropdown(
        id = 'dropdown-input',
        options=[
            {'label': 'Ticket price by passengers class', 'value': 'fare_class'},
            {'label': 'Age by passengers class', 'value': 'age_class'},
        ],
        value='fare_class'
    ),
    dcc.RadioItems(
        options=[
            {'label': 'Histogram', 'value': 'hist'},
            {'label': 'Boxplot', 'value': 'boxplot'}
        ],
        value='hist',
        id='map-radio'
    ),
    dcc.Graph(
        id='example-graph',
    )
])



confirmed_df = pd.read_csv(os.path.join(os.path.dirname(__file__), "raw_data_files\\confirmed_regions.csv"))
deaths_df = pd.read_csv(os.path.join(os.path.dirname(__file__), "raw_data_files\\deaths_regions.csv"))

confirmed_df.set_index(confirmed_df['Country/Region'],inplace=True)
deaths_df.set_index(deaths_df['Country/Region'],inplace=True)

#Removing first row
confirmed_df = confirmed_df.iloc[1: , :]
deaths_df = deaths_df.iloc[1: , :]

#Renaming columns
confirmed_df.rename(columns={'Country/Region': 'Country'},inplace=True)
deaths_df.rename(columns={'Country/Region': 'Country'},inplace=True)

confirmed_df.rename(columns={'Region Name': 'Continent'},inplace=True)
deaths_df.rename(columns={'Region Name': 'Continent'},inplace=True)

confirmed_df.rename(columns={'Sub-region Name': 'Region'},inplace=True)
deaths_df.rename(columns={'Sub-region Name': 'Region'},inplace=True)

#Removing unnecessary columns & grouping by Country
confirmed_df=confirmed_df.drop(columns=['Province/State', 'ISO 3166-1 Alpha 3-Codes', 'Intermediate Region Code', 'Intermediate Region Name'])

countries_confirmed_df=confirmed_df.groupby(['Country']).sum().copy()
countries_deaths_df=deaths_df.groupby(['Country']).sum().copy()

combined_df=pd.DataFrame()
combined_df['Confirmed']=countries_confirmed_df[countries_confirmed_df.columns[-1]]
combined_df['Deaths']=countries_deaths_df[countries_deaths_df.columns[-1]]
# combined_df['Recovered']=countries_recovered_df[countries_recovered_df.columns[-1]]

# print(countries_confirmed_df.head(3))

sorted_combined_df=combined_df.loc[:,["Confirmed","Deaths"]].sort_values("Confirmed",ascending=False)
sorted_combined_df['Country']=sorted_combined_df.index
combined_df.loc[:,["Confirmed","Deaths"]].sort_values("Confirmed",ascending=False).style.background_gradient(cmap='Blues',subset=["Confirmed"]).background_gradient(cmap='Reds',subset=["Deaths"]).background_gradient(cmap='Green',subset=["Recovered"])

# world_map = folium.Map(location=[11,0], tiles="cartodbpositron", zoom_start=2, max_zoom = 6, min_zoom = 2)

# for i in range(0,len(confirmed_df)):
#     folium.Circle(
#         location=[confirmed_df.iloc[i]['Lat'] if pd.isna(confirmed_df.iloc[i]['Lat']) == False else 0, confirmed_df.iloc[i]['Long'] if pd.isna(confirmed_df.iloc[i]['Long']) == False else 0],
#         fill=True,
#         radius=int((np.log2(confirmed_df.iloc[i, -5]+1))*6000),
#         color='orange',
#         fill_color='#ff8533',
#         tooltip = "<div style='margin: 0; background-color: black; color: white;'>"+
#                     "<h4 style='text-align:center;font-weight: bold'>"+confirmed_df.index[i] + "</h4>"
#                     "<hr style='margin:10px;color: white;'>"+
#                     "<ul style='color: white;;list-style-type:circle;align-item:left;padding-left:20px;padding-right:20px'>"+
#                         "<li>Confirmed: "+str(confirmed_df.iloc[i,-5])+"</li>"+
#                         "<li>Deaths:   "+str(deaths_df.iloc[i,-8])+"</li>"+
#                         "<li>Death Rate: "+ str(np.round(deaths_df.iloc[i,-8]/(confirmed_df.iloc[i,-5]+1.00001)*100,2))+ "</li>"+
#                     "</ul></div>",
#         ).add_to(world_map)

# world_map





@app.callback(
    Output(component_id='example-graph', component_property='figure'),
    [Input(component_id='map-radio', component_property='value')]
)
def update_map(plot_type):
    world_map = folium.Map(location=[11,0], tiles="cartodbpositron", zoom_start=2, max_zoom = 6, min_zoom = 2)

    for i in range(0,len(confirmed_df)):
        folium.Circle(
            location=[confirmed_df.iloc[i]['Lat'] if pd.isna(confirmed_df.iloc[i]['Lat']) == False else 0, confirmed_df.iloc[i]['Long'] if pd.isna(confirmed_df.iloc[i]['Long']) == False else 0],
            fill=True,
            radius=int((np.log2(confirmed_df.iloc[i, -5]+1))*6000),
            color='orange',
            fill_color='#ff8533',
            tooltip = "<div style='margin: 0; background-color: black; color: white;'>"+
                        "<h4 style='text-align:center;font-weight: bold'>"+confirmed_df.index[i] + "</h4>"
                        "<hr style='margin:10px;color: white;'>"+
                        "<ul style='color: white;;list-style-type:circle;align-item:left;padding-left:20px;padding-right:20px'>"+
                            "<li>Confirmed: "+str(confirmed_df.iloc[i,-5])+"</li>"+
                            "<li>Deaths:   "+str(deaths_df.iloc[i,-8])+"</li>"+
                            "<li>Death Rate: "+ str(np.round(deaths_df.iloc[i,-8]/(confirmed_df.iloc[i,-5]+1.00001)*100,2))+ "</li>"+
                        "</ul></div>",
            ).add_to(world_map)

    world_map
    






if __name__ == '__main__':
    app.run_server(debug=True)