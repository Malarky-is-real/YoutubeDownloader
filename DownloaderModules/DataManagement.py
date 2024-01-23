import pandas as pd

class dataFile(object):
    def __init__(self, csvFile):
        self.CSVFILE = csvFile
        self.df = pd.read_csv(csvFile, sep=",")
        self.nf = self.nf = pd.DataFrame({"Title": ["Switftie"], "Artist": ["Mak"], "Album": ["Bingnut"] })
    
    def dataFixer(self, data):
        data.replace(r",", "-")
    
    def checkExist(self, artistName, songName, albumName):        
        
        inDataBool = self.df.isin([songName, artistName, albumName]).any().all()
        print(f'Is [{songName}, {artistName}, {albumName}] in csv?: {inDataBool} \n')
        inNewDataBool = self.nf.isin([songName, artistName, albumName]).any().all()
        print(f'Is [{songName}, {artistName}, {albumName}] in newCSV?: {inNewDataBool} \n')
        
        if not inDataBool or inNewDataBool:
            self.dataFixer(songName)
            self.dataFixer(artistName)
            self.dataFixer(albumName)
            self.nf = self.nf.append({"Title": songName, "Artist": artistName, "Album":albumName}, ignore_index=True)
        print(self.nf + "\n")
        return inDataBool 

    def appendToCSV(self):
        print(f"{self.nf} !!!Appending to File!!! \n")
        self.nf = self.nf.drop([0,0])
        self.nf.set_index("Title", inplace = True)
        self.nf.to_csv(self.CSVFILE, mode='a', header=False)
        
