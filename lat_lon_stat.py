# Code to get the latitude and longitude of all the stations


import numpy as np
import json
import urllib2

stat_codes = np.load("data/alt_stat_codes.npy")
stat_codes = stat_codes.tolist()
lat_lon_arr = np.zeros((len(stat_codes),2))
new_stat_codes = []

#for jj,ii in enumerate(stat_codes):
#    code = ii.lower()
#    api_str = "http://api.railwayapi.com/code_to_name/code/"+code+"/apikey/dnsdx7015/"
#    api = urllib2.urlopen(api_str)
#    data = json.load(api)
##    lat_lon_arr[jj,0] = ii
#    for kk in range(len(data['stations'])):
#        if data['stations'][kk]['code'] == ii:
#            new_stat_codes.append(ii)
#            lat_lon_arr[jj,0] = data['stations'][kk]['lat']
#            lat_lon_arr[jj,1] = data['stations'][kk]['lng']
            
#np.save('data/lat_lon_stat.npy', lat_lon_arr)
#np.save('data/stat_code_check.npy', new_stat_codes)

