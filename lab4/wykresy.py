import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

with open("results.json", "r") as readfile:
    data = json.load(readfile)
    groups = {
        "random-accuracy": [],
        "random-f1": [],
        "edge-accuracy": [],
        "edge-f1": []
    }
    for key in data:
        groups["random-accuracy"].append(data[key]["random"]["accuracy"])
        groups["random-f1"].append(data[key]["random"]["f1"])
        groups["edge-accuracy"].append(data[key]["edge"]["accuracy"])
        groups["edge-f1"].append(data[key]["edge"]["f1"])
        
    x = np.arange(len(data.keys()))
    width = 0.1
    fig, ax = plt.subplots(layout="constrained")

    multiplier = 0

    for attribute, measurement in groups.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1
    
    ax.set_ylabel('Scores')
    ax.set_title('')
    ax.set_xticks(x + width, data.keys())
    ax.legend(loc='upper left', ncols=3)
    ax.set_ylim(0, 1)

    plt.show()

