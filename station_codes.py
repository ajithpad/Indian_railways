#Code to collect all the station codes and save in a npy file

import numpy as np
import pylab as pl
import csv
import re
import pandas as pd

#Collect all the station names

with open('/Users/ajith/bigdata/git_codes/Indian_railway/data/isl_wise_train_detail_03082015_v1.csv', 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    print reader.next()
    print reader.next()
    stat_code = [row[3] for row in reader]

#Remove all white spaces in the end
stat_code = [re.sub(r'\s+', '', ii) for ii in stat_code]

data = {'name':stat_code}
ser_stat_code = pd.DataFrame(data)

stat_code = ser_stat_code.name.unique()

np.save('data/stat_codes.npy',stat_code)