from pytube import extract
import os
import Modules.YouTubeApi
import moviepy.editor as mp
import urllib.request
import urllib
import eyed3
import shutil


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
        
    def infoChange(self, video, exten):
        self.video = video
        self.exten = exten
    
    def progress_callback(self, stream, chunk, bytes_remaining):
        size = stream.filesize
        progress = int(((size - bytes_remaining) / size) * 100)
        if self.progressBar['value'] == 100: 
            self.Link.config(text = "Downloading")
        self.loadingPercent.config(text =str(progress) + "%")
        self.progressBar['value'] = progress
        
    
    def Downloader(self):     
        #try:
        #Downloads the video(s) and puts them in a temporary file so that they can be changed correctly
        if self.useGUI == True:
            self.video.register_on_progress_callback(self.progress_callback)
        DV = self.video.streams.filter(progressive=True).get_highest_resolution().download(output_path="tempSongsFolder/", skip_existing=True)           
        self.fullFile = os.path.splitext(DV)[0] + self.exten
        if self.exten == ".mp3":
            return downloadVideo.fileConverter(self, DV, os.path.splitext(DV))
        return os.path.splitext(DV)[0] + self.exten     
        #except:
            #self.errSongs.append(self.video.watch_url)
    
    def fileFix(self, file):
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
        
        #Ensures that the file doesn't cause an error due to characters in its name. Combines destination folder with the file name and adds the extension
        fileName = downloadVideo.fileFix(self, fileName)
        fullpath = dest_folder + fileName + ".jpg"
        
        #Wget used to download specified image url,  returns both the file path and downloaded file. 
        finaltmbn = urllib.request.urlretrieve(url, fullpath)
        return finaltmbn

    #Used to changed the thumbnail of the song
    def thumbnailChanger(self, video, path):
        audiofile = eyed3.load(video)
        if (audiofile.tag == None):
            audiofile.initTage()

        audiofile.tag.images.set(3, open(path, 'rb').read(), 'image/jpeg')
        audiofile.tag.save(version=eyed3.id3.ID3_V2_3)            

    def fileConverter(self, DV, base ):
        my_clip = mp.VideoFileClip(base[0] + ".mp4") 
        my_clip.audio.write_audiofile(self.fullFile)
        my_clip.close()
        #Creates a thumbnail and adds the authors name
        os.remove(DV)
        vidName = Modules.YouTubeApi.getTitle(extract.video_id(self.video.watch_url))
        thumbnail = self.video.thumbnail_url 
        img_path, finalImg = downloadVideo.downloadThumbnail(self, thumbnail, "thumbnails/", vidName)
        downloadVideo.thumbnailChanger(self, self.fullFile, img_path)
        
    def fileMove(self, folder):
        vidTitle = downloadVideo.fileFix(self, Modules.YouTubeApi.getTitle(extract.video_id(self.video.watch_url)))
        filePath = shutil.move(self.fullFile, os.path.join(folder, vidTitle + self.exten))
        return filePath 

    def getFileName(self):
        return self.fullFile 
    
