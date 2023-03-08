import tkinter as tk
import csv
import os
import pandas as pd 

raw_data = open('C:\Studia\Sem6\SI-lab\lab1\connection_graph.csv', 'r', encoding='utf-8')

data =  pd.read_csv(raw_data, sep=',')
print(data)