# Alternative code to generate the station codes from the route jsons

import json
import pandas as pd
import numpy as np
import urllib2
import pickle


def get_route(train_no):
    with open('data/route_json/route_of_'+train_no+'.json') as jsonfile:
        json_data = json.load(jsonfile)
    return json_data

train_num = np.load('data/train_num.npy')
stat_code = []
lat_lis = []
lon_lis = []
name_lis = []

for ii in train_num:
    data = get_route(ii)
    route = data['route']
    for jj in route:
        stat_code.append(jj['code'])
        lat_lis.append(jj['lat'])
        lon_lis.append(jj['lng'])
        name_lis.append(jj['fullname'])

data = {'code':stat_code, 'lat':lat_lis,'lon': lon_lis, 'name':name_lis}
ser_stat_code = pd.DataFrame(data)
unq_stat_code = ser_stat_code.drop_duplicates()
pickle.dump(unq_stat_code,open('data/full_alt_stat_codes.p','wb'))
zero_codes = unq_stat_code[unq_stat_code.lat == 0]
non_zero_codes = unq_stat_code[unq_stat_code.lat != 0]
name_zero_codes = np.array(zero_codes.name)

# np.save("data/name_zero_codes.npy", name_zero_codes)
# pickle.dump(non_zero_codes,open("data/non_zero_codes.p","wb"))

#zero_st_name = []
#lat_zero_lis = []
#lon_zero_lis = []

#for ii in name_zero_codes:
#    low_name = ii.lower()
#    api_str = "http://api.railwayapi.com/code_to_name/code/"+low_name+"/apikey/dnsdx7015/"
#    api = urllib2.urlopen(api_str)
#    api_data = json.load(api)
#    for kk in range(len(api_data['stations'])):
#        if data['stations'][kk]['code'] == ii:
#            zero_st_name.append(ii)
#            lat_zero_lis.append(api_data['stations'][kk]['lat'])
#            lon_zero_lis.append(api_data['stations'][kk]['lng'])

#
#stat_code = ser_stat_code.name.unique()

#np.save('data/alt_stat_codes.npy',stat_code)


# data = {'name':stat_code}
# ser_stat_code = pd.DataFrame(data)

# stat_code = ser_stat_code.name.unique()

# np.save('data/alt_stat_codes.npy',stat_code)
