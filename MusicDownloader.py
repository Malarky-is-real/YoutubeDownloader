#This program will get songs from a youtube playlist and then download them to a music folder.

#Import Threading 
from asyncio import threads
import queue
import threading

#Import Tkinter
import tkinter as tk
from tkinter.ttk import *
from tkinter import  *
from tkinter import DISABLED, Widget, ttk, Grid,filedialog
from tkinter.messagebox import showinfo
from tkinter.scrolledtext import ScrolledText
from webbrowser import get

#ffmpeg
import moviepy.editor as mp

#PIL
from PIL import Image

#URLlib import
import urllib.request
import urllib

#Imports time
import time

#Importing Pytube
from pytube import YouTube, Playlist
from pytube import * 

#Importing eye3d
import eyed3


#Importing OS
import os
from os import link
import shutil

#Importing Random
import random

#import MTkinter
from mttkinter import mtTkinter as tk
from mttkinter import *


#Gets the urls of all the videos in the list
def PLChecker():
    global songtitles 
    PL_link = None
    p = None
    PL_link = ytLink.get()
    playlistCheck = None
    
    o = open("links.txt", "w", encoding="utf-8")
    o.write(PL_link + "\n" + outputPath.get())
    o.close()
    if "list" in PL_link:
        p = Playlist(PL_link)
        playlistCheck =  True
    else:
        p = YouTube(PL_link)
        playlistCheck =  False

    songtitles = []
    if playlistCheck == True:
        for vid in p.videos:
            songtitles.append(vid)
    else:
        songtitles.append(p)

    
    return songtitles



def showVideos():
    global checkboxes, Videos
    Videos=Frame(root)
    Videos.destroy()
    checkboxes = []
    musictitles = PLChecker()
    
    root.geometry(f"800x{root_height+100}")
    Videos = ttk.Frame(root,height=280, width=240)
    
    textBox = ScrolledText(Videos, height=10, width=50)

    Videos.columnconfigure(1, weight=1)
    Videos.columnconfigure(1, weight=1)
    
    for vids in range (len(musictitles)):
        clickedNew = StringVar(value=clicked.get())
        currentVar = IntVar(value=1)
        title = musictitles[vids]
        
        current_box = ttk.Checkbutton(textBox, text=title.title, variable=currentVar)
        currentExten = OptionMenu(textBox, clickedNew, *options)
        
        textBox.window_create(END, window=current_box)
        textBox.window_create(END, window=currentExten)
        textBox.insert(END, "\n")
        
        current_box.var = currentVar
        currentExten.var = clickedNew
        
        checkboxes.append(current_box)
        checkboxes.append(currentExten)
        
    textBox['state'] = 'disabled'
    Videos.grid(column=4, row=1, columnspan=5)
    textBox.grid(row=0, column=1, sticky=N+S+W+E)
    ttk.Button(Videos, text="Final download", command=outPut).grid(column=1, row=1)
    
def outPut():
    Output = []
    songTitleFinal = []
    for box in range (0, len(checkboxes), 2):
        if checkboxes[box].var.get() == 1:
            Output.append(checkboxes[box]["text"])
            Output.append(checkboxes[box+1].var.get())

    for b in range (len(songtitles)):
        for i in range (len(Output)):
            if songtitles[b].title == Output[i] and songtitles[b] not in songTitleFinal:
                songTitleFinal.append(songtitles[b])
                songTitleFinal.append(Output[i+1])

    Videos.destroy()
    zeroOut()
    root.geometry(RootSize)
    root.after_cancel(evnchng)
    root.after_cancel(anim) 
    downloadAnim()
    count = 0
    animation(count)
    threaders(songTitleFinal)
           
    
#Threads are where the downloader starts  
q = queue.Queue()
def threaders(songsTBD):
    threading.Thread(target=Downloader, args=(q,), daemon=True).start()
    for t in range(0, len(songsTBD), 2):
        ex = t + 1
        q.put([songsTBD[t], songsTBD[ex]])
    q.put([None])
    
    
    
    
        
    

    


def downloadThumbnail(url: str, dest_folder: str, fileName: str):
    if "/" in fileName:
        fileName = fileName.replace(r"/", "-")
    if '"' in fileName:
        fileName = fileName.replace(r'"', '')
    if "|" in fileName:
        fileName = fileName.replace(r"|", "-")
    if "+" in fileName:
        fileName = fileName.replace(r"+", "-")
    if  "?" in fileName:
        fileName = fileName.replace(r"?", "-")
    if  "[" in fileName and "]" in fileName:
        fileName = fileName.replace(r"[", "(")
        fileName = fileName.replace(r"]", ")")
    fullpath = dest_folder + fileName + ".jpg"
    
    # Use wget download method to download specified image url.
    finaltmbn = urllib.request.urlretrieve(url, fullpath)
    return fullpath, finaltmbn

def thumbnailChanger(video, path):
    audiofile = eyed3.load(video)
    if (audiofile.tag == None):
        audiofile.initTage()

    audiofile.tag.images.set(3, open(path, 'rb').read(), 'image/jpeg')
    audiofile.tag.save(version=eyed3.id3.ID3_V2_3)
    

#The code for the actual video downloader

def Downloader(q):
    global state
    while True:
        values = q.get()
        
        if values[0] == None:
            break
        else:
            vid = values[0]
            exten = values[1]
        downloadBtn["state"] = "disabled"
        folder = outputPath.get()
        try:
            #Downloads the videos
            DV = vid.streams.filter(progressive=True).get_highest_resolution().download(output_path="tempSongsFolder/", skip_existing=True)
            base = os.path.splitext(DV)
        
        except FileExistsError:
            print("uh oh")
        
        #Converts video to mp3 if mp3 is selected, adds a thumbnail, and changes the author
        else:
            fullFile = base[0] + exten
            print(fullFile)
            if exten == ".mp3":
                my_clip = mp.VideoFileClip(base[0] + ".mp4") 
                my_clip.audio.write_audiofile(fullFile)
                my_clip.close()
                #Creates a thumbnail and adds the authors name
                os.remove(DV)
                vidName = vid.title
                thumbnail = vid.thumbnail_url 
                img_path, finalImg = downloadThumbnail(thumbnail, "thumbnails/", vidName)
                thumbnailChanger(fullFile, img_path)
                os.remove(finalImg[0])
                audiofile = eyed3.load(fullFile)
                audiofile.tag.artist = vid.author          
        
        vidTitle = vid.title
        if ":" in vidTitle:
            vidTitle = vidTitle.replace(r":", "-")
        if "/" in vidTitle:
            vidTitle = vidTitle.replace(r"/", "-")
        if '"' in vidTitle:
            vidTitle = vidTitle.replace(r'"', '')
        if "|" in vidTitle:
            vidTitle = vidTitle.replace(r"|", "-")
        if "+" in vidTitle:
            vidTitle = vidTitle.replace(r"+", "-")
        if  "?" in vidTitle:
            vidTitle = vidTitle.replace(r"?", "-")
        if  "[" in vidTitle and "]" in vidTitle:
            vidTitle = vidTitle.replace(r"[", "(")
            vidTitle = vidTitle.replace(r"]", ")")
            
        destinationPath = os.path.join(folder, vidTitle + exten)
        
        shutil.move(fullFile, destinationPath)
        q.task_done()
    q.task_done()
    q.join()
    finish()


root = tk.Tk()
#Setting the title, background color, and size of the tkinter window and
root_height = 280
root_width=520
RootSize = root.geometry(f"{root_width}x{root_height}") 

root.title("YouTube Video Downloader")
root.config(background="PaleGreen1")


#Header for the page
heading=Label(root, text = "Youtube Video Downloader", padx=15, 
              pady=15, font="10")
heading.grid(row = 0, column = 1, pady=5, columnspan=3)

#Link Entry label
link=Label(root, text='Youtube Link')
link.grid( row=2, column=1, padx=10, pady=10)

saves = open
f = open("Links.txt", "r")

#Variables for youtube and output path
ytLink = tk.StringVar()
outputPath = tk.StringVar()
ytLink.set(f.readline())
outputPath.set(f.readline())
f.close()
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
downloadBtn = ttk.Button(root, text="Download", command=showVideos)
downloadBtn.grid(row=4, column=2)


def zeroOut():
    global state, idle_action, movement, moveinc, count, moveinc, file, fileUsed, info, frames
    moveinc = 0
    file = None
    fileUsed = None
    info = None
    frames = None
    idle_action = None
    movement = None
    count = 0

zeroOut()
state = None
states = ["moving", "not_moving"]
moving_state = ["move_left", "move_right"]
idle_state = ["sleep", "idle"]
moving_file = ['images/DevelonFlyingFlipped.gif', 'images/DevelonFlying.gif']
idle_file = ['images/DevelonSleeping.gif', 'images/DevelonFlyingFlipped.gif', 'images/DevelonSleepingIdle.gif']
downloading_files = ["images/DownloadingDevelon.gif",'images/DevelonComplete.gif']
tempState = None


def eventChange():
    global state, idle_action, movement, moveinc
    #Develon Broad states


    tempState = random.choice(states)
    
    while tempState == state: 
        tempState = random.choice(states)
    
    state = tempState
    
    
    idle_action = None
    movement = None
    
    #Checks if state is movement and then chooese a specific state from moving state
    if state == "moving":
        tempState2 = random.choice(moving_state)
        
        while tempState2 == state: 
            tempState2 = random.choice(moving_state)
        movement = tempState2
        
        #If specific state is left then put move inc to move develon left, opposite for move right
        if movement == "move_left":
            moveinc = -1

        else:
            moveinc = 1
        
    #if not moving then chooese between specific idling states
    else: 
        tempState3 = random.choice(idle_state)
        while tempState3 == idle_action:
            tempState3 = random.choice(idle_state)
        idle_action = tempState3
        moveinc = 0


def animation(count):
    global anim, file, fileUsed, idle_action
    im2 = imgs[count]
    count += 1
    if idle_action == "sleep" and count == frames:
        idle_action = "sleep2"
        next_gif()
    else:        
        if count == frames:
            count = 0
    
    canvas.itemconfig(develon, image=im2)
    anim = root.after(100, lambda: animation(count))


def fileconfigs():
    #Globalization
    global file, fileUsed, state, idle_action, count
    #File specific checker
    if state == "moving":
        if movement == "move_right":
            fileUsed = 0
            file = moving_file[fileUsed]
            count = 0

        elif movement == "move_left":
            fileUsed = 1
            file = moving_file[fileUsed]
            count = 0

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
    canvas.itemconfigure(develon, image=myImage)

def createcanv():
    global frames, info, imgs, develon
    info = Image.open(file)
    frames = info.n_frames
    imgs = [tk.PhotoImage(file=file, format=f'gif -index {i}') for i in range(frames)]
    myImage = tk.PhotoImage(file=file)
    develon = canvas.create_image(startPosX-64,startPosY, image=myImage)

def next_gif():
    global imgs, fileUsed, file, count
    if state == "moving": 
        if movement == "move_left":
            count = 0
            fileUsed = 1
            file = moving_file[fileUsed]
            canvas.move(develon, -10, 0)

        elif movement == "move_right":
            count = 0
            fileUsed = 0
            file = moving_file[fileUsed]
            canvas.move(develon, 10, 0)

    elif state == "not_moving":
        if idle_action == "sleep":
            file = 'images/DevelonSleeping.gif'
            
        elif idle_action == "sleep2":
            file = 'images/DevelonSleepingIdle.gif'            
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

def downloadAnim():
    global count, file, fileUsed
    count = 0
    file = downloading_files
    fileUsed = 0
    file = file[fileUsed]
    imageFileConfig()


def finish():
    
    zeroOut()
    root.after_cancel(anim) 
    finishAnim()
    animation(count)
    showinfo(title=finish, message="VIideos have been sucessfully downloaded")
    downloadBtn["state"] = "enabled"
    time.sleep(5)
    zeroOut()
    eventChanger()

def finishAnim():
    global count, file, fileUsed
    count = 0
    file = downloading_files
    fileUsed = 1
    file = file[fileUsed]
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