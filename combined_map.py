#Code to use bokeh and gmplot and plot all the stations in India

from bokeh.io import output_file, show
from bokeh.models import (GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool)
from bokeh.models import HoverTool, ResetTool,TapTool
import pickle
from bokeh.charts import Scatter
import matplotlib as mpl

#lat_lon_df = pickle.load(open("data/non_zero_codes.p","rb"))
lat_lon_df = pickle.load(open("data/dep_times_lat_lon.p","rb"))

#lat_lon_df = lat_lon_df.ix[:,['lat','lon']]


map_options = GMapOptions(lat=23.29, lng=78.73,map_type="roadmap", zoom=4)


col_vals = lat_lon_df['num_deps'].values

colors = [
    "#%02x%02x%02x" % (int(r), int(g), int(b)) for r, g, b, _ in 255*mpl.cm.Blues(mpl.colors.Normalize()(col_vals))
]
lat_lon_df['col_vals'] = colors

plot = GMapPlot(
    x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, title="India"
)

source = ColumnDataSource(lat_lon_df)

#circle = Circle(x="lon", y="lat", size=5, fill_color="blue", fill_alpha=0.7, line_color=None)
circle = Circle(x ='lon', y = 'lat',size = 5, fill_color = 'col_vals')

plot.add_glyph(source, circle)

plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool(), HoverTool(tooltips = [('name','@name'),('No. of deps/week', '@num_deps'),('Code','@code')]),ResetTool(),TapTool())

import pickle
import numpy as np
from bokeh.charts import Bar, output_file, show, Dot
import pylab as pl
import seaborn as sbn
from bokeh import mpl as mpl
from bokeh.io import output_notebook, show
from bokeh.plotting import figure, show, output_file
from bokeh.models import FixedTicker, TickFormatter
import pandas as pd


dis_trains = pickle.load(open("data/dep_times_lat_lon.p","rb"))

gradient = []
for ii in range(7):
    gradient += range(25)
    
gradient = np.array(gradient)
gradient = gradient/24.
gradient = gradient.reshape(1,-1)

fig = figure(x_range = (0,10080), y_range = (0,16))

def get_trains_week(stat_code): 
    sbn.set_style("white")
    stat_vals = dis_trains[dis_trains.code == stat_code]
    all_trains = stat_vals.times.values
    xx = all_trains
    days = np.array(xx[0])/1440
    tot_mins = np.array(xx[0])%1440
    hour = tot_mins/60
    mins = tot_mins % 60
    train_time = zip(days,hour,mins)
    hist, edges = np.histogram(xx[0], bins = range(0,10081,120))    
    d = np.sin(3*gradient)
    fig.image(image = [d],x = 0, y = 0, dw = 10080, dh = max(hist)+1)
    fig.quad(top=hist, bottom=0, left=edges[:-1],right=edges[1:],fill_color="#036564",line_color="#033649")
    fig.xaxis[0].ticker=FixedTicker(ticks=[])
    fig.xaxis.major_label_orientation = "vertical"
#    output_file("test_bg_image.html", title = "Background image")
    show(fig)
    
plot.on_change('selected',get_trains_week)
