#Code to read Sajjad json values

import json
import pandas as pd
import pickle

with open('data/station_list_sajjad.json') as jsonfile:
        json_data = json.load(jsonfile)

code_lis = []
lat_lis = []
lon_lis = []
for ii in json_data['features']:
	if ii['geometry'] is not None:
		code_lis.append(ii['properties']['code'])
		lat_lis.append(ii['geometry']['coordinates'][1])
		lon_lis.append(ii['geometry']['coordinates'][0])

temp_dict = {'code':code_lis, 'latitude': lat_lis, 'longitude': lon_lis }

df = pd.DataFrame(temp_dict)
df2 = pickle.load(open('data/full_alt_stat_codes.p', 'rb'))
indexed_df2 = df2.set_index([range(len(df2))])

for nr,ii in enumerate(indexed_df2.code.values):
	aa = df[df.code == ii]
	if len(aa.index) > 0:
		indexed_df2.set_value(nr,'lat',aa.latitude.values[0])
		indexed_df2.set_value(nr,'lon',aa.longitude.values[0])

pickle.dump(indexed_df2,open('data/full_lat_lon_stat_code.p', 'wb'))