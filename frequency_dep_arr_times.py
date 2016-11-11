#Code to bin the departure and arrival times of all the trains across India

import pickle
import numpy as np 
# import seaborn as sbn 
import pylab as pl


df = pickle.load(open('data/full_dep_times_lat_lon.p', 'rb'))

count_0 = 0
count_1 = 0
count_2 = 0
count_3 = 0
count_4 = 0
count_5 = 0 
count_6 = 0
count_7 = 0
count_8 = 0
count_9 = 0
for ii in df.times.values:
	str_vals = [str(jj)[-1] for jj in ii]
	conc_str = ''.join(str_vals)
	count_0 += conc_str.count('0')
	count_1 += conc_str.count('1')
	count_2 += conc_str.count('2')
	count_3 += conc_str.count('3')
	count_4 += conc_str.count('4')
	count_5 += conc_str.count('5')
	count_6 += conc_str.count('6')
	count_7 += conc_str.count('7')
	count_8 += conc_str.count('8')
	count_9 += conc_str.count('9')

pl.plot(range(0,10), [count_0,count_1,count_2, count_3,count_4,count_5,count_6, count_7,count_8, count_9], lw = 4.)
pl.show()


