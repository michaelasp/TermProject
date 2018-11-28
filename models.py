from findFolder import *
from changeDB import add_gpxFile
from select import *
from math import sin, cos, sqrt, atan2, radians

def retrieveFiles(data):
    (folders, files) = findGPX(data.path)
    data.totalPages = (len(files) + len(folders)) // data.pageLength
    start = data.currentPage * data.pageLength
    if start > len(files) - 1:
        fileStart = start - len(files)
        return folders[fileStart:fileStart+data.pageLength]
    else:
        if len(files) - start >= data.pageLength:
            return files[start:start+data.pageLength]
        else:
            end = len(files) - start
            return files[start:start+end] + folders[:(start+data.pageLength-end)]

def retrieveUsers(data):
    data.totalPages = len(data.users) // data.pageLength
    start = data.currentPage * data.pageLength
    return data.users[start:start+data.pageLength]

def retrieveRides(data):
    data.totalRides = select_gpx(data.conn, data.id)
    data.totalPages = len(data.totalRides) // data.pageLength
    start = data.currentPage * data.pageLength
    return data.totalRides[start:start+data.pageLength]

def addGPX(data, selected):
    name = data.files[selected]
    if data.path == ".":
        gpxFile = data.files[selected]
    else:
        gpxFile = data.path + data.files[selected]
    gpx = open(gpxFile, 'r')
    add_gpxFile(data.conn, name, gpx, data.id)

def retrieveGPXMiles(data):
    files = select_gpx(data.conn, data.id)
    data.totalRides = len(files)
    data.totalMiles = 0
    for gpx in files:
        data.totalMiles += gpx[3]
    data.totalMiles = int(data.totalMiles)

def reccommendTrail(data):
    pass

#Find distance from lattitude longitude https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
def findDistance(lat1, lon1, lat2, lon2):
    R = 6373.0
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance













