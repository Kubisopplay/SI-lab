import time
def get_distance(name1, name2):
    global przystanki
    lat1, lon1 = przystanki[name1]
    lat2, lon2 = przystanki[name2]
    R = 6371
    dLat = (lat2-lat1)*3.141592/180
    dLon = (lon2-lon1)*3.141592/180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1*3.141592/180) * math.cos(lat2*3.141592/180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d

    
    
def strtotime(str):
    return time.strptime(str, "%H:%M:%S")

class Node():
    def __init__(self, name, parent, time = "12:00:00"):
        self.name = name
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0
        self.time = strtotime(time)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
