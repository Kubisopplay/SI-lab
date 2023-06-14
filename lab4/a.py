import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn as sk
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.tree import DecisionTreeClassifier
import json

data = pd.read_csv('''C:\Studia\Sem6\SI-lab\lab4\glass.data''')
savefile = open("results.json", "w")
jsontowrite = {}

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

def predict(predictor, desc):
    savejson = {}
    predictions = predictor.predict(random_data.iloc[:, 2:-1])
    print("Number of mispredictions for random cases: "+ str((predictions != random_data.iloc[:, -1]).sum()))
    print("Accuracy: " + str(accuracy_score(random_data.iloc[:, -1], predictions)))
    print("F1: " + str(f1_score(random_data.iloc[:, -1], predictions, average='macro')))
    temp = {}
    temp["accuracy"] = accuracy_score(random_data.iloc[:, -1], predictions)
    temp["f1"] = f1_score(random_data.iloc[:, -1], predictions, average='macro')
    savejson["random"] = temp

    predictions = predictor.predict(edge_cases.iloc[:, 3:-1])
    print("Number of mispredictions for edge cases: "+ str((predictions != edge_cases.iloc[:, -1]).sum()))
    print("Accuracy: " + str(accuracy_score(edge_cases.iloc[:, -1], predictions)))
    print("F1: " + str(f1_score(edge_cases.iloc[:, -1], predictions, average='macro')))
    temp = {}
    temp["accuracy"] = accuracy_score(edge_cases.iloc[:, -1], predictions)
    temp["f1"] = f1_score(edge_cases.iloc[:, -1], predictions, average='macro')
    savejson["edge"] = temp
    
    jsontowrite[desc] = savejson



predict(class1, "Normal Naive Bayes")

class2 = GaussianNB(var_smoothing=0.0001)
class2.fit(training_data.iloc[:, 2:-1], training_data.iloc[:, -1])

predict(class2, "Naive Bayes with smoothing")

class3 = GaussianNB(priors=np.array([1,0,0,0,0,0]), var_smoothing=0.0001)
class3.fit(training_data.iloc[:, 2:-1], training_data.iloc[:, -1])
predict(class3 , "Naive Bayes with preset priors")

print("Decision trees:")

tree1 = DecisionTreeClassifier(random_state=2137)

tree1.fit(training_data.iloc[:, 2:-1], training_data.iloc[:, -1])
predict(tree1, "Normal Decision Tree")

tree2 = DecisionTreeClassifier(random_state=2137, min_samples_leaf=5, max_depth=5)

tree2.fit(training_data.iloc[:, 2:-1], training_data.iloc[:, -1])
predict(tree2, "Decision Tree with min_samples_leaf=5, max_depth=5")

tree3 = DecisionTreeClassifier(random_state=2137, max_depth=20, criterion="entropy")
tree3.fit(training_data.iloc[:, 2:-1], training_data.iloc[:, -1])
predict(tree3, "Decision Tree with max_depth=20, criterion=entropy")

# standaryzowane dane
training_data.iloc[:,2:-1] = Normalizer().fit_transform(StandardScaler().fit_transform(training_data.iloc[:,2:-1]))
random_data.iloc[:,2:-1] = Normalizer().fit_transform(StandardScaler().fit_transform(random_data.iloc[:,2:-1]))
edge_cases.iloc[:,3:-1] = Normalizer().fit_transform(StandardScaler().fit_transform(edge_cases.iloc[:,3:-1]))


print("Standaryzowane dane:")

class1 = GaussianNB()
class1.fit(training_data.iloc[:, 2:-1], training_data.iloc[:, -1])
predict(class1, "Normal Naive Bayes with standardized data")

class2 = GaussianNB(var_smoothing=0.0001)
class2.fit(training_data.iloc[:, 2:-1], training_data.iloc[:, -1])
predict(class2, "Naive Bayes with smoothing with standardized data")

class3 = GaussianNB(priors=np.array([1,0,0,0,0,0]), var_smoothing=0.0001)
class3.fit(training_data.iloc[:, 2:-1], training_data.iloc[:, -1])
predict(class3 , "Naive Bayes with preset priors with standardized data")

print("Decision trees:")
tree1 = DecisionTreeClassifier(random_state=2137)
tree1.fit(training_data.iloc[:, 2:-1], training_data.iloc[:, -1])
predict(tree1, "Normal Decision Tree with standardized data")

tree2 = DecisionTreeClassifier(random_state=2137, min_samples_leaf=5, max_depth=5)
tree2.fit(training_data.iloc[:, 2:-1], training_data.iloc[:, -1])
predict(tree2, "Decision Tree with min_samples_leaf=5, max_depth=5 with standardized data")

tree3 = DecisionTreeClassifier(random_state=2137, max_depth=20, criterion="entropy")
tree3.fit(training_data.iloc[:, 2:-1], training_data.iloc[:, -1])
predict(tree3, "Decision Tree with max_depth=20, criterion=entropy with standardized data")








savefile.write(json.dumps(jsontowrite, indent=4))
savefile.close()
