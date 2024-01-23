from pytube import extract
import os
import moviepy.editor as mp
import urllib.request
import urllib
import eyed3
import shutil
from proglog import ProgressBarLogger
from YouTubeApi import YT_API




class downloadVideo(object):

    
    def __init__(self, video, exten, useGUI, progressBar, titlelabel, loadpercentshower):
        self.errSongs = []
        self.useGUI = useGUI
        self.video = video
        self.exten = exten
        self.fullFile = ""
        self.progressBar = progressBar
        self.Link = titlelabel      
        self.loadingPercent = loadpercentshower
        self.logger = self.MyBarLogger(progressBar=self.progressBar, loadingValue=self.loadingPercent)
        self.TubeAPi = YT_API()
    
    class MyBarLogger(ProgressBarLogger):
        def __init__(self, init_state=None, bars=None, ignored_bars=None, logged_bars='all', min_time_interval=0, ignore_bars_under=0, progressBar = None, loadingValue = None):
            super().__init__(init_state, bars, ignored_bars, logged_bars, min_time_interval, ignore_bars_under)
            self.progressBar = progressBar
            self.loadingValue = loadingValue

        def bars_callback(self, bar, attr, value,  old_value = None ):
            # Every time the logger progress is updated, this function is called        
            percentage = (value / self.bars[bar]['total']) * 100
            self.progressBar["value"] = percentage
            self.loadingValue.config(text =str(round(percentage, 2)) + "%")
            
    def infoChange(self, video, exten):
        self.video = video
        self.exten = exten
    
    def progress_callback(self, stream, chunk, bytes_remaining):
        size = stream.filesize
        progress = int(((size - bytes_remaining) / size) * 100)
        if self.progressBar['value'] == 100: 
            self.Link.config(text = "Converting")
        self.loadingPercent.config(text =str(progress) + "%")
        self.progressBar['value'] = progress
        
    
    def Downloader(self):     
        #Downloads the video(s) and puts them in a temporary file so that they can be changed correctly
        if self.useGUI == True:
            self.video.register_on_progress_callback(self.progress_callback)
        DV = self.video.streams.filter(progressive=True).get_highest_resolution().download(output_path="tempSongsFolder/", skip_existing=True)           
        self.fullFile = os.path.splitext(DV)[0] + self.exten
        if self.exten == ".mp3":
            return downloadVideo.fileConverter(self, DV, os.path.splitext(DV))
        return os.path.splitext(DV)[0] + self.exten   


    
    def fileFix(self, file):    
        #Ensures that the file doesn't cause an error due to characters in its name.
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
        if "'" in file:
            file = file.replace(r"'", "")
        return file
            

    #downloads the thumbnail for the videos
    def downloadThumbnail(self, url: str, dest_folder: str, fileName: str):
        #Wget used to download specified image url,  returns both the file path and downloaded file. 
        return urllib.request.urlretrieve(url, dest_folder + downloadVideo.fileFix(self, fileName) + ".jpg")

    #Used to changed the thumbnail of the song
    def thumbnailChanger(self, video, path):
        audiofile = eyed3.load(video)
        if (audiofile.tag == None):
            audiofile.initTage()
        audiofile.tag.images.set(3, open(path, 'rb').read(), 'image/jpeg')
        audiofile.tag.save(version=eyed3.id3.ID3_V2_3)            

    def fileConverter(self, DV, base):
        my_clip = mp.VideoFileClip(base[0] + ".mp4") 
        my_clip.audio.write_audiofile(self.fullFile, logger=self.logger)
        my_clip.close()
        os.remove(DV)
        #Creates a thumbnail and adds the authors name
        vidName = self.TubeAPi.getTitle(extract.video_id(self.video.watch_url))
        thumbnail = self.video.thumbnail_url 
        img_path, finalImg = downloadVideo.downloadThumbnail(self, thumbnail, "thumbnails/", vidName)
        downloadVideo.thumbnailChanger(self, self.fullFile, img_path)
        
    def fileMove(self, folder):
        filefixed = downloadVideo.fileFix(self, self.TubeAPi.getTitle(extract.video_id(self.video.watch_url))) + self.exten
        print(filefixed)
        fileLocation = shutil.move(self.fullFile, os.path.join(folder, filefixed)) 
        return fileLocation

    def getFileName(self):
        return self.fullFile 
    

