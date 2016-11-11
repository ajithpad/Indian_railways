#Code to extract the train numbers and save as a text file
import csv
import numpy as np


# Get the list of Indian trains with their numbers
with open('/Users/ajith/bigdata/git_codes/Indian_railway/data/isl_wise_train_detail_03082015_v1.csv', 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    print reader.next()
    train_num = [int(row[0][1:-1]) for row in reader]
    
train_num = np.unique(np.array(train_num))

train_lis = []

for ii in train_num:
    if len(str(ii)) == 3:
        train_lis.append('00'+str(ii))
    elif len(str(ii)) == 4:
        train_lis.append('0'+str(ii))
    else:
        train_lis.append(str(ii))
        
np.save('data/train_num', train_lis)
