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
arr_times = {k: [] for k in stat_codes}


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
        if len(ii['scharr']) == 5:
            scharr = (int(ii['scharr'][:2]) * 60) + int(ii['scharr'][3:]) 
            tra_time = ((ii['day']-1) * 24 * 60) + scharr
            arr_arr_sta = np.mod((base_time + tra_time),week_min)
            lis_arr_sta = arr_arr_sta.tolist()
            arr_times[ii['code']] = arr_times[ii['code']]+ lis_arr_sta 
            
name_zero_codes = np.load("data/name_zero_codes.npy")
# non_zero_codes = pickle.load(open("data/non_zero_codes.p","rb"))
non_zero_codes = pickle.load(open("data/full_lat_lon_stat_code.p","rb"))


times = []
num_arrs = []
for row in non_zero_codes['code']:
    arr_times[row].sort()
    xx = arr_times[row]
    times.append(xx)
    num_arrs.append(len(xx))

non_zero_codes['times'] = times 
non_zero_codes['num_arrs'] = num_arrs

pickle.dump(non_zero_codes,open("data/full_arr_times_lat_lon.p","wb"))
        
            
        
    

