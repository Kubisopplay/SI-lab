import tkinter as tk
import csv
import os
import pandas as pd 
import threading
import math
from helper import Node, get_distance


raw_data = open('C:\Studia\Sem6\SI-lab\lab1\connection_graph.csv', 'r', encoding='utf-8')

data =  pd.read_csv(raw_data, sep=',')


przystanki = dict()

for i in data["start_stop"].unique():
    loc = data.loc[data["start_stop"] == i].iloc[0]
    przystanki[i] = loc[7], loc[8]

for i in przystanki:
    print(i, przystanki[i])

