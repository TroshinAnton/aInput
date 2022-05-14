#!/usr/bin/python
from tkinter import *
import serial
import time

root = Tk()
root.title("aInput")

port = "/dev/ttyUSB0" # Serial port
speed = 9600 # Serial port speed
max_len = 20 # Maximum number of characters per line
text_end = "~" # What to say at the end of input lines
default_text = "" # Initial text in the input field

ssize = StringVar()

def send_to_print(txt):
    arduino = serial.Serial(port, speed)
    arduino.write(txt.encode("utf-8"))
    arduino.close()
    time.sleep(0.5)

def nlen(txt):
    result_length = len(txt)
    for i in txt:
        if i.isdigit() or i.isupper(): 
            result_length += 1
    return result_length
	
def cut_to_print(txt):
    max_len = int(ssize.get())
    
    get = txt.split('\n')[:-1]
    result = []
    for st in get:
        if nlen(st) <= max_len:
            result.append(st)
        else:
            current = ""
            for i in st:
                if nlen(current+i) < max_len: current += i
                else:
                    result.append(current)
                    current = i
            if current != '':
                result.append(current)	
    result.append(text_end)
    for st in result:
        send_to_print(st)
	
	
def rollPaper():
    send_to_print('`')

def antiRollPaper():
    send_to_print('$')

name = Label(root, text = "aInput", font = "Calibri 20")
name.grid(row = 0)

inp = Text(root, width = 60, height = 20)
inp.grid(row = 1)
inp.insert(1.0, default_text)

start = Button(root, text = "Print", 
command = lambda:cut_to_print(inp.get(1.0, END)))
start.grid(row = 2, sticky = E)

clr = Button(root, text = "Clear", 
command = lambda:inp.delete(1.0, END))
clr.grid(row = 2, sticky = W)

roll = Button(root, text = "Roll",
command = lambda:rollPaper())
roll.grid(row = 3, sticky = W)

antiroll = Button(root, text = "Inversed Roll",
command = lambda:antiRollPaper())
antiroll.grid(row = 4, sticky = W)



cnt = Entry(root, textvariable=ssize, width=10)
cnt.grid(row = 3, sticky=E)
cnt.insert(0, str(max_len))


root.mainloop()
