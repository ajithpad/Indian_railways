# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 10:11:51 2016

@author: ajith
"""

# Code to perform the degree distribution and other complex network calculations

import pickle
import pylab as pl
import seaborn as sbn
import numpy as np
#from bokeh.charts import scatter
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, HoverTool,PanTool, WheelZoomTool, BoxSelectTool
import pandas as pd
import matplotlib as mpl

conn_arr = pickle.load(open("data/conn_arr.p","rb"))

fig = pl.figure(1)
ax1 = fig.add_subplot(111)
def deg_dis(conn_arr, plot_fl = 1):
    deg = np.sum((conn_arr > 0)*1, axis = 0)
    if plot_fl:
        ax1.hist(deg, bins = range(0,1001, 20), alpha = 0.5)
        
deg_dis(conn_arr)
pl.show()
def degVsweight(conn_arr, plot_fl = 1):
    deg = np.sum((conn_arr > 0)*1, axis = 0)
    weight = np.sum(conn_arr, axis = 0)
#    ax1.plot(deg,weight, 'o',markersize = 5.,  color = 'green')
    return deg, weight

deg, weight = degVsweight(conn_arr)
data_dict = {}
data_dict['deg'] = deg.tolist()
data_dict['weight'] = weight.tolist()
dis_trains = pickle.load(open("data/dep_times_lat_lon.p","rb"))
st_name = dis_trains.name.values
st_name = st_name.tolist()
data_dict['name'] = st_name



st_code = dis_trains.code.values
st_code = st_code.tolist()
data_dict['code'] = st_code

lat = dis_trains.lat.values
lat = lat.tolist()
data_dict['lat'] = lat
df = pd.DataFrame(data_dict)

df = df[df.lat.values != '']
col_vals = df.lat.values
colors = [
    "#%02x%02x%02x" % (int(r), int(g), int(b)) for r, g, b, _ in 255*mpl.cm.RdBu(mpl.colors.Normalize()(col_vals))
]

df['col_vals'] = colors

p = figure(title="Degree Vs Weight")
source = ColumnDataSource(df)
p.circle('deg', 'weight', source = source, size = 7, fill_alpha = 0.5, color = 'col_vals')
p.add_tools(HoverTool(tooltips = [('name','@name'),('Code', '@code')]))


output_file("figures/degVsWeight.html", title="Degree vs Weight")
show(p)
#pl.show()
