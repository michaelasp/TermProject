import string
from changeDB import *
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
    if unitW*2 <= event.x <= unitW * 9 and unitH * 5 <= event.y <= unitH *15:
        print("yes")
        data.mode = "create"
    elif unitW * 11 <= event.x <= unitW * 18 and unitH * 5 <= event.y <= unitH *15:
        print("no")

def mouseView(event, data):
    unitW = data.unitW
    unitH = data.unitH
    if unitW*7 <= event.x <= unitW * 13 and unitH * 18 <= event.y <= unitH *20:
        data.files = retrieveFiles(data)
        data.mode = "addGPX"

def mouseAddGPX(event, data):
    unitW = data.unitW
    unitH = data.unitH
    selected = int((event.y // (2*unitH)) + data.currentPage * data.pageLength)
    if selected <= len(data.files) - 1:
        if "." not in data.files[selected]:
            if data.path == ".":
                data.path = data.files[selected] + "/"
    print(selected)



