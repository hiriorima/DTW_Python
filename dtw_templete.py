import numpy as np
import csv
import glob
import math

sample_count = 20

#/-----------------------------

def motionRecognition(input):

    allDistances = getDistances(input);
    count = len(parseCSV(input + '.csv')['ax'])
    
    min_dist_list = []
    min_file_list = []

    for count in range(math.ceil(count / sample_count)):
      
        distances = []
        files = []

        for file in allDistances.keys():
            distances.append(allDistances[file][count])            
            files.append(file)
       
        min_dist_list.append(min(distances))
        min_file_list.append(files[min(enumerate(distances), key=lambda x: x[1])[0]])
 
    print("-----------result-------------")
    for i in range(len(min_file_list)):
        print(str(i) + "秒~" )
        print(min_file_list[i])
        print(min_dist_list[i])
    return 0

#/-----------------------------

def getDistances(query_file_name):

    distances = {}

    files = glob.glob('./data/*.csv')

    query = parseCSV(query_file_name + '.csv'  )
    query_len = len(query['ax'])

    print("-----------途中経過-------------")

    for file in files:
        data = parseCSV(file)
        distance_list = []
        count = 1
        i = 0
       
        while i <= query_len:
          distance = 0.0
          if i + sample_count >= query_len:
             distance += dtw(query['ax'][i : query_len -1],data['ax'])
             distance += dtw(query['ay'][i : query_len -1],data['ay'])
             distance += dtw(query['az'][i : query_len -1],data['az'])
             distance += dtw(query['gx'][i : query_len -1],data['gx'])
             distance += dtw(query['gy'][i : query_len -1],data['gy'])
             distance += dtw(query['gz'][i : query_len -1],data['gz'])
          else:
             distance += dtw(query['ax'][i : i + 60],data['ax'])
             distance += dtw(query['ay'][i : i + 60],data['ay'])
             distance += dtw(query['az'][i : i + 60],data['az'])
             distance += dtw(query['gx'][i : i + 60],data['gx'])
             distance += dtw(query['gy'][i : i + 60],data['gy'])
             distance += dtw(query['gz'][i : i + 60],data['gz'])
          print(file)
          #print(count)
          print(distance)
          distance_list.append(distance)
          i = i + sample_count
          count = count + 1
      
        print(file.replace("./data/",""))
        distances[file.replace("./data/","")] = distance_list

    return distances

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
