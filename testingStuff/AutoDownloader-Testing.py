import DownloaderModules.Spot as Spot
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import queue, threading
import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
import DownloaderModules.download as download
import DownloaderModules.YouTubeApi as YouTubeApi
from pytube import extract
gauth = GoogleAuth()
gauth.LoadCredentialsFile("C:/Users/tatsm/OneDrive/Desktop/Website/Python/YoutubeDownloader/mycreds.txt")
drive = GoogleDrive(gauth)

folder = drive.ListFile({'q': "title = 'music' and trashed=false"}).GetList()[0]
main = tk.Tk()
main.title("Downloding")
main.geometry("200x100")

#Widgets
textBox = tk.Label(main, text="Current Downloading").pack()
currentlydownloading = tk.Label(main, text="")
downloadingprogress = ttk.Progressbar(main, orient="horizontal", length=160, mode='determinate', maximum=100)
LoadPercent = tk.Label(main, text="")

YouYubeApi = YouTubeApi.YT_API()

#Adding to the GUI
currentlydownloading.pack()
downloadingprogress.pack()
LoadPercent.pack()


songs = Spot.spotiPlaylistDownload("https://open.spotify.com/playlist/1klUYmADVLqF7JfReWHvp2?si=aa0593dad036466f")

def threaders(songs):
    #q = queue.Queue()
    #threading.Thread(target=dl, args=(q,), daemon=True).start()
    for t in range(0, len(songs)):
        YouYubeApi.getTitle(extract.video_id(songs[t].watch_url))
        #q.put(songs[t])
        
    #Used to stop the downloader once all the songs have been downloaded
    #q.put(None)

def end():
    os._exit(0)
    
    

def dl(q):
    while True:
        song = q.get()
        downloadingprogress['value'] = 0
        LoadPercent.config(text="0%")
        #Stops the downloader once all the files have been downloaded or inputs the files and extensions to be downloaded. 
        if song == None:
            q.task_done()
            break

        title = YouYubeApi.getTitle(extract.video_id(song.watch_url))
        if len(title) > 10: 
            currentlydownloading['text'] = f'{title[0:25]}...'
        else: 
            currentlydownloading['text'] = title
    
        currentlydownloading.config(text=title)
        currentVidDL = download.downloadVideo(song, ".mp3", True, downloadingprogress, currentlydownloading, LoadPercent)
        currentVidDL.Downloader()
        fileLocation = currentVidDL.fileMove("C:/Users/tatsm/Music/SongsFromSpoti")
        file = drive.CreateFile({'title': title + ".mp3", 'parents': [{'id': folder['id']}]})
        file.SetContentFile(fileLocation)
        file.Upload() 
        q.task_done()
    
    q.join()
    end()
    
button = Button(main, command=threaders(songs))
main.mainloop()




