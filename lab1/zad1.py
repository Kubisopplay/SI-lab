from helper import Node, get_distance, strtotime, timediff
import pandas as pd
import time
import threading
from dateutil.relativedelta import *



stops = dict()


def zad1(start, end, all_stops : dict, data : pd.DataFrame, start_hour):
    startnode = Node(start, None, start_hour)
    data.sort_values(by="arrival_time",inplace=True)
    stop_lists = create_stops(data, all_stops)
    openlist = [startnode]
    closedlist = []
    while len(openlist) > 0:
        #print("openlist",len(openlist))
        #print("closedlist",len(closedlist))
        openlist.sort(key=lambda x: x.f, reverse=True) 
        currentnode = openlist.pop()
        #print(currentnode.name, time.strftime( "%H:%M:%S",currentnode.time), currentnode.line)
        closedlist.append(currentnode)
        if len(closedlist) > 10000:
            print("Przeszedl 10000 wezlow, prawdopodobnie nie dziala")
            return None
        # success
        if currentnode.name == end:
            print("openlist",len(openlist))
            print("closedlist",len(closedlist))
            return get_path(currentnode, startnode)
        else:
            children = get_children(currentnode, stop_lists, data)
            children = [child for child in children if child not in closedlist]
            for child in children:
                child = get_values(child, currentnode, end,startnode, all_stops)
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
    #print(path)
    return path


def get_children(currentnode : Node, all_stops, data : pd.DataFrame):
    children = []
    #candidates = data.loc[data["start_stop"] == currentnode.name]
    candidates = all_stops[currentnode.name]
    candidates = candidates.loc[candidates["arrival_time"] > time.strftime("%H:%M:%S",currentnode.time)]
    #unique_lines = candidates["end_stop"].unique().tolist()
    candidates = candidates.drop_duplicates(subset=["end_stop"], keep="first")
    for i in candidates.itertuples():
        child = Node(i.end_stop, currentnode, i.arrival_time)
        child.line = i.line
        children.append(child)
        continue
        if abs(timediff(currentnode.time, child.time)) > 1000:
            continue
        if len(children) > 10:
            if child.name in unique_lines:
                children.append(child) 
                unique_lines.remove(child.name)
            if unique_lines == []:
                break
            continue
        children.append(child)

    
       
    return children
g_timefactor = 1
g_distancefactor =0
g_offset = 100 
h_timefactor = 1
h_distancefactor = 2

przesiadka_factor = 10
#magic happens here

def get_values(child : Node, currentnode : Node, end,start, all_stops):
    global h_distancefactor, h_timefactor, g_distancefactor, g_timefactor, przesiadka_factor
    child.g = currentnode.g + abs(timediff(currentnode.time, child.time))*g_timefactor + get_distance(currentnode.name, child.name)*g_distancefactor + g_offset 
    if child.line != currentnode.line:
        child.g = child.g + 1000*przesiadka_factor #koszt przesiadki jest spory, a co najmniej niemały
    child.h = get_distance(child.name, end)*h_distancefactor + abs(timediff(child.time,currentnode.time ))*h_timefactor
    child.f = child.g + child.h 
    return child

def set_globals(g_tf,g_df,g_of,h_tf,h_df,p_f):
    global h_distancefactor, h_timefactor, g_distancefactor, g_timefactor, przesiadka_factor,g_offset
    g_timefactor = g_tf
    g_distancefactor = g_df
    h_timefactor = h_tf
    h_distancefactor = h_df
    przesiadka_factor = p_f
    g_offset = g_of


def create_stops(data, start_stops):
    stop_list = dict()
    for stop in start_stops:
        stop_list[stop] = data.loc[data["start_stop"] == stop].copy()
        stop_list[stop].sort_values(by="arrival_time",inplace=True)
    return stop_list