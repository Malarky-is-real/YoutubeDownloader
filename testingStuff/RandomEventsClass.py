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
        textSurface = test_font.render("Boss", False,pygame.Color('red'))
        
        testEnemy = pygame.image.load("images/BossPlaceHolder.png").convert_alpha()
        enemyRect = testEnemy.get_rect(midbottom = (400, 300))
        
       
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
                
        
        attacker = ""        
        
        def charAttack(attacker, attackerRect, alive, attackX, spawn_YCoord):
            #Checks if an attack already exists. 
            if not alive:
                #Gets the location the space button was pressed at
                attackX = attackerRect.midbottom[0] + 20
                spawn_YCoord = attackerRect.midbottom[1]
                alive = True
            
            #Updates the attack object to match the screen
            attackRect = attackObj.get_rect(midbottom = (attackX, spawn_YCoord))
            screen.blit(attackObj, attackRect)
            
            #Moves the attack so long as it is not off the screen or it doesn't hit the boss
            if attackRect.left < 810 and attackRect.colliderect(enemyRect) == False:
                attackX += 5
                attack = True
                return attack, alive, attackX, spawn_YCoord
                
                
            else: 
                attack = False
                alive = False
                attackRect.left = 80
                print("del")
                return attack, alive, 80, 300
        
        def bossAttack(playerRect, enemyRect):
            if playerRect.right > enemyRect.right:
                playerRect.x -= 2
                print("sucking left")
                
            if playerRect.right < enemyRect.right:
                playerRect.x += 2
                print("sucking right")
            
            if playerRect.top < enemyRect.top:
                playerRect.y += 2
                print("sucking down")
            


        while running:
            
            #checks for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False  
                
                #Checks if the player presses a button 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        attack = True
                        attacker = "player"
                    
                    if event.key == pygame.K_l:
                        attack = True
                        attacker = "boss"
                
            #Runs the whole game
            if gameRunning:    
                
                screen.fill("blue")
                screen.blit(testSurface, (0,0))
                screen.blit(testGround, (0, 300))
                screen.blit(textSurface, (0, 200))
                #enemyRect.right -=1
                #if enemyRect.right < -100:
                #    enemyRect.left = 900

                screen.blit(testEnemy, enemyRect)
                screen.blit(playerSurface, playerRect)

                #Creates the players attack
                if attack:
                    if attacker == "player":
                        attack, alive, attackXCoord, attackYCoord = charAttack("player", playerRect, alive, attackXCoord, attackYCoord)
                    
                    elif attacker == "boss":
                        bossAttack(playerRect, enemyRect)
                        
                
                if playerRect.colliderect(enemyRect) and invincible != True:
                    playerHealth -= 1
                    print("hit")
                    invincible = True
                    attack = False

                if playerRect.colliderect(enemyRect) == False: 
                    invincible = False
                    
                
                #Player 
                #pygame.draw.circle(screen, "grey", player_pos, 40)
                
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    playerRect.top -= 5 
                if keys[pygame.K_s]:
                    playerRect.top += 5
                if keys[pygame.K_a]:
                    playerRect.left -= 5 
                if keys[pygame.K_d]:
                    playerRect.left += 5
                
                
                
                if playerHealth == 0:
                    gameRunning = False
                
                
                    
            else: 
                screen.fill("Red")
                
        
            #Draws all the elements  
            pygame.display.update()
            dt = clock.tick(60) / 1000
            
        pygame.quit()
        
