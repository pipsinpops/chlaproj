# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 20:51:19 2024

@author: pippa

Phillippa Edwards

Clean Code for github submission

Univeristy of Plymouth

SST Analysis
Mann-Kendall Test
Graphs showing SST trend over time
Graph relating SST to Chla concetration per year

SST data downloaded from CMEMS website.
CHLA from OC-CCI database

Style created with help of Dr. Lauren Biermann (UoP) and asking google.
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

#day functions for array slicing
s_31 = [1, 3, 5, 7, 8, 10, 12]

def get_last_day(m):
    if m in s_31:
        return(31)
    elif m == 2:
        return(28)
    else:
        return(30)

#%%

#import data
data1 = xr.open_dataarray("SST_early.nc") #before 2021
data2 = xr.open_dataarray("SST_late.nc") #after 2021 - split this way on CMEMS

#set lists to export to 
dates = []
temps = []

#add together
data = xr.concat([data1, data2], dim = "time")
#data is 209 steps long 

#for each year and month:
for y in range(1998,2024):
    for m in range(1,13):

          #set the last day of the month for slicing reasons 
          d = get_last_day(m)
            
          s = date(y, m, 1)
          e  = date(y, m, d)
          
          #slice data and find mean for that month
          sub = data.sel(time = slice(s, e))
          submean = np.nanmean(sub)

          dates.append(s)
          temps.append(np.nanmean(sub))
          print(y, m, np.nanmean(sub))
          
#remove the last three from the list as they are all nan
dates = dates[:-3]
temps = temps[:-3]
#these should be same length as data

#Obtain yearly means
ytemps = []
ydates = []
for x in range(26):
    x1 = x*12 +12
    print(x*12, x1)
    subs = temps[x*12:x1]
    ydates.append(dates[x*12])
    ytemps.append(np.nanmean(subs))

graphdates = ydates + [(date(2024, 1, 1))]

#%%

#SST over time graph
sns.set_theme(style = "ticks", font_scale=1.5)
fig, ax = plt.subplots(figsize = (12, 9), dpi = 300)
sns.lineplot(x =dates,y= temps, marker = "o",
             linestyle = "--", color = "grey",
             label = "Monthly Mean")
sns.scatterplot(x = ydates, y = ytemps, marker = "s", color = "#78c9b4", s = 100, label = "Yearly Mean")
plt.xlabel("Year")
plt.ylabel("SST ($^{o}C$)")
plt.xlim([date(1997, 9, 1),date(2024, 2, 1)])
plt.ylim([5, 31])
plt.xticks(graphdates, labels = list(range(1998, 2025)), rotation = 90)
plt.legend()
plt.show()

#%%%
#Mann Kendall test:
"""
The Mann-Kendall Trend Test is used to determine whether or not a trend exists in timeseries data. It is a non-parametric test, meaning there is no underlying assumption made about normality.

mk.original_test(yourdataframe)
OUTPUT-
 trend: This tells the trend-increasing, decreasing, or no trend.
 h: True if the trend is present. False if no trend is present.
 p: The p-value of the test.
 z: The normalized test statistic.
 Tau: Kendall Tau.
 s: Mann-Kendal’s score
 var_s: Variance S
 slope: Theil-Sen estimator/slope
 intercept: Intercept of Kendall-Theil Robust Line

If you are worried about autocorrelation in your data, use a modified Mann Kendall test instead, e.g.:
mk.hamed_rao_modification_test(yourdataframe)
"""

SST_trend = mk.original_test(ytemps)
print(SST_trend)
#no trend for yearly mean
SST_trend = mk.original_test(temps)
print(SST_trend)
SST_trend =mk.hamed_rao_modification_test(temps)
print(SST_trend)
#no trend for monthly mean

#%%

#Graphing Chla against temp
chla = pd.read_csv("chla_saved.csv") #made in chla_2_analysis_f.py of yearly means
chla["temp"] = ytemps
marker_styles = {'Large Bloom': 's', 'Small Bloom': '<', "No Bloom" :"o"}
fig, ax = plt.subplots(figsize = (8, 6), dpi = 300)
sns.scatterplot(data = chla, x = "temp", y = "Mean", s= 100, palette = cm.vanimo,
                hue = "Year", style = "Size", markers = marker_styles)
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[-3:] , labels[-3:], loc='best')
plt.xlabel("Mean Sea Surface Temperature ($^{o}C$)")
plt.ylabel("Mean Chla Concentration (mg m$^{-3}$)")
plt.show()