import time
import math
import datetime
przystanki = dict()

def set_przystanki(przystanki_):
    global przystanki
    przystanki = przystanki_

def get_distance(name1, name2):
    global przystanki
    lat1, lon1 = przystanki[name1]
    lat2, lon2 = przystanki[name2]
    dLat = abs(lat2-lat1)
    dLon = abs(lon2-lon1)
    d = dLat + dLon
    return d * 100000 #mnożenia są po to żeby rząd wielkości był podobny

    
    
def strtotime(text):
    if int(text[0:2]) >23:
        text = str(int(text[0:2])-24) + text[2:] 
    return time.strptime(text, "%H:%M:%S") #I hate this so much
    
 

class Node():
    def __init__(self, name, parent, time = "12:00:00"):
        self.name = name
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0
        self.time = strtotime(time)
        self.line = ""

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
    
    def __eq__(self, other):
        return self.name == other.name and self.time == other.time
    
    


def timediff(time1 : time.struct_time, time2: time.struct_time):
    if (time1.tm_hour == 0 ) and time2.tm_hour == 23 :
        return (time2.tm_hour-24-time1.tm_hour)*3600 + (time2.tm_min - time1.tm_min)*60 + (time2.tm_sec - time1.tm_sec)
    if time2.tm_hour == 0  and time1.tm_hour == 23:
        return (time2.tm_hour+24 - time1.tm_hour)*3600 + (time2.tm_min - time1.tm_min)*60 + (time2.tm_sec - time1.tm_sec)
        
    
    return (time2.tm_hour - time1.tm_hour)*3600 + (time2.tm_min - time1.tm_min)*60 + (time2.tm_sec - time1.tm_sec)
        