#Code to make a raster of all the trains and plot the histogram of trains in India

import pickle
import pylab as pl
import pandas as pd
import numpy as np
import seaborn as sbn

df = pickle.load(open("data/dep_times_lat_lon.p","rb"))
ef = df.reset_index()
# ef['ind_val'] = pd.Series(ef.index.values)
tot = {'code':[], 'lat':[],'lon': [], 'name':[],'num_deps':[], 'times':[], 'ind_val':[]}

for ii,row in enumerate(df.values):
    tot['code']+=([row[0]] * row[-1])
    tot['lat']+=([row[1]] * row[-1])
    tot['lon']+=([row[2]] * row[-1])
    tot['name']+=([row[3]] * row[-1])
    tot['times']+=row[4]
    tot['num_deps']+=([row[-1]] * row[-1])
    tot['ind_val']+=([ef.index[ii]]* row[-1])

new_df = pd.DataFrame(tot)

gradient = []
for ii in range(7):
    gradient += range(25)
    
gradient = np.array(gradient)
gradient = gradient/24.
gradient = gradient.reshape(1,-1)

fig = pl.figure(1)
ax1 = fig.add_subplot(111)

sbn.set_style("white")
aa,bb = np.histogram(tot['times'], bins = range(0,10081,120))
ax1.hist(tot['times'], bins = range(0,10081,120), alpha = 0.3, color = 'green')
# sbn.distplot(tot['times'], hist = False)
ax1.imshow(0.3*np.sin(3*gradient), extent=[0, 10080, 0, 4000], aspect='auto', cmap='gray')
ax1.set_xlim(0,24*60*7)
ax1.set_xticks(range(0,10081,1440))
ax1.set_xticklabels(['Sun','Mon', 'Tue','Wed','Thu','Fri','Sat'],size = 16, rotation = 90)
ax1.set_ylabel("Number of trains departing", size = 16)
ax1.set_yticks(range(0,4001,1000))
ax1.set_yticklabels(range(0,4001,1000), size = 16)
ax1.grid('off')

pl.show()