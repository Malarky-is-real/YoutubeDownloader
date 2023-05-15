from logging import root
from msilib.schema import CheckBox
from multiprocessing.spawn import import_main_path
from re import I
from statistics import variance
from tkinter import Tk
from typing import overload
from unicodedata import name
import eyed3
from eyed3.id3.frames import ImageFrame
import requests
import shutil
import os
from pytube import * 
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import DISABLED, Widget, ttk, Grid
import random as rand
import time 
from tkinter.scrolledtext import ScrolledText
import os
import youtube_dl
from subprocess import call
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
from bs4 import BeautifulSoup
import json
import googleapiclient.discovery
from pytube import extract
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import googleapiclient.errors
import queue, threading
import tkinter as tk
from tkinter.ttk import *
from tkinter import  *
from tkinter import DISABLED, Widget, ttk, filedialog
from tkinter.messagebox import *
from tkinter.scrolledtext import ScrolledText
import moviepy.editor as mp
from PIL import Image
import urllib.request
import urllib
import time
#Importing Pytube
from pytube import YouTube, Playlist
from pytube import * 
from pytube import extract
import pytube.request
import eyed3
import os
from os import link 
import shutil
import requests
import random
from mttkinter import mtTkinter as tk
from mttkinter import *
from Spot import *  
import json
from bs4 import BeautifulSoup as bs # importing BeautifulSoup


def loadData(ran):
    global songsNames, locationNames, playlistName
    songsNames = []
    locationNames = []
    playlistName = []
    with open('TextFiles/Links.json', 'r') as json_file:
        data = json.load(json_file)
    
    songLinks = data['songs'][0]['song']
    print(songLinks)
    locationPath = data['songs'][0]['outputs']
    playlistInfo = data['playlistStuff'][0]['playlist']
    for music in songLinks:
        try: 
            if "www.youtube.com/playlist?list" in music or "&list" in music:
                songsNames.append(Playlist(music).title + " - Youtube Playlist")
            
            elif "https://open.spotify.com/playlist" in music:
                songsNames.append(getPlaylistName(music) + " - Spotify Playlist")

            elif "open.spotify.com/album" in music:
                songsNames.append(getAlbumName(music) + " - Spotify Album")
            
            else:
                songsNames.append(YouTube(music, use_oauth=True, allow_oauth_cache=True).title + " - " + YouTube(music, use_oauth=True, allow_oauth_cache=True).author)
        except:
            if "www.youtube.com/playlist?list" in music or "&list" in music:
                songsNames.append("Youtube Playlist")
            
            elif "https://open.spotify.com/playlist" in music:
                songsNames.append("Spotify Playlist")

            elif "open.spotify.com/album" in music:
                songsNames.append("Spotify Album")
            
            else:
                songsNames.append("Youtube Video")
            songsNames.append("err")
            continue

    for locations in locationPath:
        locationNames.append(os.path.basename(locations))
    return songsNames, songLinks, locationNames, locationPath, playlistInfo, playlistName, data

"""    if ran == 1:
        linkEntry['values'] = songsNames
        outputEntry['values'] = locationNames
        playlistLinkEntry.insert(0, playlistInfo)
        playlistOutputEntry['values'] = locationNames"""
    


"""
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
"""

#songsNames, songLinks, locationNames, locationPath, playlistInfo, playlistName, data = loadData(0)
"""
for i in range(len(songsNames)):
    print(songsNames[i])
    print(songLinks[i])
    print("\n")
"""