import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn as sk
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix


data = pd.read_csv('glass.data')


headers = data.columns.values[1:-1]
print(headers)

#split_data = []
#for row in data.itertuples():
#    split_data.append((row[2:11], row[11]))


random_data = data.sample(frac=0.05,random_state=2137) #nothing else done to the data


edge_cases = []
important= ["Ba", "Na", "Al"]
for parameter in headers: #bad idea, too many edge cases
    temp = data.copy().sort_values(by=parameter)
    edge_cases.append(temp.iloc[0])
    edge_cases.append(temp.iloc[-1])

edge_cases = pd.DataFrame(edge_cases).reset_index()

training_data = data.drop(edge_cases.index)
training_data = training_data.drop(random_data.index)

print(training_data)
print(random_data)
print(edge_cases)
class1 = GaussianNB()
class1.fit(training_data.iloc[:, 2:-1], training_data.iloc[:, -1])

predictions = class1.predict(random_data.iloc[:, 2:-1])
print("Number of mispredictions: "+ str((predictions != random_data.iloc[:, -1]).sum()))
print("Accuracy: " + str(accuracy_score(random_data.iloc[:, -1], predictions)))

predictions = class1.predict(edge_cases.iloc[:, 3:-1])
print("Number of mispredictions: "+ str((predictions != edge_cases.iloc[:, -1]).sum()))
print("Accuracy: " + str(accuracy_score(edge_cases.iloc[:, -1], predictions)))