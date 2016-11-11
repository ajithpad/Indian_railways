#Code to find the altitude of all the stations and add it as a column

import geocoder as gc
import pickle
import pandas as pd
import numpy as np
import json

# df = pickle.load(open('data/non_zero_codes.p','rb'))
df = pickle.load(open("data/dep_times_lat_lon.p","rb"))
df = df[df.lat.values != '']
uu = range(len(df))
df = df.set_index([uu])

ele_lis = []
pop_lis = []
for ii in df.code.values:
	name = "data/stat_json/"+ii+"_details.json"
	with open(name) as jsonfile:
		json_data = json.load(jsonfile)
	elev = json_data[0]['statistics']['elevation']['value']
	pop_den = json_data[0]['statistics']['population_density']['value']
	ele_lis.append(elev)
	pop_lis.append(pop_den)

df['altitude'] = pd.Series(ele_lis, index = df.index)
df['popden'] = pd.Series(pop_lis, index = df.index)

pickle.dump(df, open('data/stat_coo_alt_pop.p', 'wb'))
