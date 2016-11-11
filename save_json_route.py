#Code to save JSON files that correspond to the routes of all the trains in a separate folder

import urllib2
import json
import pylab as pl
import numpy as np

train_num = np.load('data/train_num.npy')

for ii in train_num:
    api_str = "http://api.railwayapi.com/route/train/" +ii+"/apikey/dnsdx7015/"
    api = urllib2.urlopen(api_str)
    data = json.load(api)
    with open('data/route_json/route_of_'+ii+'.json','w') as outfile:
        json.dump(data,outfile)