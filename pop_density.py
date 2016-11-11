#Code to plot the station density across India

import urllib2
import json
import pylab as pl
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn
from matplotlib.colors import LinearSegmentedColormap, LogNorm, Normalize
from geopy.geocoders import Nominatim
from bokeh import mpl
import pickle


stat_details = pickle.load(open('data/stat_coo_alt_pop.p', 'rb'))
stat_details = stat_details[stat_details.lat.values != '']
sbn.set(style = 'white',font_scale = 2)

def get_route(train_no):
    with open('data/route_json/route_of_'+train_no+'.json') as jsonfile:
        json_data = json.load(jsonfile)
    return json_data


from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
fig3 = pl.figure(3, facecolor = 'white')
ax1 = fig3.add_subplot(111)
map = Basemap(projection='merc', lat_0 = 20, lon_0 = 80,
    resolution = 'h', area_thresh = 1.,
    llcrnrlon=67.0, llcrnrlat=7.0,
    urcrnrlon=96.0, urcrnrlat=37.0)

map.drawmapboundary()
#map.fillcontinents()
map.drawcoastlines()
map.drawcountries()


cdict = {'red':  ( (0.0,  1.0,  1.0),
                   (1.0,  1.0,  1.0) ),
         'green':( (0.0,  1.0,  1.0),
                   (1.0,  0.03, 0.0) ),
         'blue': ( (0.0,  1.0,  1.0),
                   (1.0,  0.0, 0.0) ) }
custom_map = LinearSegmentedColormap('custom_map', cdict)
plt.register_cmap(cmap=custom_map)

sup_lon_lis = stat_details.lon.values
sup_lon_lis = sup_lon_lis.tolist()
sup_lat_lis = stat_details.lat.values
sup_lat_lis = sup_lat_lis.tolist()
db = 1
lon_bins = np.linspace(min(sup_lon_lis)-db, max(sup_lon_lis)+db, 60+1)
lat_bins = np.linspace(min(sup_lat_lis)-db, max(sup_lat_lis)+db, 60+1)

density, _, _ = np.histogram2d(sup_lat_lis, sup_lon_lis, [lat_bins, lon_bins])
density = np.hstack((density,np.zeros((density.shape[0],1))))
density = np.vstack((density,np.zeros((density.shape[1]))))

lon_bins_2d, lat_bins_2d = np.meshgrid(lon_bins, lat_bins)

xs, ys = map(stat_details.lon.values, stat_details.lat.values)

# pl.pcolormesh(xs, ys, density, cmap = custom_map,vmax = 14, shading = 'flat')
ax1.hexbin(x = xs , y = ys , C =stat_details.popden.values, reduce_C_function=np.mean, gridsize = 25, cmap = pl.cm.YlOrBr, bins = 'log')
#pl.contourf(xs,ys,density, cmap = custom_map, vmax = 800)
pl.title('Population density in India')
# pl.colorbar()


# pl.pcolormesh(xs, ys, density, cmap = custom_map,vmax = 40, shading = 'flat')
# #pl.contourf(xs,ys,density, cmap = custom_map, vmax = 800)
# pl.title('Station density in India')
# pl.colorbar()
pl.show()