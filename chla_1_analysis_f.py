# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 21:31:59 2024

@author: pippa

Phillippa Edwards

Clean Code for github submission

Univeristy of Plymouth

Comparison of Chlorophyll-a data before and after bloom
This is a yearly trend comparison to see if befire and after the bloom there is a change in chlorophyll-a timing
uses wilcox test.

CHLA from OC-CCI database

"""

import netCDF4 as nc
import matplotlib.pyplot as plt
from shapely.geometry.polygon import LinearRing
import matplotlib
matplotlib.rcParams['font.family'] = 'Arial'
import matplotlib.dates as mdates
import pandas as pd
import pymannkendall as mk
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import xarray as xr
from cmcrameri import cm
import os
from datetime import date
import seaborn as sns
import math
from scipy import stats
os.chdir("C:/Users/pippa/OneDrive/Documents/Uni/Year3/dissi/dissi_code/usethisdata")


#%%

#Looking at themonths

#load in data
data = xr.open_dataset("chla_conc_YS.nc")
chla = data["chlor_a"]

#make dataframe base:
df = {"Month":[],
      "Year":[],
      "Mean":[],
      "Time":[]}

years = list(range(1998,2024))

for year in years:
    for month in range(1,13):
        if month < 6:
            df["Month"].append(month+12)
            df["Year"].append(year-1)
            if year-1 < 2007:
                df["Time"].append("Before 2007")
            else:
                df["Time"].append("After 2007")
        else:
            df["Month"].append(month)
            df["Year"].append(year)
            if year < 2007:
                df["Time"].append("Before 2007")
            else:
                df["Time"].append("After 2007")

        
for x in range(312):    
    sub = chla[x, :, :]
    df["Mean"].append(np.nanmean(sub))

df = pd.DataFrame(data = df)

#%%

#Graph before and after to show trend over a year. 
m_labels = ["Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec","Jan", "Feb", "Mar", "Apr", "May"]

pal = ["#8f2662", "#8eb840", "#78c9b4"]
sns.set_theme(style = "ticks", font_scale=1.5)


fig, ax = plt.subplots(figsize = (12, 9), dpi = 300)
sns.lineplot(x="Month", y="Mean", hue="Time", data=df,
             marker="o", palette= pal)
plt.legend(loc = "upper left")
plt.xticks(range(6,18), m_labels)
plt.ylabel("Mean Chla Concentration (mg m$^{-3}$)")
plt.margins(0.0)
plt.show()

#%%
#stats test to see difference between

befores = df[df["Time"]=="Before 2007"]
afters = df[df["Time"]=="After 2007"]


bef_avs = []
aft_avs = []

for m in range(6,18):
    bef = befores[befores["Month"] == m]
    af = afters[afters["Month"] == m]
    
    bef_avs.append(np.nanmean(bef["Mean"]))
    aft_avs.append(np.nanmean(af["Mean"]))

stats.wilcoxon(bef_avs, aft_avs)
#WilcoxonResult(statistic=2.0, pvalue=0.00146484375)

#apparently significant increase.

