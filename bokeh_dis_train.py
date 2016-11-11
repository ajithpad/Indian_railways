#Code to use bokeh to plot the distribution of trains for a given station across the week

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

dummy_ = pd.DataFrame()
dummy_['vals'] = range(0,10080,1440)
dummy_['names'] = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
dummy_['y_vals'] = [-1]*7

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
    fig = figure(x_range = (0,10080), y_range = (0,max(hist+1)))    
    d = np.sin(3*gradient)
    fig.image(image = [d],x = 0, y = 0, dw = 10080, dh = max(hist)+1)
    fig.quad(top=hist, bottom=0, left=edges[:-1],right=edges[1:],fill_color="#036564",line_color="#033649")
    fig.xaxis[0].ticker=FixedTicker(ticks=[])
    fig.xaxis.major_label_orientation = "vertical"
    output_file("test_bg_image.html", title = "Background image")
    show(fig)
    return hist,edges
