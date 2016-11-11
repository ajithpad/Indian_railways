#Convert a pickle of departure times based on codes to one based on times
import pickle
import pandas as pd
import json

dis_trains = pickle.load(open("data/full_arr_times_lat_lon.p","rb"))


stat = dis_trains.code.values
dep = dis_trains.times.values
time_dict = dict.fromkeys(range(10080))

for ii in range(10080):
	stat_lis = []
	for jj,kk in enumerate(stat):
		if ii in dep[jj]:
			stat_lis.append(kk)
	time_dict[ii] = stat_lis

with open("data/times_stat_arr.json","w") as outfile:
	json.dump(time_dict, outfile, indent = 0, separators=(',', ':'))







