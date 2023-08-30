import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk

class RandomEvents(object):
    
    def __init__(self):
        pass
    
    def bossEvent(self):

        
        Main = tk.Tk()
        
        
        MainFrame = tk.Frame(Main).grid(column=0, row=0)
        BossCanvas = tk.Canvas(MainFrame, background="grey")
        
        img= PhotoImage(file="images/DragonPlaceHolder.png")
        img = img.subsample(2,2)
        Player = BossCanvas.create_image(100, 130, image=img)
        
        p = BossCanvas.coords(Player)
        print(p)
        collisions = BossCanvas.find_overlapping(p[0], p[1], 0, 0)
        collisions = list(collisions)
        collisions.remove(Player)
        
        
        

        
        img2= PhotoImage(file="images/BossPlaceHolder.png")
        img2 = img2.subsample(2,2)
        Boss = BossCanvas.create_image(200, 130, image=img2)

        
        #Bindings
        Main.bind('w', lambda event: move("w"))
        Main.bind('a', lambda event: move("a"))
        Main.bind('s', lambda event: move("s"))
        Main.bind('d', lambda event: move("d"))
        
        
            
        def collisionDetection():
            PB = BossCanvas.bbox(Player)
            BB = BossCanvas.bbox(Boss)
            if BB[0] < PB[2] < BB[2] and BB[1] < PB[1] < BB[3]:
                print("Hit")
                BossCanvas.move(Boss, 100, 100)
        
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
        
        