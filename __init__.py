import gpxpy
import os
import sqlite3
from sqlite3 import Error
from tkinter import *
from createDB import *
from views import *
from controllers import *
from models import *
from tkinter import *

def init(data):
    data.mode = "select"
    data.unitW = data.width/20
    data.unitH = data.height/20
    data.newUser = ""
    data.conn = create_connection("db/user.db")
    data.path = "."
    data.pageLength = 10
    data.currentPage = 0
    data.users = select_users(data.conn)

def mousePressed(event, data):
    if data.mode == "select":
        mouseSelect(event, data)
    elif data.mode == "view":
        mouseView(event, data)
    elif data.mode == "login":
        mouseLogin(event, data)
    elif data.mode == "addGPX":
        mouseAddGPX(event, data)

def keyPressed(event, data):
    if data.mode == "create":
        keyCreate(event, data)
    elif data.mode == "addGPX":
        keyAddGPX(event, data)
    elif data.mode == "login":
        keyLogin(event, data)

def timerFired(data):
    pass

def redrawAll(canvas, data):
    if data.mode == "select":
        selectScreen(canvas, data)
    elif data.mode == "create":
        createScreen(canvas, data)
    elif data.mode == "login":
        viewLogin(canvas, data)
    elif data.mode == "view":
        viewScreen(canvas, data)
    elif data.mode == "addGPX":
        viewAddGPX(canvas, data)
    elif data.mode == "progress":
        viewProgress(canvas, data)


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