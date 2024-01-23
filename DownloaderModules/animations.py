from PIL import Image
import tkinter as tk
import random
import time

#Sets up all the different animation files for develon
class petAnimations(object):
    def __init__(self, rootObject, canv):
        self.root  = rootObject
        self.canvas = canv
        self.pet = ""
        self.action = ""
        self.DevAnim = ""
        self.anim = ""
        self.startPosX=166 
        self.startPosY=52
        self.canvas_width = 200
        self.canvas_height = 100
        self.IFCalreadyRan = False
        self.states = ["moving", "not_moving"]
        self.moving_state = ["move_left", "move_right"]
        self.idle_state = ["sleep", "idle"]
        self.moving_file = ['images/DevelonFlyingFlipped.gif', 'images/DevelonFlying.gif']
        self.idle_file = ['images/DevelonSleeping.gif', 'images/DevelonFlyingFlipped.gif', 'images/DevelonSleepingIdle.gif']
        self.downloading_files = ["images/DownloadingDevelon.gif",'images/DevelonComplete.gif']
        self.err_Files = ["images/Err.gif"]
            
    def override(self):
        overridingAction = input("Input a new action: ")

    #Starts the animation loop  
    def eventStarter(self, action = None):
        direct = self.eventChange(action)
        self.move(direct)
        self.DevAnim = self.root.after(2000, lambda: self.eventStarter(action = self.action))
        
    def eventPauser(self, direct):
        self.move(direct)
        self.DevAnim = self.root.after(2000, lambda: self.eventStarter(action = self.action))
        
    def eventStopper(self):
        self.root.after_cancel(self.DevAnim)
    
    def switchAnims(self, switchAction): 
        if switchAction == "switch_right":
            
            self.imageFileConfig("images/DevelonTurnsRight.gif", "turn_right")
            
        if switchAction == "switch_left":
            self.imageFileConfig("images/DevelonTurnsleft.gif", "turn_left")
    
    #Changes the animation that the pet is using
    def eventChange(self, action = None):
        #Develon Broad states
        state = "moving"
        # state = random.choice(states)
        moveinc = 0
        change = 1

        #Checks if the state is 'moving' and then chooses a direction for the moving state
        if state == "moving":
            
            #Makes a random action from the moving states list the temporary action
            tempAction = random.choice(self.moving_state)
            
            
            #Checks if the action was the previous action and if so it stops resetting entirely.
            if tempAction == self.action: 
                change = 0
            
            #If the tempaction isn't the same as the previous action then you continue with the animation changing. 
            else:
                action = tempAction
                
            del tempAction
            #If specific action is left then put move increment to move the pet left, opposite for move right
            if action == "move_left":
                moveinc = -1
                
                if change == 0:
                    return moveinc
            
            else:
                moveinc = 1
                
                if change == 0:
                    return moveinc
            
        #if not moving then choose between different idling states
        else: 
            tempAction = random.choice(self.idle_state)
            moveinc = 0
            if tempAction == self.action:
                del tempAction
                return moveinc
                
            else: 
                action = tempAction
                del tempAction
        self.fileconfigs(action, True)        
        return moveinc

    def eventVerify(self, newEvent):
        #print(self.action, " --> ", newEvent)
        if newEvent == "move_left" and self.action == "move_right": 
            print("Changing")
            self.action = newEvent
            self.eventStopper()
            self.switchAnims("switch_left")
            self.eventPauser(-1)
            
        elif newEvent == "move_right" and self.action == "move_left":
            #print("Changing")
            self.action = newEvent
            self.eventStopper()
            self.switchAnims("switch_right")
            self.eventPauser(1)
        
        else:
            self.action = newEvent
            self.fileconfigs(action = newEvent, changeCheck = True)
 
    def fileconfigs(self, action, changeCheck):
        #File specific checker:
        if changeCheck:
            if action == "move_right":
                self.action = "move_right"
                file = self.moving_file[0]
                
            elif action == "move_left":
                self.action = "move_left"
                file  = self.moving_file[1]

            elif action == "sleep":
                self.action = "sleep"
                file  = self.idle_file[0]
            
            elif action == "idle":
                self.action = "idle"
                file = self.idle_file[1]
            
            elif action == "Err":
                self.action = "Err"
                file = self.err_Files[0]

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
        if action == "finish":
            return imgs, frames, action     
        else:
            self.animation(imgs, frames, cnt = 0, action = action)
        
        
    def animation(self, imgs, frames = 0, cnt=0, action = None):
        
        cnt += 1

        if action == "sleep" and cnt >= frames - 1:
            cnt = frames - 1
        
        elif action == "turn_right" and cnt >= frames - 1:
            self.action = "move_right"
            self.next_gif("move_right")
            
        
        elif action == "turn_left" :
            self.action = "move_left"
            self.next_gif("move_left")
            
            
        
        elif cnt == frames:        
            cnt = 0
            
        self.canvas.itemconfig(self.pet, image=imgs[cnt])
        self.anim = self.root.after(100, lambda: self.animation(imgs, frames, cnt, action))


    def next_gif(self, nextAction):
        file = "images/Err.gif"
        
        if nextAction == "move_left":
            file = self.moving_file[1]
            self.imageFileConfig(file, action = None)
                

        elif nextAction == "move_right":
            file = self.moving_file[0]
            self.imageFileConfig(file, action = None)

        elif nextAction == "sleep":
            file = 'images/DevelonSleeping.gif'
            self.imageFileConfig(file, action = None)
            
            
        self.action = nextAction
        self.imageFileConfig(file, action = None)

    def move(self, moveIncrem):
        xinc = moveIncrem
        #print("xinc", xinc)
        change = 0
        flyingtime = random.randint(10,30)
        timeFlewn = 0
        wall = False
        
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
                    direction = "move_right"
                    self.canvas.move(self.pet, 10, 0)
                    
                elif self.canvas_width - abs(xinc):
                    direction = "move_left"
                    self.canvas.move(self.pet, -10, 0)
                
                self.next_gif(direction)



            
   
    
    def downloadAnim(self):
        if self.DevAnim != "":
            self.root.after_cancel(self.DevAnim)
        file = self.downloading_files[0]
        self.imageFileConfig(file, action = None)
        self.move(0)

    def finish(self): 
        imgs, frames, action = self.imageFileConfig(self.downloading_files[1], action="finish")
        self.animation(imgs, frames, cnt = 0, action = action)
        
        #self.root.after_cancel(self.anim) 
        #self.eventStarter()


