from findFolder import *
from changeDB import *
from select import *


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











