import pandas as pd
import numpy as np

dfcountry = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/01-01-2021.csv")
dfconfirmed = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/01-10-2022.csv")
dfrecovered = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/4e067f927ea439d291f6df515079a80bc1a8cb88/csse_covid_19_data/csse_covid_19_daily_reports/01-01-2022.csv")
dfdeaths = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/00a1ea4c9821ac9c737a36f697a2241d64dd63b8/csse_covid_19_data/csse_covid_19_daily_reports/01-01-2021.csv")


#Each country confirmed and death cases increasing graph
import plotly.graph_objects as go
def plot_cases_for_country(country):
    labels = ['confirmed', 'deaths']
    colors = ['blue', 'red']
    mode_size = [6, 8]
    line_size = [4, 5]

    dflist = [dfconfirmed, dfdeaths]

    fig = go.Figure()

    for i, df in enumerate(dflist):
        if country == 'World' or country =='world':
            x_data = np.array(list(df.iloc[:, 2:].columns))
            y_data = np.sum(np.asarray(df.iloc[:, 2:]), axis=0)

        else:
            x_data = np.array(list(df.iloc[:, 2:].columns))
            y_data = np.sum(np.asarray(df[df['Country_Region']==country].iloc[:, 2:]), axis=0)

        fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines+markers', 
                                 name=labels[i],
                                 line = dict(color=colors[i], width=line_size[i]), 
                                 connectgaps=True, 
                                 text = "Total " + str(labels[i]) + ": "+ str(y_data[-1])))


    fig.show()


plot_cases_for_country('India')