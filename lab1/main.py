import random
import tkinter as tk
import csv
import os
import pandas as pd 
import multiprocessing
import math
from helper import Node, get_distance,set_przystanki
from zad1 import zad1
import cProfile
import timeit

raw_data = open('C:\\Studia\\Sem6\\SI-lab\\lab1\\connection_graph.csv', 'r', encoding='utf-8')

data =  pd.read_csv(raw_data, sep=',')


przystanki = dict()

for i in data["start_stop"].unique():
    loc = data.loc[data["start_stop"] == i].iloc[0]
    przystanki[i] = loc[7], loc[8]
  
for i in data["end_stop"].unique():
    loc = data.loc[data["end_stop"] == i].iloc[0]
    przystanki[i] = loc[7], loc[8]

set_przystanki(przystanki)
#for i in przystanki:
  #  print(i, przystanki[i])

min_latitude = min([przystanki[i][0] for i in przystanki])
max_latitude = max([przystanki[i][0] for i in przystanki])
min_longitude = min([przystanki[i][1] for i in przystanki])
max_longitude = max([przystanki[i][1] for i in przystanki])

print(min_latitude, min_longitude, max_latitude, max_longitude)

cProfile.run('zad1("PL. GRUNWALDZKI", "DWORZEC GŁÓWNY", przystanki, data, "10:00:00")', "wynik.txt")
#print(zad1( "DWORZEC GŁÓWNY","PL. GRUNWALDZKI", przystanki, data, "20:00:00"))
cProfile.run('zad1("Komuny Paryskiej", "Wilkszyn - Polna", przystanki, data, "01:39:39")', "wynik2.txt")
random.seed(2137)
test_pairs = []
for i in range(10):
    start = list(przystanki)[random.randint(0, len(przystanki)-1)]
    end = list(przystanki)[random.randint(0, len(przystanki)-1)]
    while end == start:
        end = list(przystanki)[random.randint(0, len(przystanki.keys())-1)]
    hour = str(random.randint(0, 23)).zfill(2) + ":" + str(random.randint(0, 59)).zfill(2) + ":" + str(random.randint(0, 59)).zfill(2)
    
    test_pairs.append((start, end,hour))
  
#default values for time and distance factors
default = 0 

for start, finish, hour in test_pairs:
    print("start ", start, "finish ", finish, "hour ", hour)
    default = default + timeit.timeit(lambda: zad1(start, finish, przystanki, data, hour), number=1)





print("default", default/10)