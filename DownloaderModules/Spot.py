import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from pytube import YouTube, Playlist
from pytube import * 
import DownloaderModules.DataManagement as DataManagement

cid = 'e2ba3be9797249cdae236e95cafa46aa'
secret = '07949281789c4445851d5eb1b3b495cd'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)


scope = "user-library-read"
auth_manager = spotipy.oauth2.SpotifyClientCredentials(
    client_id=cid,
    client_secret=secret
    
)
token = auth_manager.get_access_token()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#Gets the playlist name
def getPlaylistName(plID):
    playList = sp.playlist(playlist_id=plID, fields="name")
    return playList["name"]

#Gets the album name
def getAlbumName(plID):
    playList = sp.album(plID)
    return playList["name"]

#Gets the name of all the songs in a playlist
def getAllSongs(plID):
    if "playlist" in plID:
        
        results = sp.playlist_items(plID)
        tracks = results['items']

        while results['next']:
                results = sp.next(results)
                tracks.extend(results['items'])

        results = tracks
        for num in range(len(results)):
            print(results[num]['track']['name'] )
    
    elif "album" in plID: 
        results = sp.album_tracks(plID)
        tracks = results['items']
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])

        results = tracks
        for num in range(len(results)):
            print(results[num]['name'])

#Downloads all songs in a playlist/album no matter if they are in savedSongs list
def spotiPlaylistDownload(plId):
    if "playlist" in plId:
        results = sp.playlist_tracks(plId)
        tracks = results['items']

        while results['next']:
                results = sp.next(results)
                tracks.extend(results['items'])

        results = tracks 
        
        SongLinks = []
        for i in range(len(results)):
            currSong = results[i]['track']['name']
            artist_uri = results[i]['track']['artists'][0]['name']
            
            try:
                s = Search(f'{artist_uri} - {currSong} +audio ')
                SongLinks.append(s.results[0])
                
                
            except:
                print(currSong + " not found, please find manually sorry")
                
    elif "album" in plId:
        results = sp.album_tracks(plId)
        tracks = results['items']
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])

        results = tracks
        SongLinks = []
        albumName = sp.album(plId)['name']
        authorName = sp.album(plId)['name']
        for num in range(len(results)):
            currSong = results[num]['name']
            artist_uri = results[num]['artists'][0]['name']
            try:

                s = Search(f'{currSong} - {albumName} - {artist_uri} +audio ')
                SongLinks.append(s.results[0])
                
            except:
                print(currSong + " not found, please find manually sorry")
    return SongLinks

#Downloads songs not in savedSongs list
def spotiPlaylist(plID):

    results = sp.playlist_tracks(plID)
    tracks = results['items']

    while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])

    results = tracks 
    toDownload = []
    songlist = DataManagement.dataFile("TextFiles/savedSongs.csv")
    for num in range(len(results)):
        currSong = results[num]['track']['name']
        artist_uri = results[num]['track']['artists'][0]['name']
        
        if not songlist.checkExist(currSong, artist_uri, results[num]['track']['album']["name"]):
            toDownload.append(f"{currSong} - {artist_uri}")
    songlist.appendToCSV()            

    SongLinks = []

    for i in toDownload:

        try:
            
            s = Search(f"{i} +audio ")
            
            SongLinks.append(YouTube(s.results[0].watch_url, use_oauth=True, allow_oauth_cache=True ))

        except:
    
            print(i + " not found, please find manually sorry")
    return SongLinks

"""
def getEverything(plID):
    if "playlist" in plID:
        
        results = sp.playlist_items(plID)
        tracks = results['items']

        while results['next']:
                results = sp.next(results)
                tracks.extend(results['items'])
        
        with open ('testingStuff/mak.csv', 'w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            field = ["title", "author", "album"]
            writer.writerow(field)

            results = tracks
            for num in range(len(results)):
                writer.writerow([results[num]['track']['name'], results[num]['track']['artists'][0]['name'], results[num]['track']['album']["name"] ])
"""

