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
            for i in data.loc[data["start_stop"] == currentnode.name].itertuples():
                child = Node(i[2], currentnode, i[6])
                if child in closedlist:
                    continue
                child.g = currentnode.g + get_distance(currentnode.name, child.name)
                child.h = get_distance(child.name, end)
                child.f = child.g + child.h
                if child in openlist:
                    if child.g > currentnode.g:
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