# Code to map the routes that pass through a station

import pickle
import numpy as np
import pandas as pd
import json
from os.path import isfile
from more_itertools import unique_everseen as uese

import time
start_time = time.time()


train_num = np.load('data/train_num.npy')

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

# Function to get the list of all the stations, lat and lon in a given train
def get_route_st(train_no):
    with open('data/route_json/route_of_'+train_no+'.json') as jsonfile:
        json_data = json.load(jsonfile)
	data = json_data['route']
	st_lis = []
	lat_lis = []
	lon_lis = []
	for jj in data:
		if jj['route'] == 1:
			st_lis.append(jj['code'])
			lat_lis.append(jj['lat'])
			lon_lis.append(jj['lng'])
    return st_lis, lat_lis, lon_lis

#Average speed of a train between station 1 and station 2
def train_speed(train_no, stat_1, stat_2):
	with open('data/route_json/route_of_'+train_no+'.json') as jsonfile:
		json_data = json.load(jsonfile)
	data = json_data['route']
	st_lis,_,_ = get_route_st(train_no)
	st_val_1 = st_lis.index(stat_1)
	st_val_2 = st_lis.index(stat_2)
	if st_val_1 < st_val_2:
	# st_val = np.sort([st_1_val, st_2_val])
		st_schdep = (int(data[st_val_1]['schdep'][:2]) * 60) + int(data[st_val_1]['schdep'][3:]) 
		st_tra_time = ((data[st_val_1]['day']-1) * 24 * 60) + st_schdep
		en_schdep = (int(data[st_val_2]['scharr'][:2]) * 60) + int(data[st_val_2]['scharr'][3:]) 
		en_tra_time = ((data[st_val_2]['day']-1) * 24 * 60) + en_schdep
		tot_time = en_tra_time - st_tra_time
		speed = ((data[st_val_2]['distance'] - data[st_val_1]['distance']) /float(tot_time))*60
		return speed
	else:
		return 0 

#Function to save the list of all the stations reached by all the trains with the number and code
def pickle_df_nr_route():
	route_st_lis = []
	df = pd.DataFrame(columns = ['number', 'code'])	
	for ii in train_num:
		route_st,_,_ = get_route_st(ii)
		df1 = pd.DataFrame({'number':[ii]*len(route_st),'code':route_st})
		df = df.append(df1, ignore_index = True)
	pickle.dump(df,open("data/number_code.p","wb"))

if not isfile("data/number_code.p"):
	pickle_df_nr_route()

df = pickle.load(open("data/number_code.p","rb"))
#Function that returns the station, lat and lon list of all the stations in all the trains passing through a station
def get_all_route_stat(code):	
	stat_det = df[df.code.values == code]
	route_lis = []
	lat_lis = []
	lon_lis = []
	for ii in stat_det.number.values:
		route, lat, lon = get_route_st(ii)
		route_lis.append(route)
		lat_lis.append(lat)
		lon_lis.append(lon)
	return route_lis, lat_lis, lon_lis


# Function to get the unique list of all stations connected to the given station
def unq_all_station(code):
	st_lis,_,_ = get_all_route_stat(code)
	lis = [item for sublist in st_lis for item in sublist]
	unq_lis = np.unique(lis)
	return unq_lis

#Function to get the train numbers passing through a station
def stat_train(code):
	stat_det = df[df.code.values == code]
	return stat_det.number.values

# Function to get the dict of lists of all the connections from a station 
# long_fl = 0 gives only the unique routes to a place
# long_fl = 1 gives the longest route to a place

def get_all_unq_route(code, long_fl = 0):
	unq_lis = unq_all_station(code)
	stat_tr = stat_train(code)
	dict_lis = {k: [] for k in unq_lis}
	for jj in unq_lis:
		for ii in stat_tr:
			st_ord,_,_ = get_route_st(ii)
			if jj in st_ord and code in st_ord:
				st_val = st_ord.index(code)
				end_val = st_ord.index(jj)
				if st_val < end_val:
					ind_val = [st_val, end_val]
					ind_val.sort()
					fin_lis = st_ord[ind_val[0]:ind_val[1]+1]
					# fin_lis.remove(code)
					# if len(fin_lis) > 1:
					dict_lis[jj].append(fin_lis)  
		# if len(dict_lis[jj]) > 1:
		temp_tup = [tuple(l) for l in dict_lis[jj]]
		temp_lis = list(uese(temp_tup))
		dict_lis[jj] = [list(l) for l in temp_lis]
		if long_fl == 1:
			if len(dict_lis[jj]) > 0:
				length = len(max(dict_lis[jj], key = len))
				dict_lis[jj] = [x for x in dict_lis[jj] if len(x) == length]
	return dict_lis

def save_unq_route(code):
	xx = get_all_unq_route(code, long_fl = 1)
	name = "data/unq_route/unq_route_"+code+".p"
	pickle.dump(xx, open(name,"wb"))


# Code to save the final routes originating from a given station
def save_fin_route(code):
	name = "data/unq_route/unq_route_"+code+".p"
	if not isfile(name):
		save_unq_route(code)
	xx = pickle.load(open(name,"rb"))
	unq_lis = unq_all_station(code)
	route_lis = []
	for ii in unq_lis:
		for temp in xx[ii]:
			route_lis.append(temp)


	sorted_rte = sorted(route_lis, key = len)
	rem_lis = sorted_rte[:]
	fin_lis = []
	for val,ii in enumerate(sorted_rte):
		check_set = set(ii)
		rem_lis.pop(0)
		num =0
		for jj in rem_lis:
			if check_set.issubset(set(jj)):
				num += 1
		if num == 0:
			fin_lis.append(sorted_rte[val])
	fil_name = "data/fin_route/fin_route_"+code+".p"
	pickle.dump(fin_lis, open(fil_name,"wb"))

# code ='DMM'
# if not isfile("data/fin_route/fin_route_"+code+".p"):
# 	save_fin_route(code)


def get_speed_dis(stat_1, stat_2):
	unq_1 = stat_train(stat_1)
	unq_2 = stat_train(stat_2)
	unq_1 = unq_1.tolist()
	unq_2 = unq_2.tolist()
	fin_unq = list(set(unq_1).intersection(set(unq_2)))
	speed_lis = []
	for ii in fin_unq:
		speed = train_speed(ii, stat_1, stat_2)
		speed_lis.append(speed)
	speed_lis = np.array(speed_lis)
	speed_arr = speed_lis[speed_lis != 0]
	#The following line is to ward off problems that arise due to change in days when stations are crossed. Change it later
	speed_arr = speed_arr[speed_arr > 10]
	return speed_arr

def unq_fin_unq_route(code):
	name = "data/unq_route/unq_route_"+code+".p"
	# name = "data/fin_route/fin_route_"+code+".p"
	if not isfile(name):
		save_fin_route(code)
	fin_lis = pickle.load(open(name, "rb"))
	lis_lis = fin_lis.values()
	lis_lis = [x for ii in lis_lis for x in ii]
	main_lis = []

	join_lis = [1,1]
	#Chunk to find different chunks of disjoint sets
	nr = 0
	while len(lis_lis) > 1:
		join_lis = []
		nr_lis = []
		ii = lis_lis[nr]
		for nr_jj,jj in enumerate(lis_lis):
			if len(set(ii[1:]).intersection(jj[1:])) != 0:
				join_lis.append(jj)
				nr_lis.append(nr_jj)
		lis_lis = [ item for i,item in enumerate(lis_lis) if i not in nr_lis]
		main_lis.append(join_lis)
	if len(lis_lis) == 1:
		main_lis.append([lis_lis[0][1:]])

	#To group the subsets together in each route
	big_big_lis = []
	sort_lis = [sorted(ii, key = len, reverse = True) for ii in main_lis]
	for ii in sort_lis:
		sup_lis = ii[:]
		nr = 0
		big_lis = []
		if len(sup_lis) > 1:
			while len(sup_lis) > 1:
				temp_lis = []
				nr_lis = []
				comp = sup_lis[nr]
				for nr_jj,jj in enumerate(sup_lis):
					if set(jj).issubset(comp):
						nr_lis.append(nr_jj)
						temp_lis.append(jj)
				un_lis = max(temp_lis, key = len)
				sup_lis = [item for i,item in enumerate(sup_lis) if i not in nr_lis]
				big_lis.append(un_lis)
			big_big_lis.append(big_lis)
		else:
			big_big_lis.append(sup_lis)
	fin_lis = []
	for ii in big_big_lis:
		fin_lis+=ii

	return fin_lis

# Returns the routes emerging from a station in a matrix form
def get_sta_conn_mat(code):
	routes = unq_fin_unq_route(code)
	flat_lis = [item for sublist in routes for item in sublist]
	unq_lis = list(set(flat_lis))
	conn_mat = pd.DataFrame(np.zeros((len(unq_lis), len(unq_lis))), index = unq_lis, columns = unq_lis)
	for ii in routes:
		if len(ii) > 1:
			coup_lis = []
			for jj in range(0,len(ii)-1):
				coup_lis.append([ii[jj],ii[jj+1]])
				for kk in coup_lis:
					conn_mat[kk[0]][kk[1]]+=1 

	adj_mat = (conn_mat >= 1)*1 
	# fil_name = 'adj_mat_'+ code + '.p'
	# path = 'data/adj_mat/'+fil_name 
	# if not isfile(path):
	# 	pickle.dump(adj_mat,open(path,"wb")) 

	adj_dict = dict.fromkeys(unq_lis)
	for ii in unq_lis:
		adj_dict[ii] = adj_mat.loc[adj_mat[ii] == 1].index.tolist()

	fil_name = 'adj_dict_'+ code + '.p'
	path = 'data/adj_mat/'+fil_name 
	if not isfile(path):
		pickle.dump(adj_dict,open(path,"wb")) 

	return adj_mat, adj_dict


#A function that returns the number of trains given the code for the three stations
#through which the trains pass.
def train_num_3_station(stat_1, stat_2, stat_3):
	stat_det = df[df.code.values == stat_1]	
	aa = df[df.number.isin(stat_det.number)]
	stat_det_2 = aa[aa.code.values == stat_2]
	bb = df[df.number.isin(stat_det_2.number)]
	stat_det_3 = bb[bb.code.values == stat_3] 
	return stat_det_3.number.values,len(stat_det_3)


def create_json_all_routes():
	stat_arr = np.load("data/full_alt_stat_codes.npy")
	stat_name = stat_arr[:,0][1000:1002]

	tot_dict = {}
	for ii in stat_name:
		fil_name = "data/adj_mat/"+ii + '.p'
		if not isfile(fil_name):
			_,conn_sta = get_sta_conn_mat(ii)
		else:
			_,conn_sta = pickle.load(open(fil_name, "rb"))
		tot_dict[ii] = dict.fromkeys(conn_sta.keys())
		for jj in conn_sta.keys():
			temp_lis = []
			for kk in conn_sta[jj]:
				_,num_train = train_num_3_station(ii,jj,kk)
				temp_lis.append({'code':kk, 'numtrain':num_train})
			tot_dict[ii][jj] = temp_lis

	pickle.dump(tot_dict, open('data/all_conn_mat_num_train.p', 'wb'))
	with open("data/conn_mat_num_train_1000_1002.json","w") as outfile:
		json.dump(tot_dict, outfile, indent = 0, separators=(',', ':'))

print("--- %s seconds ---" % (time.time() - start_time))

















