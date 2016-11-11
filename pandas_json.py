#Code to convert a given pandas file to a json file

import pandas as pd
import pickle 
import json

df = pickle.load(open('data/full_arr_times_lat_lon.p', 'rb'))
xf = df[df.lat != '']
temp_lis = []

temp_dict = {}
for index, row in xf.iterrows():
	# temp_key = str(row['code'])
	temp_dict = {}
	temp_dict['code'] = str(row['code'])
	temp_dict['name'] = str(row['name'])
	temp_dict['coordinates'] = [row['lat'], row['lon']]
	temp_dict['times'] =  row['times']
	temp_dict['num_arrs'] = row['num_arrs']
	temp_lis.append(temp_dict)

with open("data/ed_full_station_info_arr.json","w") as outfile:
	json.dump(temp_lis, outfile, indent = 0, separators=(',', ':'))
