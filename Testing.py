import eyed3
from eyed3.id3.frames import ImageFrame
import requests
import shutil
import os
from pytube import * 

y = YouTube("https://www.youtube.com/watch?v=95CMUOA0bRI").thumbnail_url
thumbnailLink = y 
def download(url: str, dest_folder: str):
    global file_path
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))
        
download(y, dest_folder="C:/Users/Anthony/Desktop/Website/Python/YoutubeDownloader/thumbnails")


audiofile = eyed3.load('C:/Users/Anthony/Music/Sonic 3 - Big Arms - Traditional Japanese Version.mp3')
if (audiofile.tag == None):
    audiofile.initTage()

audiofile.tag.images.set(3, open(file_path, 'rb').read(), 'image/jpeg')
audiofile.tag.save(version=eyed3.id3.ID3_V2_3)

print("Bruh")