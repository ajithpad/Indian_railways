#Code to use bokeh to plot the distribution of trains for a given station across the week

import pickle
import numpy as np
from bokeh.charts import Bar, output_file, show
import pylab as pl
import seaborn as sbn
from bokeh import mpl as mpl
from bokeh.io import output_notebook, show


dis_trains = pickle.load(open("data/dep_times_lat_lon.p","rb"))

gradient = []
for ii in range(7):
    gradient += range(25)
    
gradient = np.array(gradient)
gradient = gradient/24.
gradient = gradient.reshape(1,-1)

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
    fig = pl.figure(2)
    ax1 = fig.add_subplot(111)
    
    aa,bb = np.histogram(xx[0], bins = range(0,10081,120))
    ax1.hist(xx[0], bins = range(0,10081,120), alpha = 0.5)
    ax1.imshow(np.sin(3*gradient), extent=[0, 10080, 0, max(aa)+1], aspect='auto', cmap='gray')
    ax1.set_xlim(0,24*60*7)
    ax1.set_xticks(range(0,10081,1440))
    ax1.set_xticklabels(['Sun','Mon', 'Tue','Wed','Thu','Fri','Sat'],size = 16, rotation = 90)
    ax1.set_ylabel("Number of trains departing", size = 16)
    ax1.set_yticks(range(0,max(aa)+1,2))
    ax1.set_yticklabels(range(0,max(aa)+1,2), size = 16)
pl.show()
