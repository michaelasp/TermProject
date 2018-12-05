from tkinter import *
from image_util import *
from models import *
from math import atan
import gpxpy

def selectScreen(canvas, data):
    unitW = data.unitW
    unitH = data.unitH
    canvas.create_rectangle(unitW*2, unitH*5, unitW*9, unitH*15)
    canvas.create_rectangle(unitW*11, unitH*5, unitW*18, unitH*15)
    canvas.create_text(unitW*5.5, unitH*10, text = "New User", font = "Arial " + str(int(unitH)))
    canvas.create_text(unitW*14.5, unitH*10, text = "Login", font = "Arial " + str(int(unitH)))

def createScreen(canvas, data):
    unitW = data.unitW
    unitH = data.unitH
    canvas.create_rectangle(unitW*4, unitH*8, unitW*16, unitH*12)
    canvas.create_text(unitW*5, unitH*9, text = data.newUser, anchor = NW, font = "Arial " + str(int(unitH)))
    canvas.create_rectangle(unitW*6, unitH*18, unitW*14, unitH*20)
    canvas.create_text(unitW*12, unitH*19, text = "Cancel", font = "Arial " + 
        str(int(unitH)))

def viewScreen(canvas, data):
    unitW = data.unitW
    unitH = data.unitH
    canvas.create_text(unitW*7, unitH*1, text = "Welcome " + data.name, anchor = NW, font = "Arial " + 
        str(int(unitH)))
    canvas.create_rectangle(unitW*1, unitH*7, unitW*8, unitH*13)
    canvas.create_rectangle(unitW*12, unitH*7, unitW*19, unitH*13)
    canvas.create_rectangle(unitW*6, unitH*18, unitW*14, unitH*20)
    canvas.create_text(unitW*4.5, unitH*10, text = "New Activity", font = "Arial " + str(int(unitH/1.5)))
    canvas.create_text(unitW*15.5, unitH*10, text = "Recommendations", font = "Arial " + str(int(unitH/1.5)))
    canvas.create_text(unitW*7, unitH*18, text = "Input a new file", anchor = NW, font = "Arial " + 
        str(int(unitH)))

def viewAddGPX(canvas, data):
    unitW = data.unitW
    unitH = data.unitH
    for i in range(len(data.files)):
        canvas.create_text(unitW*7, unitH*2*i, text = data.files[i], anchor = NW, font = "Arial " + 
        str(int(unitH/2)))
    canvas.create_text(unitW*10, unitH*19.5, text = "Page: " + str(data.currentPage), font = "Arial " + 
        str(int(unitH/2)))

def viewProgress(canvas, data):
    unitW = data.unitW
    unitH = data.unitH
    canvas.create_text(unitW*10, unitH*.5, text = "You have done " + str(data.totalMiles) + " Miles", font = "Arial " + 
        str(int(unitH/2)))
    canvas.create_text(unitW*10, unitH*1.5, text = "You have done " + str(len(data.totalRides)) + " Activities Total", font = "Arial " + 
        str(int(unitH/2)))
    canvas.create_rectangle(unitW*12, unitH*7, unitW*19, unitH*13)
    canvas.create_text(unitW*15.5, unitH*10, text = "View Activities", font = "Arial " + 
        str(int(unitH/1.5)))
    canvas.create_rectangle(unitW*1, unitH*7, unitW*8, unitH*13)
    canvas.create_text(unitW*4.5, unitH*10, text =  "View Sections", font = "Arial " + 
        str(int(unitH/1.5)))

def viewRides(canvas, data):
    unitW = data.unitW
    unitH = data.unitH
    for i in range(len(data.curRides)):
        canvas.create_text(unitW*7, unitH*2*i, text = data.curRides[i][1], anchor = NW, font = "Arial " + 
        str(int(unitH/2)))
    canvas.create_text(unitW*10, unitH*19.5, text = "Page: " + str(data.currentPage), font = "Arial " + 
        str(int(unitH/2)))

def viewLogin(canvas, data):
    unitW = data.unitW
    unitH = data.unitH
    for i in range(len(data.curUsers)):
        canvas.create_text(unitW*7, unitH*2*i, text = data.curUsers[i][1], anchor = NW, font = "Arial " + 
        str(int(unitH/2)))    
    canvas.create_text(unitW*10, unitH*19.5, text = "Page: " + str(data.currentPage), font = "Arial " + 
        str(int(unitH/2)))
    
    

def plotPoints(canvas, data):
    unitW = data.unitW
    unitH = data.unitH
    marginX = unitW
    marginY = unitH
    (_,_,gpxFile,_, min_lat, min_lon, max_lat, max_lon,_) = data.plot
    totalChangex = max_lon - min_lon
    totalChangey = max_lat - min_lat
    gpx = gpxpy.parse(gpxFile)
    i=0
    elevationChange = 0
    elevation = 0
    point1 = None

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                posX = point.longitude - min_lon
                posY = point.latitude - min_lat
                ratioX = posX / totalChangex
                ratioY = posY / totalChangey
                if i == 0:
                    point1 = ((ratioX*18*unitW)+marginX, (ratioY*18*unitH)+marginY)
                    elevation = point.elevation
                    lastLat = point.latitude
                    lastLon = point.longitude
                else:
                    elevationChange = point.elevation - elevation
                    distance = findDistance(lastLat, lastLon, point.latitude, point.longitude)*1000
                    ratio = abs(atan(elevationChange/distance))
                    if ratio > .15:
                        r = 255
                    else:
                        r = int((255/.15) * ratio)
                    rgb = rgbString(r, 255-r, 0)
                    canvas.create_line(point1, ((ratioX*18*unitW)+marginX, (ratioY*18*unitH)+marginY), fill = rgb)
                    point1 = ((ratioX*18*unitW)+marginX, (ratioY*18*unitH)+marginY)
                    lastLat = point.latitude
                    lastLon = point.longitude
                    elevation = point.elevation
                i += 1




def viewSections(canvas, data):
    unitW = data.unitW
    unitH = data.unitH
    marginX = unitW
    marginY = unitH
    (_,_,gpxFile,_, min_lat, min_lon, max_lat, max_lon,_) = data.plot
    totalChangex = max_lon - min_lon
    totalChangey = max_lat - min_lat
    i=0
    point1 = None
    sections = data.sections
    j = 0
    for section in sections:
        i = 0
        for point in section:
            r = (255 - 20 * j)%255 
            rgb = rgbString(r, 255-r, 0)
            ratioX, ratioY, _ = point
            ratioX -= min_lon
            ratioY -= min_lat
            ratioX /= totalChangex
            ratioY /= totalChangey
            if i == 0:
                    point1 = ((ratioX*18*unitW)+marginX, (ratioY*18*unitH)+marginY)
            else:
                canvas.create_line(point1, ((ratioX*18*unitW)+marginX, (ratioY*18*unitH)+marginY), fill = rgb, width = 2)
                point1 = ((ratioX*18*unitW)+marginX, (ratioY*18*unitH)+marginY)
            i += 1
        j += 1
#From notes
def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

def viewPickRecommend(canvas, data):
    unitW = data.unitW
    unitH = data.unitH
    for i in range(len(data.curRides)):
        canvas.create_text(unitW*7, unitH*2*i, text = data.curRides[i][1], anchor = NW, font = "Arial " + 
        str(int(unitH/2)))

def viewRecommend(canvas, data):
    unitW = data.unitW
    unitH = data.unitH
    marginX = unitW
    marginY = unitH    
    trailType = data.trailType
    (_,_,gpxFile,_, min_lat, min_lon, max_lat, max_lon,_) = data.picked
    totalChangex = max_lon - min_lon
    totalChangey = max_lat - min_lat
    gpx = gpxpy.parse(gpxFile)
    sections = data.sections
    i=0
    point1 = None
    canvas.create_text(unitW*5, unitH*.5, text = "Gnarly", font = "Arial " + 
        str(int(unitH/2)), fill = data.colors[0])
    canvas.create_text(unitW*10, unitH*.5, text = "Challenging", font = "Arial " + 
        str(int(unitH/2)), fill = data.colors[1])
    canvas.create_text(unitW*15, unitH*.5, text = "Flowy", font = "Arial " + 
        str(int(unitH/2)), fill = data.colors[2])
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                posX = point.longitude - min_lon
                posY = point.latitude - min_lat
                #posX, posY = float("%.3f" % (2 * posX)), float("%.3f" % (2 * posY))

                ratioX = posX / (totalChangex)
                ratioY = posY / (totalChangey)
                if i == 0:
                    point1 = ((ratioX*18*unitW)+marginX, (ratioY*18*unitH)+marginY)
                else:
                    canvas.create_line(point1, ((ratioX*18*unitW)+marginX, (ratioY*18*unitH)+marginY))
                    point1 = ((ratioX*18*unitW)+marginX, (ratioY*18*unitH)+marginY)
                i += 1
    sortedSec = analyzeSections(sections)
    if len(sortedSec) > 2:
        div = len(sortedSec) // 3
        extra = (len(sortedSec) % 3) // 2
        sortedFlow = sortedSec[div*2+extra:] 
        sortedChal = sortedSec[div*1:div*2+extra]
        sortedGnar = sortedSec[:div*1]
    elif len(sortedSec) == 2:
        sortedGnar = [sortedSec[0]]
        sortedFlow = [sortedSec[1]]
        sortedChal = [(None, None)]
    else:
        sortedFlow = sortedSec
        sortedChal = [(None, None)]
        sortedGnar = [(None, None)]
    assert(sortedFlow != sortedChal)
    sortedSec = [sortedGnar, sortedChal, sortedFlow]
    print(sortedSec)
    j = 0
    for (_, elem) in sortedSec[trailType]:
        if elem != None:
            i = 0
            r = (255 - 20 * j)%255 
            rgb = rgbString(r, 255-r, 0)
            for pointX, pointY, _ in sections[elem]:
                posX = pointX - min_lon
                posY = pointY - min_lat
                ratioX = posX / (totalChangex)
                ratioY = posY / (totalChangey)
                if i == 0:
                        point1 = ((ratioX*18*unitW)+marginX, (ratioY*18*unitH)+marginY)
                else:
                    canvas.create_line(point1, ((ratioX*18*unitW)+marginX, (ratioY*18*unitH)+marginY), fill = rgb, width = 2.5)
                    point1 = ((ratioX*18*unitW)+marginX, (ratioY*18*unitH)+marginY)
                i += 1  
        j += 1