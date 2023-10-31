import csv 
import pandas as pd

class dataFile(object):
    def __init__(self, csvFile):
        self.CSVFILE = csvFile
        self.df = pd.read_csv(csvFile, sep=",")
        

    def getArtistSongs(self, artistName, songName, albumName):
        #songsByArtist = self.df.groupby("Artist").size().sort_values(ascending=True)
        #self.df.set_index("Artist", inplace = True)
        
        bru = self.df.loc[(self.df['Artist'] == artistName) & (self.df['Album'] == albumName) & (self.df['Title'] == songName)].to_l
        print(bru)
        
                
        
            

        
            
        """"
        for row in self.df:
            if(self.df.loc[i, "Artist"] == artistName and self.df.loc[i, "Title"] == songName and self.df.loc[i, "Album"] == albumName):
                print("Match")
            else: 
                self.df = self.df.append({"Title": songName, "Artist": artistName, "Album":albumName }, ignore_index=True)
            print(self.df)
        """
            
