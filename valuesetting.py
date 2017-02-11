import numpy as np
import csv
import glob
import math

def getDistances(query_file_name):

    matches = []

    files = glob.glob('./data/'+query_file_name+'*.csv')

    print("-----------途中経過-------------")

    i = 0
    count = 0

    distance_list = []
    file_list = []

    for query_file in files:
      query = parseCSV(query_file)

      for file in files:
        data = parseCSV(file)

        if query_file == file: break

        data_len = len(data['ax'])
        distance = 0.0
        #print(file)

        distance += dtw(query['ax'],data['ax'])
        distance += dtw(query['ay'],data['ay'])
        distance += dtw(query['az'],data['az'])
        distance += dtw(query['gx'],data['gx'])
        distance += dtw(query['gy'],data['gy'])
        distance += dtw(query['gz'],data['gz'])
          
        distance_list.append(distance)
        file_list.append(file)
      
    print(file_list[max(enumerate(distance_list), key=lambda x: x[1])[0]])
    print(distance_list[max(enumerate(distance_list), key=lambda x: x[1])[0]])
      
    return 0


#/-----------------------------

def dtw(vec1, vec2):
    d = np.zeros([len(vec1)+1, len(vec2)+1])
    d[:] = np.inf
    d[0, 0] = 0
    for i in range(1, d.shape[0]):
        for j in range(1, d.shape[1]):
            cost = pow(vec1[i-1]-vec2[j-1], 2)
            d[i, j] = cost + min(d[i-1, j], d[i, j-1], d[i-1, j-1])
    return d[i][j]


#/-----------------------------

def parseCSV(file):
    data = {}

    date = []
    ax = []
    ay = []
    az = []
    gx = []
    gy = []
    gz = []

    i = 0

    reader = csv.reader( open(file, "r") )
    for row in reader:
       date.append(row[0])
       ax.append(float(row[1]))
       ay.append(float(row[2]))
       az.append(float(row[3]))
       gx.append(float(row[4]))
       gy.append(float(row[5]))
       gz.append(float(row[6]))

    data['date'] = date
    data['ax'] = ax
    data['ay'] = ay
    data['az'] = az
    data['gx'] = gx
    data['gy'] = gy
    data['gz'] = gz
    return data

#/-----------------------------

getDistances(input())
