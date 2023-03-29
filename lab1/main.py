import tkinter as tk
import csv
import os
import pandas as pd 
import threading
import math
from helper import Node, get_distance,set_przystanki
from zad1 import zad1
import cProfile

raw_data = open('connection_graph.csv', 'r', encoding='utf-8')

data =  pd.read_csv(raw_data, sep=',')


przystanki = dict()

for i in data["start_stop"].unique():
    loc = data.loc[data["start_stop"] == i].iloc[0]
    przystanki[i] = loc[7], loc[8]

set_przystanki(przystanki)
#for i in przystanki:
  #  print(i, przystanki[i])

min_latitude = min([przystanki[i][0] for i in przystanki])
max_latitude = max([przystanki[i][0] for i in przystanki])
min_longitude = min([przystanki[i][1] for i in przystanki])
max_longitude = max([przystanki[i][1] for i in przystanki])

print(min_latitude, min_longitude, max_latitude, max_longitude)

cProfile.run('print(zad1("PL. GRUNWALDZKI", "DWORZEC GŁÓWNY", przystanki, data, "10:00:00"))', "wynik.txt")
print(zad1( "DWORZEC GŁÓWNY","PL. GRUNWALDZKI", przystanki, data, "20:00:00"))