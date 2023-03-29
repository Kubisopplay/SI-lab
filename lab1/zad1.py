from helper import Node, get_distance, strtotime, timediff
import pandas as pd
import time
import threading
from dateutil.relativedelta import *
def zad1(start, end, all_stops : dict, data : pd.DataFrame, start_hour):
    startnode = Node(start, None, start_hour)
    openlist = [startnode]
    closedlist = []
    while len(openlist) > 0:
        print("openlist",len(openlist))
        print("closedlist",len(closedlist))
        openlist.sort(key=lambda x: x.f, reverse=True)
        currentnode = openlist.pop()
        print(currentnode.name)
        closedlist.append(currentnode)
        # success
        if currentnode.name == end:
            return get_path(currentnode, startnode)
        else:
            children = get_children(currentnode, all_stops, data)
            children = [child for child in children if child not in closedlist]
            for child in children:
                child = get_values(child, currentnode, end,startnode, all_stops)
                openlist.sort(key=lambda x : x.g, reverse=True)
                for i in openlist:
                    if child.name == i.name and child.g > i.g:
                        continue
                openlist.append(child)
            


def get_path(currentnode, startnode):
    path = []
    while currentnode.parent is not None:
        path.append((currentnode.name, time.strftime( "%H:%M:%S",currentnode.time), currentnode.line))
        currentnode = currentnode.parent
    path.append((startnode.name,time.strftime("%H:%M:%S",startnode.time)))
    path.reverse()
    return path

def get_children(currentnode : Node, all_stops, data : pd.DataFrame):
    children = []
    candidates = data.loc[data["start_stop"] == currentnode.name]
    for i in candidates.itertuples():
        child = Node(i.end_stop, currentnode, i.arrival_time)
        child.line = i.line
        if child.time <= currentnode.time:
            continue
        if abs(timediff(currentnode.time, child.time)) > 2000:
            continue
        children.append(child)
       
    return children


#magic happens here
def get_values(child : Node, currentnode : Node, end,start, all_stops):
    child.g = currentnode.g + abs(timediff(currentnode.time, child.time)) #get_distance(currentnode.name, child.name)#+ 
    if child.line != currentnode.line:
        child.g = child.g + 100000 #koszt przesiadki jest spory, a co najmniej niemały
    child.h = get_distance(child.name, end) + abs(timediff(child.time,currentnode.time )) 
    child.f = child.g + child.h 
    return child
