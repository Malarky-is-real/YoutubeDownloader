from PIL import Image
import tkinter as tk
import random
import time

#Sets up all the different animation files for develon
states = ["moving", "not_moving"]
moving_state = ["move_left", "move_right"]
idle_state = ["sleep", "idle"]
moving_file = ['images/DevelonFlyingFlipped.gif', 'images/DevelonFlying.gif']
idle_file = ['images/DevelonSleeping.gif', 'images/DevelonFlyingFlipped.gif', 'images/DevelonSleepingIdle.gif']
downloading_files = ["images/DownloadingDevelon.gif",'images/DevelonComplete.gif']
err_Files = ["images/Err.gif"]

class petAnimations(object):
    def __init__(self, rootObject, canv):
        self.root  = rootObject
        self.canvas = canv
        self.pet = ""
        self.file = ""
        self.action = ""
        self.anim = ""
        self.startPosX=166 
        self.startPosY=52
        self.canvas_width = 200
        self.canvas_height = 100
        self.IFCalreadyRan = False
    
    def eventVerify(self, newEvent):
        mak = self.action
        print("Original", mak)
        print("new " + newEvent)
        if newEvent == "move_left" and self.action == "move_right": 
            print("turn_left")
            self.action = newEvent
            self.switchAnims("switch_left")
            
        elif newEvent == "move_right" and self.action == "move_left":
            print("turn_right")
            self.action = newEvent
            self.switchAnims("switch_right")    
            
        else:
            self.action = newEvent
            self.fileconfigs(action = newEvent, changeCheck = 1)
    
    #Starts the animation loop  
    def eventStarter(self, action = None):
        act, direct = self.eventChange(action)
        self.move(direct)
        self.DevAnim = self.root.after(2000, lambda: self.eventStarter(action = act))
        
    def eventStopper(self):
        self.root.after_cancel(self.DevAnim)
    
    #Changes the animation that the pet is using
    def eventChange(self, action = None):
        #Develon Broad states
        state = random.choice(states)
        moveinc = 0
        change = 1

        #Checks if the state is 'moving' and then chooses a direction for the moving state
        if state == "moving":
            
            #Makes a random action from the moving states list the temporary action
            tempAction = random.choice(moving_state)
            
            
            #Checks if the action was the previous action and if so it stops resetting entirely.
            if tempAction == self.action: 
                
                change = 0
            
            #If the tempaction isn't the same as the previous action then you continue with the animation changing. 
            else:

                    
                self.action = tempAction
                
            
            #If specific action is left then put move increment to move the pet left, opposite for move right
            if action == "move_left":
                moveinc = -1
                
                if change == 0:
                    return action, moveinc
            
            else:
                moveinc = 1
                
                if change == 0:
                    return action, moveinc
            
        #if not moving then choose between different idling states
        else: 
            tempAction = random.choice(idle_state)
            moveinc = 0
            if tempAction == action:
                
                return action, moveinc
                
            else: 
                self.action = tempAction
                
        
        self.fileconfigs(self.action, change)
        return self.action, moveinc
    
    def switchAnims(self, switchAction): 
        if switchAction == "switch_right":
            print("move right")
            self.imageFileConfig("images/DevelonTurnsRight.gif", "turn_right")
        if switchAction == "switch_left":
            self.imageFileConfig("images/DevelonTurnsleft.gif", "turn_left")
        
        
    def fileconfigs(self, action, changeCheck):
        #File specific checker:
        if changeCheck == 1:
            if action == "move_right":
                self.action = "move_right"
                file = moving_file[0]
                
            elif action == "move_left":
                self.action = "move_left"
                file  = moving_file[1]

            elif action == "sleep":
                self.action = "sleep"
                file  = idle_file[0]
            
            elif action == "idle":
                self.action = "idle"
                file = idle_file[1]

            self.imageFileConfig(file, action)
        
            
    def imageFileConfig(self, file, action):
        
        if self.IFCalreadyRan == True:
            self.root.after_cancel(self.anim)  
        
        info = Image.open(file)
        frames = info.n_frames
        imgs = [tk.PhotoImage(file=file, format=f'gif -index {i}') for i in range(frames)]
        myImage = tk.PhotoImage(file=file)
        
        if self.IFCalreadyRan == False:
            self.pet = self.canvas.create_image(self.startPosX-64,self.startPosY, image=myImage)
            self.IFCalreadyRan = True
        
        else:
            
            try: 
                self.canvas.itemconfigure(self.pet, image=myImage)
            
            except:
                self.pet = self.canvas.create_image(self.startPosX-64,self.startPosY, image=myImage)
                self.canvas.itemconfigure(self.pet, image=myImage)
        
        self.IFCalreadyRan = True    
        self.animation(imgs, frames, cnt = 0, action = action)
        
    def animation(self, imgs, frames = 0, cnt=0, action = None):
        
        cnt += 1
        if action == "sleep" and cnt >= frames - 1:
            cnt = frames - 1
        
        elif action == "turn_right" and cnt >= frames - 1:
            self.action = "move_right"
            self.next_gif("move_right", False)
            
        
        elif action == "turn_left" and cnt >= frames - 1:
            self.action = "move_left"
            self.next_gif("move_left", False)
            
            
        
        elif cnt == frames:        
            cnt = 0
            
        
        im2 = imgs[cnt]
        self.canvas.itemconfig(self.pet, image=im2)
        self.anim = self.root.after(100, lambda: self.animation(imgs, frames, cnt, action))


    def next_gif(self, action, wall):
        file = "images/Err.gif"
        
        if action == "move_left":
            file = moving_file[1]
            self.imageFileConfig(file, action = None)
            if wall:
                self.canvas.move(self.pet, -10, 0)

        elif action == "move_right":
            file = moving_file[0]
            self.imageFileConfig(file, action = None)
            if wall:
                self.canvas.move(self.pet, 10, 0)


        elif action == "sleep":
            file = 'images/DevelonSleeping.gif'
            self.imageFileConfig(file, action = None)
            
            
            
        self.imageFileConfig(file, action = None)

    def move(self, moveIncrem):
        xinc = moveIncrem
        change = 0
        flyingtime = random.randint(10,30)
        timeFlewn = 0
        
        while timeFlewn != flyingtime:
            develonpos = self.canvas.coords(self.pet)
            timeFlewn += 1
            self.canvas.move(self.pet, xinc, 0)
            self.root.update()
            time.sleep(0.01)
            al = develonpos[0]
            if al < abs(xinc) or al > self.canvas_width - abs(xinc):
                change *= -1
                xinc = -xinc
                timeFlewn  += 1
                if al < abs(xinc):
                    direction = "move_right-wall"
                
                elif self.canvas_width - abs(xinc):
                    direction = "move_left-wall"
                self.next_gif(direction)



            
   
    
    def downloadAnim(self, STF):
        self.root.after_cancel(self.DevAnim)
        file = downloading_files[0]
        self.imageFileConfig(file, action = None)
        self.move(0)

    def finish(self): 
        self.imageFileConfig(downloading_files[1], action=None)
        time.sleep(5)
        self.root.after_cancel(self.anim) 
        self.eventStarter()

