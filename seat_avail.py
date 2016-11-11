# Seat Availability calculation code

import urllib2
import json
import pylab as pl
import pandas as pd
import seaborn as sbn

#Use pandas to create timestamp data and change them into strings in the format that is needed

datelist = pd.date_range(pd.datetime(2016,6,15), periods=21).tolist()
weekday_lis = [pd.datetime.weekday(ii) for ii in datelist]

day_str_lis = []
for ii in datelist:
    day_str = ii.date().day
    if len(str(day_str)) < 2:
        day_str = '0' + str(day_str)
        day_str_lis.append(day_str)
    else:
        day_str_lis.append(str(day_str))

month_str_lis = []
for ii in datelist:
    month_str = ii.date().month
    if len(str(month_str)) < 2:
        month_str = '0' + str(month_str)
        month_str_lis.append(month_str)
    else:
        month_str_lis.append(str(month_str))

year_str_lis = [str(ii.date().year) for ii in datelist]

# Concatenate the strings to get the date in the appropriate format
conc_str = ['%s-%s-%s' % t for t in zip(day_str_lis,month_str_lis,year_str_lis)]


#Get the available seats and store as a list
avail_lis = []
for ii in conc_str:
    api_str = "http://api.railwayapi.com/check_seat/train/22649/source/MAS/dest/ED/date/" + ii + "/class/SL/quota/GN/apikey/dnsdx7015/"
    api = urllib2.urlopen(api_str)
    data = json.load(api)
    avail = data['availability'][0]['status']
    if "AVAILABLE" in avail:
        avail_lis.append(int(avail.split('AVAILABLE ')[1]))
    else:
        avail_lis.append(0)
    
#fig = pl.figure(1)
#ax1 = fig.add_subplot(111)
#ax1.plot(range(len(avail_lis)),avail_lis)
#ax1.set_xticks(range(len(avail_lis)))
#ax1.set_xticklabels(conc_str, rotation = 50)
#pl.show()


#Find the days of the week and see the relative occupancy of trains over the weekends

avail_df = pd.DataFrame(np.array(zip(weekday_lis,avail_lis)))
avail_df.columns = ['day', 'avail_tk']
avail_df.hist('day', weights = avail_df['avail_tk'], bins = range(8))