import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
from pytube import YouTube, Playlist
from pytube import * 


cid = 'e2ba3be9797249cdae236e95cafa46aa'
secret = '07949281789c4445851d5eb1b3b495cd'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

scope = "user-library-read"

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

#Downloads all songs in a playlist no matter if they are in savedSongs list
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
                s = Search(f'{artist_uri} - {currSong} +audio')
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

                s = Search(f'{currSong} - {albumName} - {artist_uri} +audio')
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
    data = "" 
    toDownload = []
    lastDownloaded = []
    songlist = open('TextFiles\SavedSongs.txt', 'r+', encoding="utf-8")
    read = songlist.readlines()
    
    for line in read:
        
        if "*" in line[0]:
            lastDownloaded.append(line)
            line = line.replace("*", "", 1)
        
        data += line
    
    for num in range(len(results)):
        currSong = results[num]['track']['name']
        artist_uri = results[num]['track']['artists'][0]['name']

        if f"{currSong} - {artist_uri}" not in data:
            filesong = f"*{currSong} - {artist_uri}"

            song = f"{artist_uri} - {currSong}"
            toDownload.append(song)
            data += filesong + "\n"
    
    songlist.close()
    
    
    songListChange = open('TextFiles\SavedSongs.txt', 'w', encoding="utf-8")
    songListChange.write(data)
    songListChange.close()


    SongLinks = []
    for i in toDownload:

        try:
            
            s = Search(f"{i} +audio")
            SongLinks.append(s.results[0])

        except:
            print(i + " not found, please find manually sorry")
    return SongLinks



        
    