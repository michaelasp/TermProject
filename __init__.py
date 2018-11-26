import gpxpy
import os
import sqlite3
import string
from sqlite3 import Error
from tkinter import *
from changeDB import *
from createDB import *
from select import *


create_connection("db/user.db")
conn = sqlite3.connect("db/user.db")
select_gpx(conn, 3)
# Updated Animation Starter Code

from tkinter import *

####################################
# customize these functions
####################################

def init(data):
    data.mode = "select"
    data.unitW = data.width/20
    data.unitH = data.height/20
    data.newUser = ""

def mousePressed(event, data):
    unitW = data.unitW
    unitH = data.unitH
    if data.mode == "select":
        if unitW*2 <= event.x <= unitW * 9 and unitH * 5 <= event.y <= unitH *15:
            print("yes")
            data.mode = "create"
        elif unitW * 11 <= event.x <= unitW * 18 and unitH * 5 <= event.y <= unitH *15:
            print("no")



def keyPressed(event, data):
    if data.mode == "create":
        print(event.keysym)
        if event.keysym in string.ascii_uppercase or event.keysym in string.ascii_lowercase:
            data.newUser += event.keysym
        elif event.keysym == "BackSpace" and data.newUser != "":
            data.newUser = data.newUser[:-1]
        elif event.keysym == "Return" and data.newUser != '':
            data.id = add_user(conn, data.newUser)
            data.newUser = ""
            data.mode = "view"
             

def timerFired(data):
    pass

def redrawAll(canvas, data):
    if data.mode == "select":
        selectScreen(canvas, data)
    elif data.mode == "create":
        createScreen(canvas, data)

def selectScreen(canvas, data):
    unitW = data.unitW
    unitH = data.unitH

    canvas.create_rectangle(unitW*2, unitH*5, unitW*9, unitH*15)
    canvas.create_rectangle(unitW*11, unitH*5, unitW*18, unitH*15)

def createScreen(canvas, data):
    unitW = data.unitW
    unitH = data.unitH
    canvas.create_rectangle(unitW*4, unitH*8, unitW*16, unitH*12)
    canvas.create_text(unitW*5, unitH*9, text = data.newUser, anchor = NW, font = "Arial " + 
        str(int(unitH)))


def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1000, 750)