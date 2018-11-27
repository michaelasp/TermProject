import string
from changeDB import *
from models import *

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
    selected = int((event.y // (2*unitH)) + data.currentPage * data.pageLength)
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
        data.gpxFiles = retrieveGPX(data)
        data.mode = "progress"

def mouseAddGPX(event, data):
    unitW = data.unitW
    unitH = data.unitH
    selected = int((event.y // (2*unitH)) + data.currentPage * data.pageLength)
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

def keyAddGPX(event, data):
    unitW = data.unitW
    unitH = data.unitH
    if event.keysym == "BackSpace":
        data.mode = "view"
    elif event.keysym == "Left":
        if data.currentPage > 0:
            data.currentPage -= 1
    elif event.keysym == "Right":
        if data.currentPage < data.totalPages:
            data.currentPage += 1

def keyLogin(event, data):
    unitW = data.unitW
    unitH = data.unitH
    if event.keysym == "BackSpace":
        data.mode = "select"
    elif event.keysym == "Left":
        if data.currentPage > 0:
            data.currentPage -= 1
            data.curUsers = retrieveUsers(data)
    elif event.keysym == "Right":
        if data.currentPage < data.totalPages:
            data.currentPage += 1
            data.curUsers = retrieveUsers(data)

