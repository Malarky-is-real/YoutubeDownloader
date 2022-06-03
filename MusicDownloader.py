#This program will get songs from a youtube playlist and then download them to a music folder.

#imports
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox

from pytube import YouTube, Playlist

import os
from os import listdir
from os.path import isfile, join

#Variables
p = Playlist("https://www.youtube.com/playlist?list=PLPECdi5vt-fzoanbT7-QyTh6x_pHDUYOh")
file_path="C:/Users/Anthony/Music"

"""
#Testing
t = open("downloadedSongs.txt", "r", encoding="utf-8")
if "(Unreleased) Perfect Cell Vs SSJ Goku" in t.read():
    print("It does exist")
else: 
    print("It doesnt")
t.close()
"""


onlyFile = [f for f in listdir(file_path) if isfile]

#Makes a list of all the songs in the music folder.
def checker():
    #Variables
    global r
    #o opens downloadedSongs.txt and r reads the contents of the file.
    o = open("downloadedSongs.txt", "w+", encoding="utf-8")
    r = o.read()
    
    
    print("Checking for songs already downloaded")
    
    #split_tup gets the name of the files and exsten isolates the file type
    for file in onlyFile:
        split_tup = os.path.splitext(file)
        exsten = split_tup[1]
        
        #If the file is already has the exstention .mp3 then it adds the file to the text doc 
        if exsten == ".mp3":
            #Stripped gets rid of spaces in the names and adds .write adds the name
            stripped_file =  file.replace(" ", "") 
            o.write(stripped_file + "\n")
    
    o.close()
    
    print("Files have been added to downloadedSongs.txt\n")







#Gets the urls of all the videos in the list
urls = p.video_urls
print(f'Downloading: {p.title} \n')

def downloader():
    #for every url in the list url
    i = 0
    i2 = 0
    titles = []
    for url in urls:
    
        #names gets the video name, stripped remove unwanted characters, then it is printed
        names = (YouTube(url).title + ".mp3")
        stripped_str = names.replace('"', " ")
        stripped_str = stripped_str.replace(':', " ")
        stripped_str = stripped_str.replace(" ", "")
        titles.append(stripped_str)
        print(stripped_str + "\n")
    
    #for every vid in p.videos    
    for vid in p.videos:
            
            #checks if the video is in the downloadedSongs file and if so it skips the song.
            if titles[i] in r:
                print(titles[i] + " already downloaded, please remove from list to save time. \n")
                i += 1
                continue
            
            
            #If isn't in the list then it skips the song.
            elif titles[i] not in r: 
                print( titles[i] + " not downloaded \n")
                
                
                try:
                    DV = vid.streams.filter(only_audio=True).first().download(output_path="C:/Users/Anthony/Music")
                    print(DV)
                    base,ext = os.path.splitext(DV)
                    newfile = base + '.mp3'
                    os.rename(DV, newfile)
                
                except FileExistsError:
                    print("File already exists\n")
                    os.remove(DV)
                
                except not FileExistsError:
                    print("Somethin else is funky\n")
                
                else:
                    print(titles[i] + " was downloaded.\n")
                i += 1

    #"""

checker()
downloader()
