#Code to save JSON files that correspond to the routes of all the trains in a separate folder

import urllib2
import json
import pylab as pl
import numpy as np
import pickle
from os.path import isfile


df = pickle.load(open('data/non_zero_codes.p','rb'))

# df = df[3400:3405]
uu = range(len(df))
df = df.set_index([uu])

for ii in range(len(df)):
	lat = df.lat[ii]
	lon = df.lon[ii]
	if type(lat) is float:
		name = df.code[ii]
		if not isfile("data/stat_json/"+name+"_details.json"):
			api_str = "http://www.datasciencetoolkit.org/coordinates2statistics/"+str(lat)+"%2c"+str(lon)
			api = urllib2.urlopen(api_str)
			data = json.load(api)
			with open("data/stat_json/"+name+"_details.json",'w') as outfile:
			    json.dump(data,outfile)