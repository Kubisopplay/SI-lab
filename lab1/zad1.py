from helper import Node, get_distance, strtotime
import pandas as pd



def zad1(start, end, all_stops : dict, data : pd.DataFrame, start_hour):
    startnode = Node(start, None, start_hour)
    openlist = [startnode]
    closedlist = []
    while len(openlist) > 0:
        openlist.sort(key=lambda x: x.f, reverse=True)
        currentnode = openlist.pop()
        closedlist.append(currentnode)
        # success
        if currentnode.name == end:
            return get_path(currentnode, start)
        else:
            children = get_children(currentnode, all_stops, data)
            for child in children:
                if child in closedlist:
                    continue
            get_values(child, currentnode, end, all_stops)
            for i in openlist:
                if child.name == i.name and child.g > i.g:
                    continue
            openlist.append(child)
            


def get_path(currentnode, startnode):
    path = []
    while currentnode.parent is not None:
        path.append(currentnode.name)
        currentnode = currentnode.parent
    path.append(startnode)
    path.reverse()
    return path

def get_children(currentnode : Node, all_stops, data : pd.DataFrame):
    children = []
    for i in data["start_stop" == currentnode.name].itertouples():
        child = Node(i["end_stop"], currentnode, i["arrival_time"])
        children.append(child)
    return children


#magic happens here
def get_values(child : Node, currentnode : Node, end, all_stops):
    child.g = currentnode.g + get_distance(child.name, currentnode.name)
    child.h = get_distance(child.name, end)
    child.f = child.g + child.h
    return child
