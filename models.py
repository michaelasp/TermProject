from findFolder import *
from changeDB import add_gpxFile
from select import *
from math import sin, cos, sqrt, atan2, radians
import gpxpy

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
    data.totalRides = files
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

def findSections(data):
    (_,_,gpxFile,_, min_lat, min_lon, max_lat, max_lon,_) = data.plot
    gpx = gpxpy.parse(gpxFile)
    i=0
    plotNext = False
    last = []
    section = []
    sections = []
    looping = False
    loopDist = 0
    tolerance = 0.0008
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                posX = point.latitude - min_lat
                posY = point.longitude - min_lon
                #posX, posY = float("%.3f" % (2 * posX)), float("%.3f" % (2 * posY))
                if i != 0:
                    plotNext = True
                    #checks through all current points to see if a new one can be added or not
                    for (lastX, lastY) in last:
                        if abs(posX - lastX) < tolerance and abs(posY - lastY) < tolerance:
                            plotNext = False
                            curPoint = (lastX, lastY)
                            break
                if i == 0:
                    last.append((posX, posY))
                    section.append((posX, posY))
                elif plotNext == True:
                    last.append((posX, posY))
                    if looping == True:
                        loop = findFloats(section, section[-1])[0]
                        assert(section[loop] == section[-1])
                        loopDist = len(section) - loop
                        #in order not to have short loops
                        if len(section[-loopDist:-1]) > 10: 
                            sections.append(section[-loopDist:])
                            assert(section[-loopDist:][0] == section[-loopDist:][-1])
                            section = section[:-loopDist+1]
                            looping = False
                    section.append((posX, posY))
                    plotNext = False
                else:
                    (segEndX, segEndY) = section[-1]
                    if abs(posX - segEndX) < tolerance and abs(posY - segEndY) < tolerance:
                        pass
                    else:
                        looping = True
                        section.append(curPoint)
                i += 1
    sections.append(section)
    return sections

#https://stackoverflow.com/questions/24935938/how-to-find-a-float-number-in-a-list , modified to use tuples
def findFloats(listOfFloats, value):
    return [i for i, tup in enumerate(listOfFloats)
            if abs(tup[0]-value[0]) < 0.00001 and abs(tup[1]-value[1]) < 0.00001]













