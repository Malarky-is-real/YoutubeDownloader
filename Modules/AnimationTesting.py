#This program will get songs from a youtube playlist and then download them to a music folder.

#Import Tkinter
import animations as anim
import tkinter as tk
from tkinter.ttk import *
from tkinter import  *
from tkinter import DISABLED, Widget, ttk, Grid,filedialog
from tkinter.messagebox import showinfo

#PIL
from PIL import Image

#Imports time
import time

#Importing Random
import random

#import MTkinter
from mttkinter import mtTkinter as tk
from mttkinter import *

root = tk.Tk()
#Setting the title, background color, and size of the tkinter window and
root_height = 240
root_width=400
RootSize = root.geometry(f"{root_width}x{root_height}")

root.title("Animation Testing")
root.config(background="PaleGreen1")

#Header for the page
heading=Label(root, text = "Animation Testing")
heading.grid(row = 0, column = 2)


#DevelonWindow Set up
canvas_width = 200
canvas_height = 100
buttonFrame = tk.Frame(root, bg='red', width=canvas_width, height=canvas_height)
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, background="lightblue")
canvas.grid(row=1, column=2, sticky=NSEW, padx=100)
canvas.create_rectangle(0, 81, 220, 150, fill="red")

startPosX=100
startPosY=50


actions = ["idle", "move_left", "sleep", "move_right"]
stick = ["E", "W", "S", "N"]

#Download Button
#downloadBtn = ttk.Button(root, text="Download", command=showVideos)
#downloadBtn.grid(row=4, column=2)

develon = anim.petAnimations(root, canvas)
column = 0
row = 0
stick   
for i in range(len(actions)):
    
    if i >= 2:
        button = tk.Button(buttonFrame, text=actions[i], command=lambda k = i: develon.eventVerify(actions[k])).grid(row=(i-2), column=2,  sticky="W")
        
    elif i < 2:
        button = tk.Button(buttonFrame, text=actions[i], command=lambda k = i: develon.eventVerify(actions[k])).grid(row=i, column=0, sticky="E")
    



buttonStart = tk.Button(buttonFrame, text="Event Start", command=lambda: develon.eventStarter(action = None)).grid(row=0, column=1)
buttonStop = tk.Button(buttonFrame, text="Event Stop", command=lambda: develon.eventStopper()).grid(row=1, column=1)
button = tk.Button(buttonFrame, text="Err_Animat", command=lambda: develon.next_gif("ERR")).grid(row=2, column=0, sticky="E")
button = tk.Button(buttonFrame, text="Down_Finish", command=lambda: develon.finish()).grid(row=2, column=2, sticky="E")
button = tk.Button(buttonFrame, text="Download", command=lambda: develon.downloadAnim()).grid(row=2, column=1)


buttonFrame.grid(column=2, row=2, columnspan=2, rowspan=2)
root.mainloop()

