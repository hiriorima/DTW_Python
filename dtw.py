import numpy as np
import csv
import glob
import math
import pandas as pd
from pylab import *
import matplotlib.pyplot as plt
from numpy.random import randn

def actualShowPlot(input,actualData):
  
    dateparse = lambda x: pd.datetime.strptime(x, '%H%M%S%f')

    df = pd.read_csv(input + '.csv', index_col=0,date_parser=dateparse)
    df.columns = [u'ax',u'ay',u'az', u'gx', u'gy', u'gz']
    df.head()
    rcParams['figure.figsize'] = 10,6
    df.plot()

    data = actualData
    plt.plot(df.index,data)
     
    plt.show()

    return 0

#/-----------------------------
def showPlot(input,actualData,matchingData):


    dateparse = lambda x: pd.datetime.strptime(x, '%H%M%S%f')

    df = pd.read_csv(input + '.csv', index_col=0,date_parser=dateparse)
    df.columns = [u'ax',u'ay',u'az', u'gx', u'gy', u'gz']
    df.head()
    rcParams['figure.figsize'] = 10,6
    df.plot()


    data = matchingData

    plt.plot(df.index,data)

    data = actualData
    plt.plot(df.index,data)
    

    print("--------result--------")
   
    i = 0

    up_TT = 0
    up_TF = 0
    up_FT = 0
   
    inset_TT = 0
    inset_TF = 0
    inset_FT = 0
    
    put_TT = 0
    put_TF = 0
    put_FT = 0


    for i in range(len(matchingData)):
        if actualData[i] == matchingData[i]:
           if matchingData[i] == 5:
              up_TT = up_TT + 1
           elif matchingData[i] == 6:
              inset_TT = inset_TT + 1
           elif matchingData[i] == 7:
              put_TT = put_TT + 1
        else:
           if actualData[i] == 4:
              if matchingData[i] == 5:
                up_FT = up_FT + 1
              elif matchingData[i] == 6:
                inset_FT = inset_FT + 1
              elif matchingData[i] == 7:
                put_FT = put_FT + 1
           elif actualData[i] == 5:
                up_TF = up_TF + 1
           elif actualData[i] == 6:
                inset_TF = inset_TF + 1
           elif actualData[i] == 7:
                put_TF = put_TF + 1
                  
    print("up_TT" + str(up_TT) + "," + "up_TF" + str(up_TF) + "," + "up_FT" + str(up_FT) + ",")
    print("inset_TT" + str(inset_TT) + "," + "inset_TF" + str(inset_TF) + "," + "inset_TT" + str(inset_FT) + ",")
    print("put_TT" + str(put_TT) + "," + "put_TF" + str(put_TF) + "," + "put_TT" + str(put_FT) + ",")

    plt.show()
    return 0


#/-----------------------------

def motionRecognition(input):

    allDistances = getDistances(input)
    
    min_dist_list = []
    min_file_list = []

    actual = getActual(input)

    #print(len(allDistances))
    #print(len(actual))

    showPlot(input,actual,allDistances)

    #actualShowPlot(input,actual)

    #print(min_file_list)
    return 0

def getActual(query_file_name):

    i = 0

    actual = []

    files = glob.glob('./correct/*_06.csv')

    up_files = glob.glob('./correct/up*_05.csv')
    inset_files = glob.glob('./correct/inset*_05.csv')
    put_files = glob.glob('./correct/put*_05.csv')
    query = parseCSV(query_file_name + '.csv'  )
    query_len = len(query['ax'])
 
    up_count = 0
    inset_count = 0
    put_count = 0


    while i < query_len - 1:
      distance_list = []
      file_list = []
      data_len_list = []
      
      for k in range(3):
        distance = 0.0
        #print(file)
        if k == 0:
          data = parseCSV(up_files[up_count])
        elif k == 1:
          data = parseCSV(inset_files[inset_count])
        elif k == 2:
          data = parseCSV(put_files[put_count])

        data_len = len(data['ax'])

        if i + data_len >= query_len:
           distance += dtw(query['ax'][i : query_len - 1],data['ax'])
           distance += dtw(query['ay'][i : query_len - 1],data['ay'])
           distance += dtw(query['az'][i : query_len - 1],data['az'])
           distance += dtw(query['gx'][i : query_len - 1],data['gx'])
           distance += dtw(query['gy'][i : query_len - 1],data['gy'])
           distance += dtw(query['gz'][i : query_len - 1],data['gz'])
        else:
           distance += dtw(query['ax'][i : i + data_len],data['ax'])
           distance += dtw(query['ay'][i : i + data_len],data['ay'])
           distance += dtw(query['az'][i : i + data_len],data['az'])
           distance += dtw(query['gx'][i : i + data_len],data['gx'])
           distance += dtw(query['gy'][i : i + data_len],data['gy'])
           distance += dtw(query['gz'][i : i + data_len],data['gz'])
          #print(count)
          #print(distance)
 
        distance_list.append(distance)
        file_list.append(k)
        data_len_list.append(data_len)
      
      #print(file_list[min(enumerate(distance_list), key=lambda x: x[1])[0]])
      #print(distance_list[min(enumerate(distance_list), key=lambda x: x[1])[0]])
      
      j = 0
      #   i = i + len(parseCSV(file_list[min(enumerate(distance_list), key=lambda x: x[1])[0]])['ax'])
      if 0 == file_list[min(enumerate(distance_list), key=lambda x: x[1])[0]]:
            if distance_list[min(enumerate(distance_list), key=lambda x: x[1])[0]] <= 0.01:
               for j in range(data_len_list[min(enumerate(distance_list), key=lambda x: x[1])[0]]):
                   #actual.append(9)
                   actual.append(5)

               if up_count < len(up_files) - 1:
                  up_count = up_count + 1
               i = i + data_len_list[min(enumerate(distance_list), key=lambda x: x[1])[0]]
            else:
               #actual.append(8)
               actual.append(4)

               i = i + 1
      elif 1 == file_list[min(enumerate(distance_list), key=lambda x: x[1])[0]]:
            if distance_list[min(enumerate(distance_list), key=lambda x: x[1])[0]] <= 0.01:
               for j in range(data_len_list[min(enumerate(distance_list), key=lambda x: x[1])[0]]):
                   #actual.append(10)
                    
                   actual.append(6)
               if inset_count < len(inset_files) - 1:
                  inset_count = inset_count + 1
               i = i + data_len_list[min(enumerate(distance_list), key=lambda x: x[1])[0]]
            else:
               #actual.append(8)
               actual.append(4)
               i = i + 1
      elif 2 == file_list[min(enumerate(distance_list), key=lambda x: x[1])[0]]:
            if distance_list[min(enumerate(distance_list), key=lambda x: x[1])[0]] <= 0.01:
               for j in range(data_len_list[min(enumerate(distance_list), key=lambda x: x[1])[0]]): 
                   #actual.append(12)
                   
                   actual.append(7)
               if put_count < len(put_files) -1:
                  put_count = put_count + 1
               i = i + data_len_list[min(enumerate(distance_list), key=lambda x: x[1])[0]]
            else:
               #actual.append(8)
               actual.append(4)
               i = i + 1
      else:
         #actual.append(8)
         actual.append(4)
         i = i + 1

    return actual

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
           distance += dtw(query['ax'][i : query_len - 1],data['ax'])
           distance += dtw(query['ay'][i : query_len - 1],data['ay'])
           distance += dtw(query['az'][i : query_len - 1],data['az'])
           distance += dtw(query['gx'][i : query_len - 1],data['gx'])
           distance += dtw(query['gy'][i : query_len - 1],data['gy'])
           distance += dtw(query['gz'][i : query_len - 1],data['gz'])
        else:
           distance += dtw(query['ax'][i : i + data_len],data['ax'])
           distance += dtw(query['ay'][i : i + data_len],data['ay'])
           distance += dtw(query['az'][i : i + data_len],data['az'])
           distance += dtw(query['gx'][i : i + data_len],data['gx'])
           distance += dtw(query['gy'][i : i + data_len],data['gy'])
           distance += dtw(query['gz'][i : i + data_len],data['gz'])
          #print(count)
          #print(distance)
          
        distance_list.append(distance)
        file_list.append(file)
      
      print(file_list[min(enumerate(distance_list), key=lambda x: x[1])[0]])
      print(distance_list[min(enumerate(distance_list), key=lambda x: x[1])[0]])
      
      j = 0

      #   i = i + len(parseCSV(file_list[min(enumerate(distance_list), key=lambda x: x[1])[0]])['ax'])
      if 'up' in file_list[min(enumerate(distance_list), key=lambda x: x[1])[0]]:
            if distance_list[min(enumerate(distance_list), key=lambda x: x[1])[0]] <= 3.5574192: #3.5574192 #2.964516 #1.976344
               for j in range(data_len):
                   if len(matches) < query_len - 1:
                      matches.append(5)
               i = i + data_len
            else:
               matches.append(4)
               i = i + 1
      elif 'inset' in file_list[min(enumerate(distance_list), key=lambda x: x[1])[0]]:
            if distance_list[min(enumerate(distance_list), key=lambda x: x[1])[0]] <= 1.717766: #1.0306596 #0.858883
               for j in range(data_len):
                   if len(matches) < query_len - 1:
                      matches.append(6)
               i = i + data_len
            else:
               matches.append(4)
               i = i + 1
      elif 'put' in file_list[min(enumerate(distance_list), key=lambda x: x[1])[0]]:
            if distance_list[min(enumerate(distance_list), key=lambda x: x[1])[0]] <= 3.4846512: #4.355814
               for j in range(data_len):
                   if len(matches) < query_len - 1: 
                      matches.append(7)
               i = i + data_len
            else:
               matches.append(4)
               i = i + 1
      else:
         matches.append(4)
         i = i + 1

      count = count + 1

#        print(file.replace("./data/",""))
      #distances[file.replace("./data/","")] = distance_list

    print(count)
    return matches

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
