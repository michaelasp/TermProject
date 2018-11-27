from select import *
from tkinter import *
from models import *
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

def viewScreen(canvas, data):
    unitW = data.unitW
    unitH = data.unitH
    canvas.create_text(unitW*7, unitH*1, text = "Welcome " + data.name, anchor = NW, font = "Arial " + 
        str(int(unitH)))
    canvas.create_rectangle(unitW*6, unitH*18, unitW*14, unitH*20)
    canvas.create_text(unitW*7, unitH*18, text = "Input a new file", anchor = NW, font = "Arial " + 
        str(int(unitH)))

def viewAddGPX(canvas, data):
    unitW = data.unitW
    unitH = data.unitH
    for i in range(len(data.files)):
        canvas.create_text(unitW*7, unitH*2*i, text = data.files[i], anchor = NW, font = "Arial " + 
        str(int(unitH/2)))

        
    