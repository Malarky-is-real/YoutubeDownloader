import pygame 
import sys
import random 
#Boss Battle for the Random Events feature of the Develon Downloader

#Important game variables
pygame.init()
pygame.font.init()
screenW = 800
screenH = 600
screen = pygame.display.set_mode((screenW, screenH))
clock = pygame.time.Clock()

pygame.display.set_caption("BOSS")

mainMenu = True
gameRunning = True
mainFont = pygame.font.Font(None, 50)
running = True

#Image Loading | Alpha for transparent images
testSurface = pygame.image.load("images/DevelonDownloaderNew.png").convert()
enemySurface = pygame.image.load("images/BossPlaceHolder.png").convert_alpha()
playerSurface = pygame.image.load("images/DragonPlaceHolder.png").convert_alpha()
attackSurface = pygame.image.load("images/MusicNote.png").convert_alpha()
buttonSurface = pygame.image.load("images/Leg_Back.png").convert()

#Rects 
playerRect = playerSurface.get_rect(midbottom = (80,300))
attackRect = attackSurface.get_rect(midbottom = playerRect.midbottom)
enemyRect = enemySurface.get_rect(midbottom = (400, 300))
buttonRect = buttonSurface.get_rect(midbottom = (300, 400))

#TextRects
menuBackground = pygame.Surface((800, 200))
statsBackground = pygame.Surface((800, 200))

class Player(object):
    def __init__(self, playerRect, image, attackSurface):
        #CreationVars
        self.img = image
        self.attackRect = attackSurface
        self.playerRect = playerRect
        
        #Fill_In
        self.moveInt = 0
        self.directBool = True
        self.Invulnerable = False
        self.health = 5
    
    def draw(self):
        screen.blit(self.img, playerRect)
    
    def input(self, keys):      
        if keys[pygame.K_w] and playerRect.top >= 5:
            playerRect.top -= 4
        
        if keys[pygame.K_s] and playerRect.bottom <= 495:
            playerRect.top += 4
        
        if keys[pygame.K_a] and playerRect.left >= 5:
            playerRect.left -= 4 
            self.directBool = False
        
        if keys[pygame.K_d] and playerRect.right <= 795:
            playerRect.left += 4
            self.directBool = True
        
        if keys[pygame.K_SPACE] and "playerAttack" not in gameObjs:
            self.Attack(self.directBool, enemyRect)
    
    def checkCollision(self, obj):
        if self.playerRect.colliderect(obj) and not self.Invulnerable :
            self.health -= 1
            self.Invulnerable = True
            
        elif playerRect.colliderect(enemyRect) == False: 
            self.Invulnerable = False
            
        
        
            
    moveInt = 5
    def Attack(self, direction, bossRect):
        if "playerAttack" not in gameObjs:
            if direction:
                attackX = self.playerRect.midbottom[0] + 20
                self.moveInt = 5
            else: 
                attackX = self.playerRect.midbottom[0] - 20
                self.moveInt = -5
            self.attackRect.y = playerRect.y
            self.attackRect.x = attackX
            gameObjs.append("playerAttack")
            
        if (attackRect.right <= 810 and attackRect.left >= -50) and attackRect.colliderect(bossRect) == False:
            screen.blit(attackSurface, attackRect)
            attackRect.centerx += self.moveInt
        else: 
            print("gone")
            gameObjs.remove("playerAttack")
    
    def getHealth(self):
        return self.health
              
        
class GUI(object):
    def __init__(self):
        self.buttonPress = False
        
    #Button Function
    def buttons(self):
        mousePos = pygame.mouse.get_pos()
        if buttonRect.collidepoint(mousePos):
            if pygame.mouse.get_pressed(num_buttons=3)[0] and self.buttonPress == False:
                self.buttonPress = True    
                return True    
            
            else: 
                return False           
        else: 
            self.buttonPress = False
            return False
    

    def stats(self, New, health):
        if New:
            statsBackground = pygame.Surface((800, 200))
            statsBackground.fill("darkgrey")
            playerNameText = mainFont.render("Player: Develon Health: ", False,pygame.Color('red'))
            return statsBackground, playerNameText
        
        else:
            
            playerhealthText = mainFont.render("Health: " + str(health), False,pygame.Color('red'))
            return playerhealthText

class Boss(object):
    def __init__(self, rect, image):
        self.bossRect = rect
        self.img = image
        self.direction = -5
        self.leveledNum = 0
        self.dashNum = 0
        self.dashNum = 0

    def draw(self):
        screen.blit(self.img, self.bossRect)
    
    def neutral(self):
        self.bossRect
    
    #Bosses Spin Attack, sucks in player towards boss
    def spinAttack(self, playRect):
        
        if "bossAttack" in gameObjs:
            
            if playRect.right > enemyRect.right:
                playerRect.x -= 2
                
            if playRect.right < enemyRect.right:
                playerRect.x += 2
            
            if playRect.top < enemyRect.top:
                playerRect.y += 2
            
            if playRect.bottom > enemyRect.bottom:
                playerRect.y -= 2
            
            if playRect.colliderect(self.bossRect):

                gameObjs.remove("bossAttack")
    
    #Boss Follows the player only on the y coordinate
    def followPlayer(self):
        if self.leveledNum != 500:  
            if self.bossRect.y != playerRect.y:
                if playerRect.centery < self.bossRect.centery:
                    self.bossRect.y -= 2
                
                elif playerRect.centery > self.bossRect.centery:
                    self.bossRect.y += 2

            self.leveledNum += 1
        
        else: 
            self.dashAttack(random.randint(1, 4))
            
    #Boss dashes left and right
    def dashAttack(self, maxDash): 
        if self.dashNum < maxDash:
            if self.bossRect.right <= -100 or self.bossRect.right == 1000:
                self.direction = (-1 * self.direction)
                self.bossRect.right += (10 * self.direction)    
                self.dashNum += 1                
            enemyRect.right += self.direction
        
        elif self.bossRect.centerx != 400:
            
            if self.direction < 0 and self.bossRect.x < 475:
                self.direction += .1
                
            
            if self.direction > 0 and self.bossRect.x > 225:
                self.direction -= .1
            
            enemyRect.right += self.direction


        


         
class gameStates(object):
    def __init__(self):
        self.gameGUI = GUI()
        self.player = Player(playerRect, playerSurface, attackRect)
        self.boss = Boss(enemyRect, enemySurface)   
        self.health = self.player.getHealth()
        self.stats, self.playerText = self.gameGUI.stats(True, self.health)
        self.gameOn = False
        

        
    #Main Menu
    def mainMenu(self):
    
        self.gameOn = self.gameGUI.buttons()       
        
        screen.fill("grey")
        screen.blit(mainFont.render("Random Events", False, "red" ), (250, 100))
        statsBackground.fill("darkgrey")        
        screen.blit(buttonSurface, buttonRect)
    
        
    #The Main Game
    def mainGame(self):
        #Function update
        playerHealthTxt = self.gameGUI.stats(False, self.player.getHealth())

        screen.fill("skyblue") 

        #Draws characters to the screen
        screen.blit(self.stats, (0, 500))
        screen.blit(self.playerText, (0, 510))
        screen.blit(playerHealthTxt, (0, 550))
        self.player.draw()
        self.boss.draw()
        
    
        self.player.input(pygame.key.get_pressed())
        if "playerAttack" in gameObjs:
            self.player.Attack(None, enemyRect)
        
        self.boss.followPlayer()
        self.player.checkCollision(enemyRect)
        
    def gameCaller(self):
        if self.gameOn == False: 
            self.mainMenu()
        else:
            self.mainGame()
        
#important game vars

#Class Calling

fullGame = gameStates()

gameObjs = []
gameObjs.append("bossAttack")

while running: #Runs the game

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                    running = False 
                    

    fullGame.gameCaller()


  
    pygame.display.update()
    clock.tick(60)
