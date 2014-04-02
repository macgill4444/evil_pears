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
from EndScreen import PlayEndScreen


DOKILL = 1
DONTKILL = 0

COUNTERCLOCK = 1
CLOCKWISE = -1



def checkCollisions(lasers, pears):
    '''checks for collisions between two groups, the lasers and pears, and calls the ncessary functions for each collision'''

    collisionsL = pygame.sprite.groupcollide(lasers, pears, DONTKILL, DONTKILL)#dokill dontkill
    collisionsP = pygame.sprite.groupcollide(pears, lasers, DONTKILL, DONTKILL)

    for laser in collisionsL:
        #create an explosion w sound and convert laser to explosion gif
        laser.collideExplosion()

    for pear in collisionsP:
        pear.beenHit()

def main():
    #check for sound & font

    #Constants
    FPS = 50
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    BACKGROUND_COLOR = (0, 0, 0)

    #INIT pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('Battlecruiser demo')
    clock = pygame.time.Clock()

    #set pygame keyboard repeat
    pygame.key.set_repeat(100,100 )

    #creates a class that holds the game stats
    Stats = StatsPearGame(screen, 0, 0, 0, 0, 0, 280, 2)

    #create battlecrusier
    #cruiser = Battlecruiser(screen, (screen.get_size()[0]/2.0), (screen.get_size()[1]/2.0), 15, 15)
    cruiser = Battlecruiser(screen, 337, 100, 0, 0, Stats)

    #creat group of pears
    pears = pygame.sprite.Group()

    #other variables
    tick = 0
    modAmount = 40 #sets how quickly pears are generated
    

    #sets up intro screen loop, see IntroScreen.py 
    PlayIntroScreen(screen)
       
#Game loop, keep playing until health bar runs out
    while Stats.stillGame:
        time_passed = clock.tick(FPS)
        tick = tick + 1

        #add a new pear to the screen every 20th tick
        if Stats.pearsKilled > 5 and Stats.pearsKilled <= 10:
            modAmount = 30
        elif Stats.pearsKilled > 10 and Stats.pearsKilled <= 20:
            modAmount = 20
        elif Stats.pearsKilled > 20 and Stats.pearsKilled <= 30:
            modAmount = 10
        elif Stats.pearsKilled > 30:
            modAmount = 5
       
 
        if tick % modAmount == 0:
            pears.add(EvilPear(screen, randint(2, screen.get_size()[0]), screen.get_size()[1], 0, -1, Stats))
            Stats.incre_totalPears()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                       pygame.quit()
                       sys.exit()
                    if event.key == K_UP:
                        cruiser.jump("UP")
                    if event.key == K_DOWN:
                        cruiser.jump("DOWN")
                    if event.key == K_RIGHT:
                        cruiser.jump("RIGHT")
                    if event.key == K_LEFT:
                        cruiser.jump("LEFT")
                    if event.key == K_SPACE:
                        cruiser.fire()
                    if event.key == K_f:
                        cruiser.rotate(COUNTERCLOCK)
                    if event.key == K_d:
                        cruiser.rotate(CLOCKWISE)

        #redraw background
        screen.fill(BACKGROUND_COLOR)

        #check for collisions
        checkCollisions(cruiser.lasers, pears)

        #draw and update the pears
        pears.update()
        pears.draw(screen)

        #update and draw battlecruiser & lasers
        cruiser.update()
        cruiser.draw()
        cruiser.lasers.update()
        cruiser.lasers.draw(screen)

        #update and draw health bar from Stats
        Stats.update_healthBar()
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

        #draw sprites
        pygame.display.update()

        #clean up all the dead lasers
        for laser in cruiser.lasers:
            laser.killTime()
    
    PlayEndScreen(screen, cruiser, pears, Stats)
            

        
if __name__ == "__main__":
    while True:
        main()
