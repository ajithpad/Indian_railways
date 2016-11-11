#Code to create a dictionary that contains all the trains that arrive at a station

import numpy as np
import pickle
import json

def get_route(train_no):
    with open('data/route_json/route_of_'+train_no+'.json') as jsonfile:
        json_data = json.load(jsonfile)
    return json_data


train_num = np.load('data/train_num.npy')

train_num_dict = {k: [] for k in train_num}

for ii in train_num:
    route = get_route(ii)
    st_lis = []
    for kk in route['route']:
        st_lis.append(kk['code'])
    train_num_dict[ii]+=st_lis
        
    

code_df = pickle.load(open("data/dep_times_lat_lon.p","rb"))

code = code_df.code
code = code.values

train_stat_dict = {k: [] for k in code}

for ii in code:
    temp_tr_lis = []
    for jj in train_num:
        if ii in train_num_dict[jj]:
            temp_tr_lis.append(int(jj))
    train_stat_dict[ii]+=temp_tr_lis
            
pickle.dump(train_stat_dict,open('data/train_stat_dict.p',"wb"))         
            
