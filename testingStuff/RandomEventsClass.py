import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk
import pygame
import sys

class RandomEvents(object):
    
    def __init__(self):
        pass
    
    def bossEvent(self):
        #PyGame Setup
        pygame.init()
        "pygame.quit() exit()"
        pygame.font.init()
        screen = pygame.display.set_mode((800, 400))
        clock = pygame.time.Clock()
        pygame.display.set_caption("BOSS")
        running = True
        gameRunning = True
        test_font = pygame.font.Font(None, 50)
        
        testSurface = pygame.image.load("images/DevelonDownloaderNew.png").convert()
        testGround = pygame.Surface((800, 200))
        testGround.fill("darkgrey")
        
        
        testEnemy = pygame.image.load("images/BossPlaceHolder.png").convert_alpha()
        enemyRect = testEnemy.get_rect(midbottom = (400, 300))
        direction = 10
       
        playerSurface = pygame.image.load("images/DragonPlaceHolder.png").convert_alpha()
        playerRect = playerSurface.get_rect(midbottom = (80,300))
        playerHealth = 5
        invincible = False
        
        attackObj = pygame.image.load("images/MusicNote.png").convert_alpha()
        attackRect = attackObj.get_rect(midbottom = playerRect.midbottom)
        attackXCoord = 0
        attackYCoord = 0
        attack = False
        alive = False
                
        directBool = True
        boss_Attack = False
        player_Attack = False    
        moveInt = 5   
        attackType = ""
        
        def charAttack(player, attackerRect, alive, attackX, spawn_YCoord, direction, moveInt):
            #Checks if an attack already exists. 
            if not alive:
                #Gets the location the space button was pressed at
                if direction:
                    attackX = attackerRect.midbottom[0] + 20
                    moveInt = 5
                else: 
                    attackX = attackerRect.midbottom[0] - 20
                    moveInt = -5
                    
                spawn_YCoord = attackerRect.midbottom[1]
                alive = True
            
            #Updates the attack object to match the screen
            attackRect = attackObj.get_rect(midbottom = (attackX, spawn_YCoord))
            screen.blit(attackObj, attackRect)
            
            #Moves the attack so long as it is not off the screen or it doesn't hit the boss
            if attackRect.left < 810 and attackRect.left > -50  and attackRect.colliderect(enemyRect) == False:
                attackX += moveInt
                player = True
                return player, alive, attackX, spawn_YCoord, moveInt
                
                
            else: 
                alive = False
                player = False
                attackRect.left = 80
                return player, alive, 80, 300, moveInt
        
        def bossAttack(playerRect, enemyRect, type, direction):
            if attackType == "spin":
                if playerRect.right > enemyRect.right:
                    playerRect.x -= 2
                    
                if playerRect.right < enemyRect.right:
                    playerRect.x += 2
                
                if playerRect.top < enemyRect.top:
                    playerRect.y += 2
                
                if playerRect.bottom > enemyRect.bottom:
                    playerRect.y -= 2
                    
            if attackType == "dash":    
                if enemyRect.right == -100 or enemyRect.right == 1000:
                    direction *= -1
                    enemyRect.right += (10 * direction)
                    print("direction = ", direction)
        
   
            return direction



        while running:
            
            #checks for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False  
                
                #Checks if the player presses a button 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        attack = True
                        player_Attack = True
                    
                    if event.key == pygame.K_l:
                        attack = True
                        boss_Attack = True
                        attackType = "spin" 
                    
                    if event.key == pygame.K_p:
                        attack = True
                        boss_Attack = True
                        attackType = "dash" 
                        
            
            #Runs the whole game
            if gameRunning:    
                
                screen.fill("blue")
                screen.blit(testSurface, (0,0))
                screen.blit(testGround, (0, 300))
                #screen.blit(textSurface, (0, 200))
                screen.blit(testEnemy, enemyRect)
                screen.blit(playerSurface, playerRect)

                #Creates the players attack
                if attack:
                    if player_Attack:
                        player_Attack, alive, attackXCoord, attackYCoord, moveInt = charAttack("player", playerRect, alive, attackXCoord, attackYCoord, directBool, moveInt)
                    
                    if boss_Attack:
                        direction = bossAttack(playerRect, enemyRect, attackType, direction = direction)
                        
                
                if playerRect.colliderect(enemyRect) and invincible != True:
                    playerHealth -= 1
                    print("hit")
                    invincible = True
                    if attackType == "spin": 
                        boss_Attack = False

                if playerRect.colliderect(enemyRect) == False: 
                    invincible = False
                    
                
                
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    playerRect.top -= 5 
                if keys[pygame.K_s]:
                    playerRect.top += 5
                if keys[pygame.K_a]:
                    playerRect.left -= 5 
                    directBool = False
                if keys[pygame.K_d]:
                    playerRect.left += 5
                    directBool = True
                
                
                
                if playerHealth == 0:
                    gameRunning = False
                
                
                    
            else: 
                screen.fill("Red")
                
        
            #Draws all the elements  
            pygame.display.update()
            clock.tick(60)
            
        pygame.quit()
        
