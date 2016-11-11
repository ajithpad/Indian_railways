#Code to crawl through all the jsons of train routes and store the train departure times for each station

import numpy as np
import json
from collections import defaultdict
import pickle


#Get the station codes
# stat_codes = np.load("data/alt_stat_codes.npy")
stat_codes = pickle.load(open("data/full_alt_stat_codes.p", "rb"))
stat_codes = stat_codes.code.values
stat_codes = stat_codes.tolist()
dep_times = {k: [] for k in stat_codes}


#Function to get the train numbers
def get_route(train_no):
    with open('data/route_json/route_of_'+train_no+'.json') as jsonfile:
        json_data = json.load(jsonfile)
    return json_data

#Go through the trains
train_num = np.load('data/train_num.npy')

for ii in train_num:
    data = get_route(ii)
    route = data['route']
    num_days = np.zeros(7)
    for ii in range(7): 
        if data['train']['days'][ii]['runs'] == 'Y': 
            num_days[ii] = 1
        else:
            num_days[ii] = 0
    valid_ind_val = np.where(num_days > 0)[0]
    base_time = valid_ind_val * 24 * 60
    week_min = 7*24*60
    for ii in route[:-1]:
        if len(ii['schdep']) == 5:
            schdep = (int(ii['schdep'][:2]) * 60) + int(ii['schdep'][3:]) 
            tra_time = ((ii['day']-1) * 24 * 60) + schdep
            arr_dep_sta = np.mod((base_time + tra_time),week_min)
            lis_dep_sta = arr_dep_sta.tolist()
            dep_times[ii['code']] = dep_times[ii['code']]+ lis_dep_sta 
            
name_zero_codes = np.load("data/name_zero_codes.npy")
# non_zero_codes = pickle.load(open("data/non_zero_codes.p","rb"))
non_zero_codes = pickle.load(open("data/full_lat_lon_stat_code.p","rb"))


times = []
num_deps = []
for row in non_zero_codes['code']:
    dep_times[row].sort()
    xx = dep_times[row]
    times.append(xx)
    num_deps.append(len(xx))

non_zero_codes['times'] = times 
non_zero_codes['num_deps'] = num_deps

pickle.dump(non_zero_codes,open("data/full_dep_times_lat_lon.p","wb"))
        
            
        
    

