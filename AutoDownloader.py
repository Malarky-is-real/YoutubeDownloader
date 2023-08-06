import Modules.download
import Modules.YouTubeApi
import Modules.Spot
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import pytube
from pytube import extract

gauth = GoogleAuth()
gauth.LoadCredentialsFile("C:/Users/tatsm/OneDrive/Desktop/Website/Python/YoutubeDownloader/mycreds.txt")
drive = GoogleDrive(gauth)

folder = drive.ListFile({'q': "title = 'music' and trashed=false"}).GetList()[0]

fileLocation = "C:/Users/tatsm/OneDrive/Desktop/Website/Python/YoutubeDownloader/tempSongsFolder"
songs = Modules.Spot.spotiPlaylist("5ln8XN0mv5aufkiH4OZ3hq")
for song in songs:
    currentVidDL = Modules.download.downloadVideo(song, ".mp3", False, None, None, None)
    currentVidDL.Downloader()
    fileName = currentVidDL.getFileName()
    file = drive.CreateFile({'title': Modules.YouTubeApi.getTitle(extract.video_id(song.watch_url)) + ".mp3", 'parents': [{'id': folder['id']}]})
    file.SetContentFile(fileName)
    file.Upload()
    #currentVidDL.fileMove("C:/Users/tatsm/Music/SongsFromSpoti")

"""
for path  in os.listdir(fileLocation):
    if os.path.isfile(os.path.join(fileLocation, path)):
"""



