import string
from changeDB import *
from models import *
from image_util import *

def mouseSelect(event, data):
    unitW = data.unitW
    unitH = data.unitH
    if unitW * 2 <= event.x <= unitW * 9 and unitH * 5 <= event.y <= unitH * 15:
        print("yes")
        data.mode = "create"
    elif unitW * 11 <= event.x <= unitW * 18 and unitH * 5 <= event.y <= unitH * 15:
        print("no")
        data.curUsers = retrieveUsers(data)
        print(data.curUsers)
        data.mode = "login"

def mouseLogin(event, data):
    unitW = data.unitW
    unitH = data.unitH
    selected = int((event.y // (2*unitH)))
    if selected <= len(data.curUsers) - 1:
        data.id = data.curUsers[selected][0]
        data.name = data.curUsers[selected][1]
        data.mode = "view"
        data.currentPage = 0

def mouseView(event, data):
    unitW = data.unitW
    unitH = data.unitH
    if unitW * 7 <= event.x <= unitW * 13 and unitH * 18 <= event.y <= unitH * 20:
        data.files = retrieveFiles(data)
        data.mode = "addGPX"
    elif unitW * 1 <= event.x <= unitW * 8 and unitH * 7 <= event.y <= unitH * 13:
        retrieveGPXMiles(data)
        data.mode = "progress"
    elif unitW * 12 <= event.x <= unitW * 19 and unitH * 7 <= event.y <= unitH * 13:
        data.curRides = retrieveRides(data)
        data.mode = "pickRecommend"

def mouseAddGPX(event, data):
    unitW = data.unitW
    unitH = data.unitH
    selected = int((event.y // (2*unitH)))
    print(data.files)
    if selected <= len(data.files) - 1:
        if "." not in data.files[selected]:
            if data.path == ".":
                data.path = data.files[selected] + "/"
            else:
                data.path += data.files[selected] + "/"
        else:
            print("yes")
            addGPX(data, selected)
    data.files = retrieveFiles(data)

def mouseProgress(event, data):
    unitW = data.unitW
    unitH = data.unitH
    if unitW * 12 <= event.x <= unitW * 19 and unitH * 7 <= event.y <= unitH * 13:
        data.curRides = retrieveRides(data)
        data.mode = "pickRide"
        data.viewSeg = False
    elif unitW * 1 <= event.x <= unitW * 8 and unitH * 7 <= event.y <= unitH * 13:
        data.curRides = retrieveRides(data)
        data.mode = "pickRide"
        data.viewSeg = True        
        
def mouseRides(event, data):
    unitW = data.unitW
    unitH = data.unitH
    selected = int((event.y // (2*unitH)))
    if selected <= len(data.curRides) - 1:
        data.plot = data.curRides[selected]
        if data.viewSeg == False:
            data.mode = "plot"
        else:
            data.mode = "viewSeg"
            (_,_,gpxFile,_, min_lat, min_lon, max_lat, max_lon,_) = data.plot
        data.sections = findSections(data.plot)

def mousePickRecommend(event, data):
    unitW = data.unitW
    unitH = data.unitH
    selected = int((event.y // (2*unitH)))
    if selected <= len(data.curRides) - 1:
        data.picked = data.curRides[selected]
        data.mode = "recommend"
        data.trailType = 0
        data.sections = findSections(data.picked)
        data.colors = {0:"red", 1:"black", 2:"black"}

def mouseCreate(event, data):
    unitW = data.unitW
    unitH = data.unitH
    if unitW * 7 <= event.x <= unitW * 13 and unitH * 18 <= event.y <= unitH * 20:
        data.newUser = ""
        data.mode = "select"


def keyCreate(event, data):
    unitW = data.unitW
    unitH = data.unitH
    print(event.keysym)
    if event.keysym in string.ascii_uppercase or event.keysym in string.ascii_lowercase:
        data.newUser += event.keysym
    elif event.keysym == "BackSpace" and data.newUser != "":
        data.newUser = data.newUser[:-1]
    elif event.keysym == "Return" and data.newUser != '':
        data.id = add_user(data.conn, data.newUser)
        data.name = data.newUser
        data.newUser = ""
        data.mode = "view"

def keyAddGPX(event, data):
    unitW = data.unitW
    unitH = data.unitH
    if event.keysym == "BackSpace":
        data.mode = "view"
        data.currentPage = 0
    elif event.keysym == "Left":
        if data.currentPage > 0:
            data.currentPage -= 1
            data.files = retrieveFiles(data)
    elif event.keysym == "Right":
        if data.currentPage < data.totalPages:
            data.currentPage += 1
            data.files = retrieveFiles(data)

def keyLogin(event, data):
    unitW = data.unitW
    unitH = data.unitH
    if event.keysym == "BackSpace":
        data.mode = "select"
        data.currentPage = 0
    elif event.keysym == "Left":
        if data.currentPage > 0:
            data.currentPage -= 1
            data.curUsers = retrieveUsers(data)
    elif event.keysym == "Right":
        if data.currentPage < data.totalPages:
            data.currentPage += 1
            data.curUsers = retrieveUsers(data)


def keyRides(event, data):
    unitW = data.unitW
    unitH = data.unitH
    if event.keysym == "BackSpace":
        data.mode = "progress"
        data.currentPage = 0
    elif event.keysym == "Left":
        if data.currentPage > 0:
            data.currentPage -= 1
            data.curRides = retrieveRides(data)
    elif event.keysym == "Right":
        if data.currentPage < data.totalPages:
            data.currentPage += 1
            data.curRides = retrieveRides(data)

def keyPickReccomend(event, data):
    unitW = data.unitW
    unitH = data.unitH
    if event.keysym == "BackSpace":
        data.mode = "view"
        data.currentPage = 0
    elif event.keysym == "Left":
        if data.currentPage > 0:
            data.currentPage -= 1
            data.curRides = retrieveRides(data)
    elif event.keysym == "Right":
        if data.currentPage < data.totalPages:
            data.currentPage += 1
            data.curRides = retrieveRides(data)

def keyProgress(event, data):
    if event.keysym == "BackSpace":
        data.mode = "view"

def keyPlot(event, data):
    if event.keysym == "BackSpace":
        data.mode = "pickRide"

def keyReccomend(event, data):
    if event.keysym == "BackSpace":
        data.mode = "pickRecommend"
    elif event.keysym == "Left":
        if data.trailType > 0:
            data.colors[data.trailType] = "black"
            data.trailType -= 1
            data.colors[data.trailType] = "red"
    elif event.keysym == "Right":
        if data.trailType < 2:
            data.colors[data.trailType] = "black"
            data.trailType += 1
            data.colors[data.trailType] = "red"
    print(data.trailType)

def keyViewSeg(event, data):
    if event.keysym == "BackSpace":
        data.mode = "pickRide"

def keyView(event, data):
    if event.keysym == "BackSpace":
        data.mode = "select"
        data.id = 0
        data.name = ""
        data.newUser = ""
