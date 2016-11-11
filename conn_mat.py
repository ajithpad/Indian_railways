#Code to make connectivity matrix

import pickle
import numpy as np

stat_all_train = pickle.load(open("data/train_stat_dict.p","rb"))

dis_trains = pickle.load(open("data/dep_times_lat_lon.p","rb"))

stat_code = dis_trains.code.values

conn_arr = np.zeros((len(stat_code), len(stat_code)))

for ii, stat_code_1 in enumerate(stat_code):
    for jj, stat_code_2 in enumerate(stat_code):
        set_1 = set(stat_all_train[stat_code_1])
        set_2 = set(stat_all_train[stat_code_2])
        if ii == jj:
            conn_arr[ii,jj] = 0
        else:    
            conn_arr[ii,jj] = len(set_1.intersection(set_2))
            
pickle.dump(conn_arr,open('data/conn_arr.p',"wb")) 