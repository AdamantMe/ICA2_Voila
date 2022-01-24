from __future__ import print_function
from ipywidgets import interact, interactive, fixed, interact_manual
from IPython.core.display import display, HTML
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import folium
import plotly.graph_objects as go
import ipywidgets as widgets
import requests
# loading data right from the source:
confirmed_df = pd.read_csv(os.path.join(os.path.dirname(__file__), "raw_data_files/confirmed_regions.csv"))
death_df = pd.read_csv(os.path.join(os.path.dirname(__file__), "raw_data_files/deaths_regions.csv"))

confirmed_df.set_index(confirmed_df['Province/State'],inplace=True)
confirmed_df.rename(columns={'Province/State': 'State'},inplace=True)
death_df.set_index(death_df['Province/State'],inplace=True)
death_df.rename(columns={'Province/State': 'State'},inplace=True)
confirmed_df_states=confirmed_df.groupby(['State']).sum().copy()
death_df_states=death_df.groupby(['State']).sum().copy()
confirmed_df_states=pd.merge(confirmed_df[['Lat', 'Long','State']].groupby(['State']).mean(),confirmed_df_states, left_index=True, right_index=True)
death_df_states=pd.merge(death_df[['Lat', 'Long','State']].groupby(['State']).mean(),death_df_states, left_index=True, right_index=True)
combined_df=pd.DataFrame()
combined_df['Confirmed']=confirmed_df_states[confirmed_df_states.columns[-1]]
combined_df['Deaths']=death_df_states[death_df_states.columns[-1]]
sorted_combined_df=combined_df.loc[:,["Confirmed","Deaths"]].sort_values("Confirmed",ascending=False)
sorted_combined_df['State']=sorted_combined_df.index
combined_df.loc[:,["Confirmed","Deaths"]].sort_values("Confirmed",ascending=False).style.background_gradient(cmap='Blues',subset=["Confirmed"]).background_gradient(cmap='Reds',subset=["Deaths"])