
"""
C:\Users\tatsm\AppData\Local\Programs\Python\Python310\Scripts
C:\Users\tatsm\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts
#Testing
t = open("downloadedSongs.txt", "r", encoding="utf-8")
if "(Unreleased) Perfect Cell Vs SSJ Goku" in t.read():
    print("It does exist")
else: 
    print("It doesnt")
t.close()
"""


"""
Stupid way of finding the extension format of the song
for i in range(1, len(checkboxes), 2):
    print("i is ", i)
    ind = i - 1 
    print("ind is ", ind)
    if checkboxes[ind].var.get() == 1: 
        print("List len is ", len(songTitleFinal))
        songTitleFinal.insert(len(songTitleFinal)+0, checkboxes[i].var.get())
        print(checkboxes[i].var.get() + " is being inserted in ", len(songTitleFinal)+0)
"""     

"""
Test for queue threading 
def threadQueue(q, vids, ind):
    q.put(vids)
    for t in songTitleFinal: 
        task = q.get()
        q.task_done()
        print(f'thread is downloading {vids}')
"""

    
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

"""
Checked to see if thredas were alive
    if f.is_alive() == False:
        print(f"thread {threads[thread]} is dead")
    print(f" thread {threads[thread]} is alive?: {f.is_alive()}")
"""

#print(f" Is Q empty? {q.empty()}")
#print(f" thread {threads[thread]} is alive?: {f.is_alive()}")
#time.sleep(15)
#print(f" Is Q empty? {q.empty()}")

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

#Changes \ to / to make files work in the downloader. 
#PL_link = PL_link.replace(r"\"", "/")

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
checked to see if threads were still working
def threadAliveChecker(threadnum):
    global threads
    threads[threadnum-2].should_abort_immediately = True
    if len(threads) <= 1:
        threads.clear()
        finish()
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

"""
Old Downloading Code
    while True:
        progressbar['value'] = 0
        loadingPercent.config(text="0%")
        values = q.get()

        #Stops the downloader once all the files have been downloaded or inputs the files and extensions to be downloaded. 
        if values[0] == None:
            break

        else:
            vid = values[0]
            exten = values[1]
            currentlyDownloading['text'] = getTitle(extract.video_id(vid.watch_url))

        downloadBtn["state"] = "disabled"
        folder = outputLocation
        
        try:
            #Downloads the video(s) and puts them in a temporary file so that they can be changed correctly
            vid.register_on_progress_callback(progress_callback)
            
            #DV = vid.streams.filter(progressive=True).get_highest_resolution().download(output_path="tempSongsFolder/", skip_existing=True)           
            #base = os.path.splitext(DV)
               
        except:
            errsSongs.append(vid.watch_url)
            continue
        
        #Converts video to mp3 if mp3 is selected, adds a thumbnail, and changes the author
        else:
            fullFile = base[0] + exten
            if exten == ".mp3":
                fileConverter(vid, fullFile, DV, base)
"""

"""
    Original Code for trying to get a boss battle to work, pre Pygame
        Main = tk.Tk()
        
        
        MainFrame = tk.Frame(Main).grid(column=0, row=0)
        BossCanvas = tk.Canvas(MainFrame, background="grey")
        
        img= PhotoImage(file="images/DragonPlaceHolder.png")
        img = img.subsample(2,2)
        Player = BossCanvas.create_image(100, 130, image=img)
        
        #p = BossCanvas.coords(Player)
        
        #collisions = BossCanvas.find_overlapping(p[0], p[1], 0, 0)
        #collisions = list(collisions)
        #collisions.remove(Player)
        
        
        

        
        img2= PhotoImage(file="images/BossPlaceHolder.png")
        img2 = img2.subsample(2,2)
        Boss = BossCanvas.create_image(200, 130, image=img2)

        
        #Bindings
        Main.bind('w', lambda event: move("w"))
        Main.bind('a', lambda event: move("a"))
        Main.bind('s', lambda event: move("s"))
        Main.bind('d', lambda event: move("d"))
        P = BossCanvas.coords(Player)
        coll = BossCanvas.find_overlapping(P[0], P[1], 0, 0)
        coll = list(coll)
        coll.remove(Player)
        
            
        def collisionDetection():

            if len(coll) != 0:
                print('hit')
        
        def move(key):
            if key == "w":
                BossCanvas.move(Player, 0, -10)
                
            elif key == "a":
                BossCanvas.move(Player, -10, 0)
            
            elif key == "s": 
                BossCanvas.move(Player, 0, 10)
                
            elif key == "d":
                BossCanvas.move(Player, 10, 0 )
            
            collisionDetection()
        
        BossCanvas.grid(column=0, row=0)
        
        
        
        Main.mainloop()
"""