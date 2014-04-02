import pygame, os, sys
import Laser
import Battlecruiser
from Laser import Laser
from Battlecruiser import Battlecruiser
from Pear import EvilPear
from pygame.locals import *
from random import randint
from IntroScreen import PlayIntroScreen, load_image
from Stats import StatsPearGame



def PlayEndScreen(screen, cruiser, pears, Stats):
    #End of game loop that shows the screen frozen
    while Stats.stillGame == False:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                       pygame.quit()
                       sys.exit()
                    if event.key == K_n:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_y:
                        #reset still game so the player can break out of loop
                        #and play again
                        Stats.stillGame = True
                        

        #redraw background
        screen.fill((0, 0, 0))

        pears.draw(screen)

        cruiser.draw()
        cruiser.lasers.draw(screen)

        Stats.draw_healthBar()
                
        #print how many pears got by the ship
        font = pygame.font.Font(None, 24)
        text = font.render("Evil Pears Past Line: " + str(Stats.pearsPassed), 1, (255, 255, 255))
        screen.blit(text, (600, 0))

        #print how many pears have been killed
        font = pygame.font.Font(None, 24)
        text = font.render("Evil Pears Killed: " + str(Stats.pearsKilled), 1, (255, 255, 255))
        screen.blit(text, (20, 0))

        #print how many lasers have been fired
        font = pygame.font.Font(None, 24)
        text = font.render("Lasers Fired: " + str(Stats.lasersFired), 1, (255, 255, 255))
        screen.blit(text, (20, 20))

        #print how many pears have been generated in all
        font = pygame.font.Font(None, 24)
        text = font.render("Pears Generated: " + str(Stats.totalPears), 1, (255, 255, 255))
        screen.blit(text, (600, 20))

        #print the you lose text on screen
        font = pygame.font.Font(None, 50)
        text = "HAHA YOU LOSE! EVIL PEARS WIN!"
        printText = font.render(text, 1, (255, 0, 0))
        screen.blit(printText, ((screen.get_size()[0]/2) - 270, (screen.get_size()[1]/2) - 40))

        #print instructions to 
        font = pygame.font.Font(None, 30)
        text = "Play again ? (y/n)"
        printText = font.render(text, 1, (255, 0, 0))
        screen.blit(printText, ((screen.get_size()[0]/2) - 100, (screen.get_size()[1]/2) + 15))

        #draw sprites
        pygame.display.update()



    

