import numpy as np
import csv
import re
import pylab as pl
import pickle
import station_route_map as srp
from mpld3 import plugins
import mpld3
from sklearn import datasets, linear_model
from pyearth import Earth as earth
from sklearn.svm import SVR


city_name = []
city_pop_2000 = []
city_pop_2010 = []
city_pop_2020 = []
city_lat = []
city_lon = []

with open('/Users/ajith/bigdata/data/indicator_data_IN.csv', 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        if "urban_population_cities" in row:
            if row[-2] == '2000':
                city_name.append(row[-3])
                city_pop_2000.append(int(row[-1]))
                city_lat.append(float(row[-7]))
                city_lon.append(float(row[-6]))
            if row[-2] == '2010':   
                city_pop_2010.append(int(row[-1]))
            if row[-2] == '2020':   
                city_pop_2020.append(int(row[-1]))

# df = pickle.load(open('data/dep_times_lat_lon.p', 'rb'))


stat_code = [['BRC'], ['DDR','DR','CSTM','LTT','BCT','BDTS'], ['KOAA','SDAH','HWH','SHM'], ['RJT','BKNG'], ['BBS'], ['LDH'], ['KOTA','DKNT'], ['SINA'], ['CLT'], ['LC', 'LKO'], ['TATA'],['RNC','HTE','TTS','NKM'],['R'],['JBP'],['INDB'],['SA','SXT'],['AWB'],['SUR'],['NDLS','DLI','NZM','ANVT','DEE'],['HYB','SC','KCG'],['PUNE'],['NGP'],['TUP'],['JP'],['CNB','CPA'],['PNBE','PPTA','RJPB','GZH','DNR','PNC'],['MAS','MS'],['ADI','SBI'],['ST'],['ASN'],['JUC'],['ALD'],['GHY','KYQ'],['TPJ'],['MB'],['VSKP'],['BZA','KI'],['TVC','KCVL'],['ERS','ERN'],['UBL'],['MYS'],['SBC','BNCE','BNC'],['JU'],['BE'],['WL'],['CDG'],['ASR'],['BSB','MUV','MGS','KEI'],['NK'],['DURG','BIA'],['BPL','HBJ'],['MDU'],['CBE','CBF'],['AGC','AF'],['ALJN'],['MTC','MUT'],['DHN'],['GWL'] ]

# stat_code = [['KOAA','SDAH','HWH','SHM']]
num_deps = []
for ii in stat_code:
    all_train = []
    for jj in ii:
        temp = srp.stat_train(jj)
        temp = temp.tolist()
        temp = [int(x) for x in temp]
        all_train+=temp
    all_train = np.unique(all_train)
    all_train = all_train.tolist()
    num_deps.append(all_train)

num_trains = [len(x) for x in num_deps]

test_data = 'data3'

records = np.rec.fromarrays((np.array(city_name), np.array(city_pop_2000),np.array(city_pop_2010),np.array(city_pop_2020), np.array(city_lat),np.array(city_lon), np.array(num_trains)), names=('keys', 'data1', 'data2','data3','lat', 'lon', 'train_num'))
records.sort(order = test_data)
fig2 = pl.figure(2)
ax2 = fig2.add_axes([0.1,0.15,0.8,0.8])

scatter = ax2.scatter(records['train_num'], records[test_data], s = 100., alpha = 0.4, c = records['lat']*20, cmap = pl.cm.RdBu)
ax2.set_xlim(0,30000)
pl.xticks(size = 16)
pl.yticks(size = 16)
pl.ylabel('Number of trains', size = 18)
pl.xlabel('Population in year 2020 in 000s', size = 18)
labels = [i for i in records['keys']]
#fig2.plugins = [plugins.PointLabelTooltip(scatter, labels)]
tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels=labels)
mpld3.plugins.connect(fig2, tooltip)
mpld3.save_html(fig2, 'figures/mpld3_city_analy_check.html')                     

# model = earth()
# regr = linear_model.LinearRegression()



# # svr_poly = SVR(kernel='poly', C=1e2, degree=2)
# model.fit(records[test_data].reshape(-1,1), records['train_num'].reshape(-1,1))

# pl.scatter(records['train_num'], records[test_data], s = 10.)
# pl.plot(records[test_data].reshape(-1,1), model.predict(records[test_data].reshape(-1,1)), lw = 3.)


