import numpy as np
import csv
import glob
import math
import pandas as pd
from pylab import *
import matplotlib.pyplot as plt
from numpy.random import randn

#/-----------------------------
def showPlot(input,matchingData):


    dateparse = lambda x: pd.datetime.strptime(x, '%H%M%S%f')

    df = pd.read_csv(input + '.csv', index_col=0,date_parser=dateparse)
    df.columns = [u'ax',u'ay',u'az', u'gx', u'gy', u'gz']
    df.head()
    rcParams['figure.figsize'] = 10,6
    df.plot()
    
    data = matchingData

    plt.plot(df.index,data)
    
    plt.show()
    return 0


#/-----------------------------

def motionRecognition(input):

    allDistances = getDistances(input);
    
    min_dist_list = []
    min_file_list = []

    #print(min_file_list)
    return 0

#/-----------------------------

def getDistances(query_file_name):

    matches = []

    files = glob.glob('./data/*.csv')

    query = parseCSV(query_file_name + '.csv'  )
    query_len = len(query['ax'])

    print("-----------途中経過-------------")

    i = 0
    count = 0

    while i < query_len - 1:
      distance_list = []
      file_list = []
      for file in files:
        data = parseCSV(file)
        data_len = len(data['ax'])
        distance = 0.0
        #print(file)

        if i + data_len >= query_len:
           distance += dtw(query['ax'][i : query_len -1],data['ax'])
           distance += dtw(query['ay'][i : query_len -1],data['ay'])
           distance += dtw(query['az'][i : query_len -1],data['az'])
           distance += dtw(query['gx'][i : query_len -1],data['gx'])
           distance += dtw(query['gy'][i : query_len -1],data['gy'])
           distance += dtw(query['gz'][i : query_len -1],data['gz'])
        else:
           distance += dtw(query['ax'][i : i + data_len - 1],data['ax'])
           distance += dtw(query['ay'][i : i + data_len - 1],data['ay'])
           distance += dtw(query['az'][i : i + data_len - 1],data['az'])
           distance += dtw(query['gx'][i : i + data_len - 1],data['gx'])
           distance += dtw(query['gy'][i : i + data_len - 1],data['gy'])
           distance += dtw(query['gz'][i : i + data_len - 1],data['gz'])
          #print(count)
          #print(distance)
          
        distance_list.append(distance)
        file_list.append(file)
      
      print(file_list[min(enumerate(distance_list), key=lambda x: x[1])[0]])
      print(distance_list[min(enumerate(distance_list), key=lambda x: x[1])[0]])
    
      if distance_list[min(enumerate(distance_list), key=lambda x: x[1])[0]] <= 1.0:
      #   i = i + len(parseCSV(file_list[min(enumerate(distance_list), key=lambda x: x[1])[0]])['ax'])
         if 'up' in file_list[min(enumerate(distance_list), key=lambda x: x[1])[0]]:
            matches.append(5)
         elif 'inset' in file_list[min(enumerate(distance_list), key=lambda x: x[1])[0]]:
            matches.append(6)
      else:
         matches.append(4)
      
      i = i + 1
      count = count + 1

#        print(file.replace("./data/",""))
      #distances[file.replace("./data/","")] = distance_list

    showPlot(query_file_name,matches)

    print(count)
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
