#This program will get songs from a youtube playlist and then download them to a music folder.

#Import Threading 
import threading

#Import Tkinter
import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import *
from tkinter import  *
from tkinter import DISABLED, Widget, ttk, Grid
from tkinter.messagebox import showinfo

#ffmpeg
import moviepy.editor as mp

#PIL
from PIL import Image

#Imports time
import time

#Importing Pytube
from pytube import YouTube, Playlist
from pytube import * 

from pyyoutube import Api


#Importing OS
import os
from os import link, listdir
from os.path import isfile, join

#Importing Random
import random

#import MTkinter
from mttkinter import mtTkinter as tk
from mttkinter import *


#Gets the urls of all the videos in the list
def PLChecker():
    global p
    PL_link = ytLink.get()
    #PL_link = PL_link.replace(r"\"", "/")
    p = Playlist(PL_link)
    
    
    titles = []
    #if isinstance(p):
    for vid in p.videos:
        titles.append(vid)
    
        

    #else: 
        #titles.append(vid)
    print(titles)
    return titles

def Downloader():
    global state
    
    downloadBtn["state"] = "disabled"
    
    downloading()
    
    folder = outputPath.get()
    #for every vid in p.videos 
    Bool = None
    
    for vid in p.videos:
        try:
            DV = vid.streams.filter(progressive=True).get_highest_resolution().download(output_path=folder)
            print(DV)
            base = os.path.splitext(DV)
            print(base)
           
            my_clip = mp.VideoFileClip(base[0] + ".mp4") 
            my_clip.audio.write_audiofile(base[0] + ".mp3")
            my_clip.close()
            
        
        except FileExistsError:
            os.remove(DV)
    
        else:
            os.remove(DV)

    print("Done")
    finish()


#Threads   
def threaders():
    titles = PLChecker()
    threads = []
    t = threading.Thread(target=Downloader)
    threads.append(t)
    t.start()


root = tk.Tk()
#Setting the title, background color, and size of the tkinter window and
root_height = 280
root_width=520
root.geometry(f"{root_width}x{root_height}")

root.title("YouTube Video Downloader")
root.config(background="PaleGreen1")


#Header for the page
heading=Label(root, text = "Youtube Video Downloader", padx=15, 
              pady=15, font="10")
heading.grid(row = 0, column = 1, pady=5, columnspan=3)

#Link Entry label
link=Label(root, text='Youtube Link')
link.grid( row=2, column=1, padx=10, pady=10)



#Variables for youtube and output path
ytLink = tk.StringVar()
outputPath = tk.StringVar()

#Playlist link, Entry
linkEntry = ttk.Entry(root, textvariable=ytLink, show='')
linkEntry.grid(row=2,column=2)
linkEntry.focus()

#File exstension chooser
options = [".mp3", ".mp4"]
clicked = StringVar()

clicked.set( ".mp3" )
drop = OptionMenu(root, clicked, *options)
drop.grid(row=2, column=3)
label = Label(root, text='')

#Output Location Entry
output=Label(root, text="Output to")
output.grid(row=3, column=1, padx=10, pady=10)
outputEntry = ttk.Entry(root, textvariable=outputPath)
outputEntry.grid(row=3, column=2)

def browse():
    #Sets download location
    downloadDirectory = filedialog.askdirectory(
        initialdir="Your Directory Path", title="Save Songs to")
    
    #Displays directory in text field
    outputPath.set(downloadDirectory)

#Browse Button
browser = ttk.Button(root, text="Browse", command=browse)
browser.grid(row=3, column=3)

#Download Button
downloadBtn = ttk.Button(root, text="Download", command=threaders)
downloadBtn.grid(row=4, column=2)

count = 0
moveinc = 0
movement = None
states = ["moving", "not_moving"]
moving_state = ["move_left", "move_right"]
idle_state = ["sleep", "idle"]
Finish = ["Downloading", "Finished"]
moving_file = ['images/DevelonFlyingFlipped.gif', 'images/DevelonFlying.gif']
idle_file = ['images/DevelonSleeping.gif', 'images/DevelonFlyingFlipped.gif']
sleep_file = 'images/DevelonSleepingIdle.gif'
complete_file = ["images/DownloadingDevelon.gif",'images/DevelonComplete.gif']

def zeroOut():
    global state, idle_action, movement, status, moveinc, count, moveinc, file, fileUsed, info, frames
    status = None
    moveinc = 0
    file = None
    fileUsed = None
    info = None
    frames = None
    idle_action = None
    movement = None
    finished = None
    count = 0

def eventChange():
    global state, idle_action, movement, status, moveinc
    #Develon Broad states
    state = None
    state = random.choice(states)

    #Develon specific States
    status = None
    idle_action = None
    movement = None
    finished = None
    #Checks if state is movement and then chooese a specific state from moving state

    if state == "moving":
        movement = random.choice(moving_state)
        #If specific state is left then put move inc to move develon left, opposite for move right
        if movement == "move_left":
            moveinc = -1
            status = 1

        elif movement == "move_right":
            moveinc = 1
            status = 1
        
    #if not moving then chooese between specific idling states
    else: 
        idle_action = random.choice(idle_state)
        if idle_action == "sleep":
   
            moveinc = 0
            status = 0
        elif idle_action == "idle":
 
            moveinc = 0


def animation(count):
    global anim
    frames = info.n_frames
    im2 = imgs[count]
    count += 1
    if count == frames:
        count = 0

    canvas.itemconfig(develon, image=im2)
    anim = root.after(100, lambda: animation(count))







def fileconfigs():
    #Globalization
    global file, fileUsed, state, status, idle_action, count

    file = None
    fileUsed = 0
    #File specific checker
    if state == "moving":
        if movement == "move_right":
            fileUsed = 0
            file = moving_file[fileUsed]
            count = 0

        elif movement == "move_left":
            fileUsed = 1
            file = moving_file[fileUsed]

    elif state != "moving":
        if idle_action == "sleep":
            fileUsed = 0
            file = idle_file[fileUsed]
        
        elif idle_action == "idle":
            fileUsed = 1
            file = idle_file[fileUsed]


def imageFileConfig():
    global frames, info, imgs
    info = Image.open(file)
    frames = info.n_frames
    imgs = [PhotoImage(file=file, format=f"gif -index {i}") for i in range(frames)]
    myImage = PhotoImage(file=file)
    canvas.itemconfigure(develon, image=myImage )

def createcanv():
    global frames, info, imgs, develon
    info = Image.open(file)
    frames = info.n_frames
    imgs = [PhotoImage(file=file, format=f'gif -index {i}') for i in range(frames)]
    myImage = PhotoImage(file=file)
    develon = canvas.create_image(startPosX-64,startPosY, image=myImage)

def next_gif():
    global imgs, fileUsed, file, count
    if state == "moving": 
        if movement == "move_left":
            count = 0
            fileUsed = 1
            file = moving_file[fileUsed]
            canvas.move(develon, -4, 0)

        elif movement == "move_right":
            count = 0
            fileUsed = 0
            file = moving_file[fileUsed]
            canvas.move(develon, 4, 0)

    elif state == "not_moving":
        if idle_action == "sleep":
            file = sleep_file
    imageFileConfig()

def move():
    global movement 
    xinc = 0
    xinc = moveinc
    change = 0
    flyingtime = random.randint(1,30)
    timeFlewn = 0
    
    while state == "moving" and timeFlewn != flyingtime:
        develonpos = canvas.coords(develon)
        timeFlewn += 1
        canvas.move(develon, xinc, 0)
        root.update()
        time.sleep(0.01)
        
        al = develonpos[0]
        if al < abs(xinc) or al > canvas_width - abs(xinc):
            change *= -1
            xinc = -xinc
            timeFlewn  += 1
            #print(timeFlewn)
            if al < abs(xinc):
                movement = "move_right"
            
            elif canvas_width - abs(xinc):
                movement = "move_left"
            next_gif()

def eventStarter():
    eventChange()
    fileconfigs()
    createcanv()
    animation(count)
    move()

def eventChanger(): 
    global evnchng
    eventChange()
    fileconfigs()
    next_gif()
    count = 0
    root.after_cancel(anim)
    animation(count)
    move()
    evnchng = root.after(2000, lambda: eventChanger())

def downloading():
    global count, file, fileUsed, moveinc
    zeroOut()
    root.after_cancel(anim) 
    file = complete_file
    
    fileUsed = 0
    file = file[fileUsed]
    imageFileConfig()
    count = 0
    animation(count)


def finish():
    zeroOut()
    root.after_cancel(evnchng)
    root.after_cancel(anim) 
    finishAnim()
    animation(count)
    showinfo(title=finish, message="Videos have been sucessfully downloaded")
    downloadBtn["state"] = "enabled"
    time.sleep(5)
    eventChanger()

def finishAnim():
    global count, file, fileUsed
    count = 0
    file = complete_file
    fileUsed = 1
    file = file[fileUsed]
    print("pleasework god damn it")
    imageFileConfig()
    

canvas_width = 200
canvas_height = 100
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="lightblue")
canvas.grid(row=1, column=2)

startPosX=100
startPosY=50

#Calling functions
eventStarter()
eventChanger()

root.mainloop()