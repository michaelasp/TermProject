from tkinter import *
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

def viewProgress(canvas, data):
    unitW = data.unitW
    unitH = data.unitH
    canvas.create_text(unitW*5, unitH*9, text = "You have done " + str(data.totalMiles) + " Miles", anchor = NW, font = "Arial " + 
        str(int(unitH/4)))
    canvas.create_text(unitW*5, unitH*10, text = "You have done " + str(len(data.totalRides)) + " Activities", anchor = NW, font = "Arial " + 
        str(int(unitH/4)))
    canvas.create_rectangle(unitW*12, unitH*7, unitW*19, unitH*13)
    canvas.create_text(unitW*13, unitH*9, text = "View Activities", anchor = NW, font = "Arial " + 
        str(int(unitH/1.5)))

def viewRides(canvas, data):
    unitW = data.unitW
    unitH = data.unitH
    for i in range(len(data.curRides)):
        canvas.create_text(unitW*7, unitH*2*i, text = data.curRides[i][1], anchor = NW, font = "Arial " + 
        str(int(unitH/2)))

def viewLogin(canvas, data):
    unitW = data.unitW
    unitH = data.unitH
    for i in range(len(data.curUsers)):
        canvas.create_text(unitW*7, unitH*2*i, text = data.curUsers[i][1], anchor = NW, font = "Arial " + 
        str(int(unitH/2)))    

def plotPoints(canvas, data):
    unitW = data.unitW
    unitH = data.unitH
    marginX = unitW
    marginY = unitH
    (_,_,gpxFile,_, min_lat, min_lon, max_lat, max_lon,_) = data.plot
    totalChangex = max_lat - min_lat
    totalChangey = max_lon - min_lon
    gpx = gpxpy.parse(gpxFile)
    i=0
    point1 = None
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                posX = point.latitude - min_lat
                posY = point.longitude - min_lon
                #posX, posY = float("%.3f" % (2 * posX)), float("%.3f" % (2 * posY))

                ratioX = posX / (totalChangex)
                ratioY = posY / (totalChangey)
                if i == 0:
                    point1 = ((ratioX*18*unitW)+marginX, (ratioY*18*unitH)+marginY)
                else:
                    canvas.create_line(point1, ((ratioX*18*unitW)+marginX, (ratioY*18*unitH)+marginY))
                    point1 = ((ratioX*18*unitW)+marginX, (ratioY*18*unitH)+marginY)
                i += 1
    sections = findSections(data)
    j = 0
    for section in sections:
        i = 0
        for point in section:
            r = (255 - 50 * j)%255 
            rgb = rgbString(r, 255-r, 0)
            ratioX, ratioY = point
            ratioX /= totalChangex
            ratioY /= totalChangey
            if i == 0:
                    point1 = ((ratioX*18*unitW)+marginX, (ratioY*18*unitH)+marginY)
                    canvas.create_text(point1, text = "here" + str(j))
            else:
                canvas.create_line(point1, ((ratioX*18*unitW)+marginX, (ratioY*18*unitH)+marginY), fill = rgb, width = 2)
                point1 = ((ratioX*18*unitW)+marginX, (ratioY*18*unitH)+marginY)
            i += 1
        j += 1
        
def plotDifficulty(canvas, data):
    unitW = data.unitW
    unitH = data.unitH
    marginX = unitW
    marginY = unitH
    (_,_,gpxFile,_, min_lat, min_lon, max_lat, max_lon,_) = data.picked
    totalChangex = max_lat - min_lat
    totalChangey = max_lon - min_lon
    gpx = gpxpy.parse(gpxFile)
    i=0
    elevationChange = 0
    elevation = 0
    point1 = None
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                posX = point.latitude - min_lat
                posY = point.longitude - min_lon
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
    pass



    