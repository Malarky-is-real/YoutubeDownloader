"""
Different Testing Sites
"""

#Game Testing
"""
import RandomEventsClass
BossTest = RandomEventsClass.RandomEvents()
BossTest.bossEvent()
"""

#Data Management Module Testing
"""
import DataManagement
dataMaker = DataManagement.dataFile("testingStuff/mak.csv")
dataMaker.checkExist("Mak Twin", "#3","Maks Awesome Sauce Works" )
dataMaker.appendToCSV()
"""

#Download Module Testing
"""
import download as download
from pytube import *
Dl = download.downloadVideo(YouTube("https://www.youtube.com/watch?v=vkailb3xcTI"), ".mp3", None, None, None, None)
Dl.Downloader()
Dl.fileMove("C:/Users/tatsm/Music/test")
"""

#YT API Module Testing
"""
import YouTubeApi as yt
You = yt.YT_API()
print(You.getTitle("ZevbD7x6TD4"))
"""

#Spotify Module Testing
"""
import Spot
mak = Spot.spotiPlaylist("5ln8XN0mv5aufkiH4OZ3hq")
"""

#Data and Auto DL Testing