# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 20:51:19 2024

@author: pippa

Phillippa Edwards

Clean Code for github submission

Univeristy of Plymouth

Graphing an area to use for data analysis using OC-CCI data products,
specifically RMSD from OC-CCI portal.

Mapping style created with help of Dr. Lauren Biermann (UoP) and asking google.

CHLA from OC-CCI database
"""

import netCDF4 as nc
import matplotlib.pyplot as plt
from shapely.geometry.polygon import LinearRing
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import matplotlib
matplotlib.rcParams['font.family'] = 'Arial'
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import xarray as xr
import os
from cmcrameri import cm
os.chdir("C:/Users/pippa/OneDrive/Documents/Uni/Year3/dissi/dissi_code/usethisdata/")
#%%

#input data:
data = xr.open_dataset("RMSD_Data.nc")
chla2 = data["chlor_a_log10_rmsd"]

#lat and lon loaded in
lat_var2 = chla2["lat"]
lon_var2 = chla2["lon"]


print(chla2[68,:,:])
#the day the file is from is. 2011-07-01
#%%
#map
#set fig size
fig = plt.figure(figsize=(20,9), dpi=300)

m = plt.axes(projection=ccrs.PlateCarree(central_longitude=0.0))
#set projection extent
extent = [116.9, 130.1, 31.9, 40.1]
m.set_extent(extent, crs=ccrs.PlateCarree())
#set the colour mesh for the 42 date in file
f = plt.pcolormesh(lon_var2, lat_var2,  chla2[68,:,:],vmin = 0.24, cmap = cm.imola)
m.coastlines(resolution="10m", color='black', linewidth=1)
m.add_feature(cfeature.LAND)
m.add_feature(cfeature.OCEAN)
#grid lines
g1 = m.gridlines(draw_labels = True)
g1.xlabels_top = False
g1.xlabel_style = {'size': 15, 'color': 'gray'}
g1.ylabel_style = {'size': 15, 'color': 'gray'}
cbar = plt.colorbar(orientation="horizontal", fraction=0.05, pad=0.06) 
cbar.set_label('RMSD of log10-transformed chlorophyll-a concentration', fontsize=16)
plt.title("2011-07-01", fontsize = 20)

# Add a box to the map
box_extent = [121.5, 124.75, 35, 36]  # Adjust coordinates as needed
box_polygon = mpatches.Rectangle((box_extent[0], box_extent[2]),
                             box_extent[1] - box_extent[0],
                             box_extent[3] - box_extent[2],
                             edgecolor='white', linewidth=3, facecolor='none', transform=ccrs.PlateCarree())
m.add_patch(box_polygon)

#save and show
plt.savefig("C:/Users/pippa/OneDrive/Documents/Uni/Year3/dissi/dissi_code/usethisdata/map.png")
plt.show()