
"""
C:\Users\Anthony\AppData\Local\Programs\Python\Python310\Scripts
#Testing
t = open("downloadedSongs.txt", "r", encoding="utf-8")
if "(Unreleased) Perfect Cell Vs SSJ Goku" in t.read():
    print("It does exist")
else: 
    print("It doesnt")
t.close()
"""
#Functions
#Defining CreateWidgets() function
# to create necessary tkinter widgets
#def widgets():
    
    



#Defining Browse() to select a destination folder to save the video
"""
def Browse():
    #Presenting user with a pop-up for directory slection. initialdir
    #argument is option Retriving the user-input destination directory
    #and storing it in downloadDirectory
    download_Directory = filedialog.askdirectory(
        initialdir="YOUR DIRECTORY PATH", title="Save Video")
        #Displaying the driectory int he directory textbox
    download_Path.set(download_Directory)
"""



#Makes a list of all the songs in the music folder.
"""
def checker():
    #Variables
    global r
    global file_path
    file_path="C:/Users/Anthony/Music"
    onlyFile = [f for f in listdir(file_path) if isfile]
    
    #o opens downloadedSongs.txt and r reads the contents of the file.
    o = open("downloadedSongs.txt", "w+", encoding="utf-8")
    r = o.read()
    
    
    print("Checking for songs already downloaded")
    
    #split_tup gets the name of the files and exsten isolates the file type
    for file in onlyFile:
        split_tup = os.path.splitext(file)
        exsten = split_tup[1]
        
        #If the file is already has the exstention .mp3 then it adds the file to the text doc 
        if exsten == ".mp3":
            #Stripped gets rid of spaces in the names and adds .write adds the name
            stripped_file =  file.replace(" ", "") 
            o.write(stripped_file + "\n")
    
    o.close()
    
    print("Files have been added to downloadedSongs.txt\n")
"""

"""
    for url in urls:
    
        #names gets the video name, stripped remove unwanted characters, then it is printed
        names = (YouTube(url).title + ".mp3")
        stripped_str = names.replace('"', " ")
        stripped_str = stripped_str.replace(':', " ")
        stripped_str = stripped_str.replace(" ", "")
        titles.append(stripped_str)
        print(stripped_str + "\n")
 
    #leftovers
    #checks if the video is in the downloadedSongs file and if so it skips the song.

    if titles[i] in r:
        print(titles[i] + " already downloaded, please remove from list to save time. \n")
        i += 1
        continue
    

    #If isn't in the list then it skips the song.
    elif titles[i] not in r: 
        print( titles[i] + " not downloaded \n")
"""

"""
Was supposed to show the selected exstension file from the drop down menu
def show():
    label.config(text = clicked.get())
"""

"""
Cancels animation
def pause_anim():
    button1['state'] = NORMAL
    button2['state'] = tk.DISABLED
    root.after_cancel(anim)

"""

"""
Warning before starting download
def checker():
    msg = f"Your link is {ytLink.get()} and it will be outputted to {outputPath.get()}"
    showinfo(title="Disclaimer", message=msg)
"""