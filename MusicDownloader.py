#This program will get songs from a youtube playlist and then download them to a music folder.

#Import Threading 
import queue, threading

#Import Tkinter
import tkinter as tk
from tkinter.ttk import *
from tkinter import  *
from tkinter import DISABLED, Widget, ttk, filedialog
from tkinter.messagebox import *
from tkinter.scrolledtext import ScrolledText

#ffmpeg
import moviepy.editor as mp

#PIL


#URLlib import
#URLlib import
import urllib.request
import urllib

#Imports time
import time

#Importing Pytube
from pytube import YouTube, Playlist
from pytube import * 
from pytube import extract
import pytube.request

#Importing eye3
import eyed3

#Importing OS
import os
from os import link 
import shutil
import requests

#Importing Random
import random

#import MTkinter
from mttkinter import mtTkinter as tk
from mttkinter import *

#Modules
from Modules.Spot import * 

#importing Json
import json

from bs4 import BeautifulSoup as bs # importing BeautifulSoup

from Modules.YouTubeApi import *

import Modules.download as download

#Functions at the top non functions at the very bottom

#Gets the urls of all the videos in the list
def loadData(ran):
    #Variable initialization
    songsNames = []
    locationNames = []
    playlistName = []
    
    #Opens up the json file and gets all the data
    with open('TextFiles/Links.json', 'r') as json_file:
        data = json.load(json_file)
    
    #Seperates data by the important features
    songLinks = data['songs'][0]['song']
    locationPath = data['songs'][0]['outputs']
    playlistInfo = data['playlistStuff'][0]['playlist']
    
    #Seperates the video links into their respective locations
    for music in songLinks:
        try: 
            if "www.youtube.com/playlist?list" in music or "&list" in music:
                songsNames.append(Playlist(music).title + " - Youtube Playlist")
            
            elif "https://open.spotify.com/playlist" in music:
                songsNames.append(getPlaylistName(music) + " - Spotify Playlist")

            elif "open.spotify.com/album" in music:
                songsNames.append(getAlbumName(music) + " - Spotify Album")
            
            else:
                
                songsNames.append(getTitle(extract.video_id(music)) + " - " + YouTube(music, use_oauth=True, allow_oauth_cache=True ).author)
        except:
            if "www.youtube.com/playlist?list" in music or "&list" in music:
                songsNames.append("Youtube Playlist")
            
            elif "https://open.spotify.com/playlist" in music:
                songsNames.append("Spotify Playlist")

            elif "open.spotify.com/album" in music:
                songsNames.append("Spotify Album")
            else:
                songsNames.append("Youtube Video")
            continue

    for locations in locationPath:
        locationNames.append(os.path.basename(locations))
    

    if ran == 1:
        linkEntry['values'] = songsNames
        outputEntry['values'] = locationNames
        playlistLinkEntry.insert(0, playlistInfo)
        playlistOutputEntry['values'] = locationNames
    
    return songsNames, songLinks, locationNames, locationPath, playlistInfo, playlistName, data

def jsonUpdate(bigvalue,  value, widget = None, list= None, widgetGet = None ): 
    
    if bigvalue == "songs":
        if widget.get() not in list:
            list.append(widget.get())
            data[bigvalue][0][value] = list
            music = json.dumps(data, indent = 4)
            with open('TextFiles/Links.json', 'w') as outfile:
                outfile.write(music)
    
    else: 
        data[bigvalue][0][value] = widgetGet
        music = json.dumps(data, indent = 4)
        with open('TextFiles/Links.json', 'w') as outfile:
            outfile.write(music)
    
    loadData(1)

def showLinks():    
    def deleteLinksSelected (event):
        def delete(event):
            nameLinkShower.delete(currItem)
            nameLinkShower.selection_clear()
             
        main.bind('<BackSpace>', delete)
        currItem = nameLinkShower.selection()[0] 
    def finishUp(event):
        songLinks = []
        locationPath = []
        
        for line in nameLinkShower.get_children():
            for value in range(len(nameLinkShower.item(line)['values']) - 1):
                nameLinkShower.item(line)['values'][value + 1]
                if 'https://www.youtube.com' in nameLinkShower.item(line)['values'][value + 1] or 'https://open.spotify.com' in nameLinkShower.item(line)['values'][value + 1] or "https://youtu.be" in nameLinkShower.item(line)['values'][value + 1]: 
                    songsNames.append(nameLinkShower.item(line)['values'][value])
                    songLinks.append(nameLinkShower.item(line)['values'][value  + 1])

                else:
                    locationNames.append(nameLinkShower.item(line)['values'][value])
                    locationPath.append(nameLinkShower.item(line)['values'][value  + 1])
                    
        main.unbind('<Return>')
        main.unbind('<BackSpace>')
        nameLinkShower.unbind('<<TreeviewSelect>>')
        nameLinkShower.destroy()
        main.geometry(f"{Main_width}x{Main_height}") 
        noteBook.config(width=Main_width, height=Main_height)
        root.config(width=Main_width, height=Main_height)
        data['songs'][0]['song'] = songLinks
        data['songs'][0]['outputs'] = locationPath
        music = json.dumps(data, indent = 4)

        with open('TextFiles/Links.json', 'w') as outfile:
            outfile.write(music)
        MainMenu.entryconfigure(1, state=ACTIVE)
        loadData(1)
    
    MainMenu.entryconfigure(1, state=DISABLED)
    main.geometry(f"950x{Main_height+120}")
    root.config(width=950, height=Main_height+120)
    noteBook.config(width=950, height=Main_height+120)
    
    shownElements = []
    columns = ("Name", "Link/Location")
    nameLinkShower = ttk.Treeview(root, columns=columns, show='headings')
    nameLinkShower.heading('Name', text="Song/Location Names")
    nameLinkShower.heading('Link/Location', text="Links/Full Location")
    
    
    for songName in range(len(songsNames)):
        shownElements.append((f'{songsNames[songName]}', f'{songLinks[songName]}'))

    for locs in range(len(locationNames)):
            shownElements.append((f'{locationNames[locs]}', f'{locationPath[locs]}'))
    
    for info in shownElements:
        nameLinkShower.insert('', tk.END, values=info)
    
    main.bind('<Return>', finishUp)    
    nameLinkShower.bind('<<TreeviewSelect>>', deleteLinksSelected)
    nameLinkShower.grid(column=4, row=1, columnspan=5, sticky=N+S+W+E)


#Lets you browse for the folder you want to put the songs in. 
def browse(frame):
    #Sets download location
    downloadDirectory = filedialog.askdirectory(initialdir="Your Directory Path", title="Save Songs to")
    
    #Displays directory in text field
    if frame == root:
        outputPath.set(downloadDirectory)
    elif frame == root2:
        playlistOutputEntry.set(downloadDirectory)

def PLChecker():
    global songUrl, outputLocation, p, PL_link, showVids
    
    PL_link = None
    p = None
    songUrl = []

    if linkEntry.get() == "" or outputEntry.get() == "":
        showwarning(title = "Empty", message="Do not leave the textboxes empty!" )
        return 
    
    if linkEntry.get() in songsNames or linkEntry.get() in songLinks: 
        PL_link = songLinks[linkEntry.current()]
        
        
    else:
        PL_link = linkEntry.get()
        jsonUpdate('songs', 'song', linkEntry, songLinks,widgetGet=PL_link )
    
    
    #Puts the video/playlist link as well as folder link in a links.txt for auto input. 
    if outputEntry.get() in locationNames:
        outputLocation = locationPath[outputEntry.current()]
        
    else:
        outputLocation = outputEntry.get()
        jsonUpdate('songs', 'outputs', outputEntry, locationPath, widgetGet=outputLocation)
        

    #checks what site the link is from and uses the proper methods to prepare for downloading.
    if "spotify" in PL_link:
        songUrl = spotiPlaylistDownload(PL_link)
    
    elif "list" in PL_link:
        p = Playlist(PL_link)
        titleOrig = p.title
        for vid in range(len(p.videos)):
            link = p.video_urls[vid]
            vidUrl = YouTube(link, use_oauth=True, allow_oauth_cache=True)
            songUrl.append(vidUrl)

    elif "youtu" in PL_link:
        p = YouTube(PL_link, use_oauth=True, allow_oauth_cache=True)
        titleOrig = getTitle(extract.video_id(p.watch_url))
        songUrl.append(p)
        
    if showVideos.alreadyExist == False:
        showVids = showVideos(songUrl) 
          
    elif showVideos.alreadyExist == True:
        
        addtoList = askyesnocancel("Crossroads", f"Would you like to add {titleOrig} to your songsTBD? \n cancel to replace the current selection with the new one")
        
        if addtoList == True:
            showVids.addon(songUrl)
            return 
        
        elif addtoList == False:
            return     
        
        else:
            showVids = showVideos(songUrl)   
    
    showVids.mainShow()
    
#Shows the videos in a box to the right
class showVideos(object):
    def __init__(self, mT = []):
        self.musictitles = mT     
    
    #Shows all the songs in a box
    def mainShow(self):
        global checkboxes, Videos, musicBoxes
        
        
        if showVideos.alreadyExist == True:
            Videos.destroy()

        Videos=Frame(main)
        showVideos.alreadyExist = True
        
        checkboxes = []
        musicBoxes = []
        
        #set up variables for the videos box. 
        main.geometry(f"1100x{Main_height}")
        Videos = ttk.Frame(main,height=280, width=240, )
        textBox = ScrolledText(Videos, height=10, width=50)
        #Videos.columnconfigure(1, weight=1)
        
        #Puts the video(s) into a box for display and lets you choose which ones to download, what type of file it'll be, and gives the option to change the video link
        nums = len(self.musictitles)
        for vids in range (nums):
            clickedNew = StringVar(value=clicked.get())
            currentVar = IntVar(value=1)
            
            tempTitle = getTitle(extract.video_id(self.musictitles[vids].watch_url))
            if len(tempTitle) > 41:
                title = f'{tempTitle[0:38]}...'
            else:
                title = tempTitle
                
            current_box = ttk.Checkbutton(textBox, text=title, variable=currentVar)
            currentExten = OptionMenu(textBox, clickedNew, *options)
            vidLinkButton = ttk.Button(textBox, text=vids+1, command= lambda k = vids:  self.changeLink(k, self.musictitles))
            
            textBox.window_create(END, window=current_box)
            textBox.window_create(END, window=currentExten)
            textBox.window_create(END, window=vidLinkButton)
            textBox.insert(END, "\n")
            
            current_box.var = currentVar
            currentExten.var = clickedNew
            
            musicBoxes.append(current_box)
            checkboxes.append(currentExten)
            
        textBox['state'] = 'disabled'
        Videos.grid(column=4, row=0, columnspan=4, padx=25)

        textBox.grid(row=0, column=1, sticky=N+S+W+E)
        ttk.Button(Videos, text="Final download", command=self.outPut).grid(column=1, row=1)
    
    #Adds new songs to the songs to be dowloaded. 
    def addon(self, newSongs):
        self.musictitles += newSongs
        self.mainShow()
    
    #Changes the link of the selected video 
    def changeLink(self, ind, musictitles):      
        Videos.config(height=1000, width=1000)
        vidTitle = musictitles[ind].watch_url
        linkLabel = Label(Videos, text="Video link " + str(ind+1))
        linkChange = tk.Entry(Videos, textvariable=vidTitle, width=35)
        linkChange.delete(0,END)
        linkChange.insert(0, vidTitle)  
        linkChangeButton = Button(Videos, text="Link Change", command = lambda: update(linkChange.get(), ind, musictitles))
        
        linkLabel.grid(column=4, row=1, padx=25)
        linkChange.grid(column=5, row=1)
        
        linkChangeButton.grid(column=6, row=1, padx=25)
        

  
        def update(link, ind, musictitles):
            Videos.destroy()
            musictitles[ind] = YouTube(link, use_oauth=True, allow_oauth_cache=True)
            linkLabel.grid_forget()
            linkChange.grid_forget()
            linkChangeButton.grid_forget()
            showVideos(musictitles).mainShow()
            #main.geometry(height=280, width=240)
    

    #Makes the changes final and prepares for download
    def outPut(self):
        songTitleFinal = []
        songExten = []
        
        #Puts all the videos that are checked into a list.
        for box in range (len(musicBoxes)):
            if musicBoxes[box].var.get() == 1:
                songTitleFinal.append(self.musictitles[box])
                
        #Gets all the videos that are checked and puts their exstenions type into a list.
        for bo in range (len(checkboxes)):
            if musicBoxes[bo].var.get() == 1:
                songExten.append(checkboxes[bo].var.get())
            
        
        #Removes video box  
        Videos.destroy()
        showVideos.alreadyExist = False
        main.geometry(f'{Main_width}x{Main_height}')
        noteBook.config(width = Main_width, height = Main_height)
        root.config(width = Main_width, height = Main_height)
        
        #Changes animation to download one, Starts animation, Starts last preperations before download begins
        downloadAnim(songTitleFinal, songExten)
    
    
#Starts the actual downloading, Starts queue and inputs all the files that need to be downloaded to the actual downloader function. 
def threaders(songsTBD, songsExt):
    global errsSongs 
    q = queue.Queue()
    errsSongs = []
    threading.Thread(target=Downloader, args=(q,), daemon=True).start()
    for t in range(0, len(songsTBD)):
        q.put([songsTBD[t], songsExt[t-1]])
    #Used to stop the downloader once all the songs have been downloaded
    q.put([None])

def fileFix(file):
    if "/" in file:
        file = file.replace(r"/", "-")
    if '"' in file:
        file = file.replace(r'"', '')
    if "|" in file:
        file = file.replace(r"|", "-")
    if "+" in file:
        file = file.replace(r"+", "-")
    if  "?" in file:
        file = file.replace(r"?", "-")
    if  "[" in file and "]" in file:
        file = file.replace(r"[", "(")
        file = file.replace(r"]", ")")
    if  "*" in file:
        file = file.replace(r"*", "-")
    if  ":" in file:
        file = file.replace(r":", "-")
    if "#" in file:
        file = file.replace(r"#", "")
    return file
        

#downloads the thumbnail for the videos
def downloadThumbnail(url: str, dest_folder: str, fileName: str):
    
    #Ensures that the file doesn't cause an error due to characters in its name. Combines destination folder with the file name and adds the extension
    fileName = fileFix(fileName)
    fullpath = dest_folder + fileName + ".jpg"
    
    #Wget used to download specified image url,  returns both the file path and downloaded file. 
    finaltmbn = urllib.request.urlretrieve(url, fullpath)
    return finaltmbn

#Used to changed the thumbnail of the song
def thumbnailChanger(video, path):
    audiofile = eyed3.load(video)
    if (audiofile.tag == None):
        audiofile.initTage()

    audiofile.tag.images.set(3, open(path, 'rb').read(), 'image/jpeg')
    audiofile.tag.save(version=eyed3.id3.ID3_V2_3)


    

def fileConverter(vid, fullFile, DV, base):
    my_clip = mp.VideoFileClip(base[0] + ".mp4") 
    my_clip.audio.write_audiofile(fullFile)
    my_clip.close()
    #Creates a thumbnail and adds the authors name
    os.remove(DV)
    vidName = getTitle(extract.video_id(vid.watch_url))
    thumbnail = vid.thumbnail_url 
    img_path, finalImg = downloadThumbnail(thumbnail, "thumbnails/", vidName)
    thumbnailChanger(fullFile, img_path)
    
#The code for the actual video downloader. While true it will keep downloading songs, one at time so very slow. 
def Downloader(q):
    #Gets the percentage of the file that has been downloaded.
    
    while True:
        progressbar['value'] = 0
        loadingPercent.config(text="0%")
        values = q.get()

        #Stops the downloader once all the files have been downloaded or inputs the files and extensions to be downloaded. 
        if values[0] == None:
            break

        else:
            vid = values[0]
            exten = values[1]
            currentlyDownloading['text'] = getTitle(extract.video_id(vid.watch_url))

        downloadBtn["state"] = "disabled"
        
        #Downloads the video(s) and puts them in a temporary file so that they can be changed correctly
        
        currentVidDL = download.downloadVideo(vid, exten, True ,progressbar, LinkLabel, loadingPercent)
        currentVidDL.Downloader()
        currentVidDL.fileMove(outputLocation)
        

        #Moves onto the next song or stops entirely.
        q.task_done()
    
    #Moves onto the finishing animation and stops the downloading. 
    finish()
    q.join()


#Animation Functions




def downloadAnim(STF, STE):
    global showVids
    #move(0)
    #root.after_cancel(DevAnim)
    #root.after_cancel(anim)
    #file = downloading_files[0]
    #imageFileConfig(file, action = None)
    noteBook.config(height=Main_height, width=Main_width-190)    
    LinkLabel.configure(text="Loading")
    currentlyDownloading.grid(row=0, column=2, sticky= S)
    loadingPercent.grid(row=1, column=2, sticky=N, pady=10)
    progressbar.grid(row=1, column=2, sticky=N, pady=35)
    threaders(STF, STE)

def finish(): 
    if len(errsSongs) > 0:
        String = ""
        for i in range(len(errsSongs)):
            String += f"{getTitle(extract.video_id(errsSongs[i]))} \n"
        download2 = askyesno("Downloading Error", message=String)

        if download2:
            for i in range(len(errsSongs)):
                mak = YouTube(errsSongs[i], use_oauth=True, allow_oauth_cache=True)
                mak.streams.filter(progressive=True).get_highest_resolution().download(output_path=outputLocation, skip_existing=True)
    #root.after_cancel(anim)
    #file = downloading_files[1]
    #imageFileConfig(file, action = None)
    noteBook.config(height=Main_height, width=Main_width)
    showinfo(title=finish, message="Videos have been sucessfully downloaded")
    downloadBtn["state"] = "enabled"
    currentlyDownloading.grid_forget()
    progressbar.grid_forget()
    loadingPercent.grid_forget()
    LinkLabel.configure(text="Youtube Link")
    time.sleep(5)
    


#---------------------------------Root 2 functions------------------------------------------------------ 
def getSongsTBD():
    global outputLocation, songUrl, showVids
    playlistTBD = playlistInfo
    outputLocation = playlistOutputEntry.get()

    if playlistLinkEntry.get() == "" or playlistOutputEntry.get() == "":
        showwarning(title = "Empty", message="Do not keep the textboxes empty!" )
        return 
    if "https://open.spotify.com/playlist" not in playlistLinkEntry.get():
        showwarning(title = "Wrong Link", message="Only put spotify playlists on this page!" )
        return 
    
    if outputLocation in locationNames:
        outputLocation = locationPath[outputEntry.current()]
        
    else:
        outputLocation = playlistOutputEntry.get()
        jsonUpdate('songs', 'outputs', playlistOutputEntry, locationPath, widgetGet=outputLocation)
        

    
    if playlistTBD != playlistInfo:
        warning  = askquestion(root2, message="Are you sure you want to make " + getPlaylistName(playlistTBD) + " your playlist to be upkept" )
        if warning == "yes":
            jsonUpdate('playlistStuff', 'playlist', widgetGet=playlistTBD)
        
    songUrl = spotiPlaylist(playlistTBD)
    if showVideos.alreadyExist == False:
        showVids = showVideos(songUrl) 
          
    if showVideos.alreadyExist == True:
        
        addtoList = askyesnocancel("Crossroads", f"Would you like to add {getPlaylistName(playlistTBD) } to your songsTBD? \n cancel to replace the current selection with the new one")
        if addtoList == True:
            showVids.addon(songUrl)
            return 
        elif addtoList == False:
            return     
        else:
            showVids = showVideos(songUrl)   
    showVids.mainShow()

#Window set up for the downloader, changes size, gives the window a name, changes color. 
main = tk.Tk()
Main_height = 350
Main_width=520
MainSize = main.geometry(f"{Main_width}x{Main_height}") 
main.title("YouTube Video Downloader")
main.config(background="grey")
s = ttk.Style()
s.theme_use('default')

noteBook = ttk.Notebook(main, height=Main_height, width=Main_width)
noteBook.grid(column=0, columnspan=2, row=0, rowspan=2)

root = Frame(noteBook, background="grey", height=Main_height, width=Main_width)
noteBook.add(root, text="Main Downloader")

root2 = Frame(noteBook, background="grey", height=Main_height, width=Main_width)
noteBook.add(root2, text="Spotify Upkeep")

songsNames, songLinks, locationNames, locationPath, playlistInfo, playlistName, data = loadData(0)

#Top name of the downloader. 
heading=Label(root, text = "Song Downloader", justify=CENTER, padx=14, pady=15, font="15", width = 19)
heading.grid(row = 0, column = 2, pady=5)

#Entry for video/playlist link 
LinkLabel=Label(root, text='Youtube Link')
LinkLabel.grid(row=2, column=1, padx=10, pady=10)

#Menu stuffs
menuBar = Menu(main)
main.config(menu=menuBar)

MainMenu = Menu(menuBar)
menuBar.add_cascade(label="File", menu=MainMenu)
MainMenu.add_command(label='Saved Links', command=showLinks)

#Variables for youtube and output path
ytLink = tk.StringVar()
outputPath = tk.StringVar()

#Entry for the video/playlist link  
linkEntry = ttk.Combobox(root, textvariable=ytLink, show='', values=songsNames)
linkEntry.grid(row=2,column=2)
linkEntry.focus()

#The file extension options 
options = [".mp3", ".mp4"]
clicked = StringVar()

#Sets the default value to .mp3 and creates the actual drop down menu
clicked.set( ".mp3" )
drop = OptionMenu(root, clicked, *options)
drop.grid(row=2, column=3)

#Output location Entry, it's default value is set to whatever was input last time similar to the video link entry. 
output=Label(root, text="Output Location")
output.grid(row=3, column=1, padx=10, pady=10)
outputEntry = ttk.Combobox(root, textvariable=outputPath, values=locationNames)
outputEntry.grid(row=3, column=2)

#Browse Button
browser = ttk.Button(root, text="Browse", command=lambda: browse(root))
browser.grid(row=3, column=3)

#Download Button
downloadBtn = ttk.Button(root, text="Download", command=PLChecker)
downloadBtn.grid(row=4, column=2)

#Download bar and loading percent 
currentlyDownloading = tk.Label(main, text="...", font=("Agency FB", 13))
progressbar = ttk.Progressbar(main, orient="horizontal", length=160, mode='determinate', maximum=100)
loadingPercent = tk.Label(main, text="0%", font=("Agency FB", 10))

#All under this are for Develon
#Develon window Set up

canvas_width = 200
canvas_height = 100
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="lightblue")
canvas.grid(row=1, column=2)
#myImage = tk.PhotoImage(file="images/DevelonDownloaderNew.png")
#canvas.create_image(startPosX-64,startPosY, image=myImage)
showVideos.alreadyExist = False
#imageFileConfig.alreadyRun = False

#Root 2 ----------------------------------------
heading2=Label(root2, text = "Spotify Upkeeper", padx=14, pady=15, font="15", width = 19)
heading2.grid(row = 0, column = 2, pady=5 )
    
playlistEntryLink = tk.StringVar()

playlistCanvas = tk.Canvas(root2, width=canvas_width, height=canvas_height, bg="lightblue")
playlistCanvas.grid(row=1, column=2)

playlistLinkLabel=Label(root2, text='Playlist Link')
playlistLinkLabel.grid(row=2, column=1, padx=10, pady=10)

playlistOutputLabel=Label(root2, text='Output Location')
playlistOutputLabel.grid(row=3, column=1, padx=10, pady=10)

playlistLinkEntry = Entry(root2, textvariable=playlistEntryLink)
playlistLinkEntry.grid(row=2,column=2)
playlistLinkEntry.insert(0, playlistInfo)

playlistOutputEntry = Combobox(root2, textvariable=outputPath, values=locationNames)
playlistOutputEntry.grid(row=3, column=2)

browser2 = ttk.Button(root2, text="Browse", command=lambda: browse(root2))
browser2.grid(row=3, column=3)
downloadBtn = ttk.Button(root2, text="Download", command=lambda: getSongsTBD())
downloadBtn.grid(row=4, column=2)



#eventStarter(action = None)


#Starts gui window
main.mainloop()