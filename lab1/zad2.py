#djikstra algorithm
from helper import Node, get_distance, strtotime, timediff
import pandas as pd
import time


def djikstra(start, end, all_stops : dict, data : pd.DataFrame, start_hour):
    dist  = dict()
    dist[start] = 0
    prev = dict()
    prev[start] = None
    Q = list(all_stops.keys())
    while len(Q) > 0:
        Q.sort(key=lambda x: dist[x])
        u = Q.pop(0)
        if u == end:
            break
        for v in get_children(Node(u, None, start_hour), all_stops, data):
            alt = dist[u] + get_distance(u, v.name)
            if alt < dist.get(v.name, float('inf')):
                dist[v.name] = alt
                prev[v.name] = u
    path = []
    u = end
    while u is not None:
        path.append(u)
        u = prev.get(u)
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