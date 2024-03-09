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

Style created with help of Dr. Lauren Biermann (UoP) and asking google.

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
data = xr.open_dataset("chla_conc_YS.nc")
chla = data["chlor_a"]


years = list(range(1998,2024))


#Get yearly mean of chlorophyll-a
df = {"Year": years,
      "Mean": []}

for y in list(range(1998,2024)):
    year_data = chla.sel(time = slice(f"{y}-01-01", f"{y}-12-31"))
    mean_chla = np.nanmean(year_data)
    print(y, mean_chla)
    df["Mean"].append(mean_chla)
    
df = pd.DataFrame(data = df)
df["Time"] = ["Before 2007"] * 9 + ["After 2007"] * 17



#%%

#monthly mean of chla
df2 = {"Year" : [],
       "Mean" : []}

for year in years:
    for month in range(12):
        point = year + ((1/12)*month)
        df2["Year"].append(point)

for x in range(312):    
    sub = chla[x, :, :]
    df2["Mean"].append(np.nanmean(sub))

df2 = pd.DataFrame(data = df2)
df2["Time"] = ["Before 2007"] * 9 *12 + ["After 2007"] * 17 *12


#%%

#base plot for green colouring in powrpoint
sns.set_theme(style = "ticks", font_scale=1.5)
sns.set_palette(["black", "black"])
marker_styles = {'Big Bloom': 's', 'Small Bloom': '<', "No Bloom" :"o"}
fig = plt.subplots(figsize = (10, 7), dpi = 300)
sns.lineplot(df, x = "Year", y = "Mean", hue = "Time", markersize = 8,
             marker = "o", linestyle = "--", legend = False)

plt.xticks(list(range(1998, 2024)), rotation = 90, size = 15)
plt.xlim([1997.8, 2023.2])
#plt.ylim([0.7, 1.1])
plt.ylabel("Mean Chla Concentration (mg m$^{-3}$)")
plt.savefig('temp.png', transparent=True)

#%%

#mannkendal tests
#Info about this in SST_analysis_f.py
b_ytrend = mk.original_test(df["Mean"][:9])
b_mtrend = mk.original_test(df2["Mean"][:108])
a_ytrend = mk.original_test(df["Mean"][9:])
a_mtrend = mk.original_test(df2["Mean"][108:])
al_ytrend = mk.original_test(df["Mean"][15:])
al_mtrend = mk.original_test(df2["Mean"][180:])

print(b_ytrend, b_mtrend) #both increasing trends
print(a_ytrend, a_mtrend) # no t significnat decreasing trend
print(al_ytrend, al_mtrend) #siginifcant decreasing trends

np.median(df["Year"][:9]) #2002 median year of before index = 4
np.median(df["Year"][9:]) #2015 index = 17
np.median(df["Year"][15:])#2018 index = 20

#%% the trend line is for cosmetic purposes only. 


#polyfit is used to make a l,s linear regression line. 
#(x, y, curve shape (1 = linear), full = True)

befm = df2.loc[:107]
afm = df2.loc[108:]
alm = df2.loc[180:]

befy = df.loc[:8]
afy =df.loc[9:]
aly = df.loc[15:]

#USE MONTHLY
#BEFORE 2007
m1, c1, *_ = np.polyfit(befm["Year"], befm["Mean"], 1, full=True)
fit1 = np.poly1d(m1)

#AFTER 2007
m2, c2, *_ = np.polyfit(afm["Year"], afm["Mean"], 1, full=True)
fit2 = np.poly1d(m2)

#AFTER BIG BLOOMS
m3, c3, *_ = np.polyfit(alm["Year"], alm["Mean"], 1, full=True)
fit3 = np.poly1d(m3)


#%%
#ALL TRENDS PLOTTED OVER MONTHLY DATA
pal = ["#8f2662", "#8eb840", "#78c9b4"]
df2["BTrend"] = fit1(df2["Year"])
fig, ax = plt.subplots(figsize = (15, 9), dpi = 300)
sns.set_theme(style = "ticks", font_scale=1.7)
sns.lineplot(data = df2, x = "Year", y = "Mean", hue = "Time",
             linestyle = "--",marker = "o",legend = False, palette = ["black", "black"])
plt.plot(befm["Year"], fit1(befm["Year"]), color = pal[0], linewidth = 4, label = "Before 2007")
plt.plot(afm["Year"], fit2(afm["Year"]), color = pal[1],linestyle = "--", linewidth = 4, label = "After 2007")
plt.plot(alm["Year"], fit3(alm["Year"]), color = pal[2], linewidth = 4, label = "After Large Blooms")

plt.legend()
plt.xticks(list(range(1998, 2025)), rotation = 90, size = 20)
plt.xlim([1997.8, 2023.2])
plt.ylim([0.3, 1.8])
plt.yticks(np.arange(0.3, 1.9, 0.1), size = 20)

plt.ylabel(" ")
plt.xlabel(" ")
plt.show()


#%%

#each trend on a smaller graph to add to the big one
dfs = [befy, afy, aly]
fits = [fit1, fit2, fit3]
for r in range(3):
    d = dfs[r]
    f = fits[r]
    fig, ax = plt.subplots(figsize = (6,6), dpi = 300)
    if r == 1:
        plt.plot(d["Year"], f(d["Year"]), color = pal[r], linestyle = "--")
    else:
        plt.plot(d["Year"], f(d["Year"]), color = pal[r])
            
    plt.scatter(d["Year"], d["Mean"], color = "black")

    plt.xticks(d["Year"], rotation = 90)
    plt.ylim([0.6, 1.1])
    plt.show()
    
    
#%%

#Graphs of extrapolated trend:

sizes = []
big_list = [2009, 2013, 2014, 2015, 2016, 2019, 2021, 2022, 2023]
for index, row in df.iterrows():
    if df["Year"][index] < 2007:
        sizes.append("No Bloom")
    elif df["Year"][index] in big_list:
        sizes.append("Large Bloom")
    else:
        sizes.append("Small Bloom")

df["Size"] = sizes
sns.set_palette(pal)
fig, ax = plt.subplots(figsize = (10,8), dpi = 300)
marker_styles = {'Large Bloom': 's', 'Small Bloom': '<', "No Bloom" :"o"}
sns.scatterplot(df, x = "Year", y = "Mean", style = "Size", 
                markers=marker_styles, color = "black", s= 100)
sns.lineplot(x = df["Year"][:10], y = fit1(df["Year"][:10]), label = "Before 2007")
sns.lineplot(x = list(range(2007,2024)), y = fit1(list(range(2007,2024))), linestyle = "--", color = pal[0])
sns.lineplot(x = list(range(2007, 2031)), y = fit2(list(range(2007, 2031))), 
             linestyle = "--", color = pal[1], label = "After 2007")
plt.xticks(list(range(1998, 2025)), rotation = 90)
plt.xlim([1997.8, 2023.4])
plt.yticks(np.arange(0.6, 1.4, 0.1))
plt.ylabel("Mean Chla Concentration (mg m$^{-3}$)")
plt.show()

fig, ax = plt.subplots(figsize = (10,8), dpi = 300)
sns.scatterplot(df.loc[9:], x = "Year", y = "Mean", style = "Size", 
                markers=marker_styles, color = "black", s= 100)
sns.lineplot(x = list(range(2007, 2031)), y = fit2(list(range(2007, 2031))), 
             linestyle = "--", color = pal[1], label = "After 2007")
sns.lineplot(x = list(range(2007, 2024)), y = fit3(list(range(2007, 2024))), 
             linestyle = "-", color = pal[2], label = "After Large Bloom")
sns.lineplot(x = list(range(2007, 2031)), y = fit3(list(range(2007, 2031))), 
             linestyle = "--", color = pal[2])
plt.legend()
plt.xticks(list(range(2007, 2031)), rotation = 90)
plt.xlim([2006.8, 2030.2])
plt.yticks(np.arange(0.6, 1.2, 0.1))
plt.ylabel("Mean Chla Concentration (mg m$^{-3}$)")
#minimum mean was 0.73462154
#following the rend line , lowest levels that were seen in 1999 will be reached at:
#0.73462154 = mx +c
#x = (0.73 - c)m

#reached in 2038 for after 2007
#reached in 2026 for after large bloom. 
#reached in 2023 for no blooms: 
#stats.linregress(bef["Year"], bef["Mean"])
(0.01746 * 2023)-34.2725 #would reach 1.01 levels on 2023.

df.to_csv("chla_saved.csv", index = False) #save means as csv for use in SST