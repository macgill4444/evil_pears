import pygame, os, sys
import Laser
import Battlecruiser
import Enemy
from Laser import Laser
from Battlecruiser import Battlecruiser
from Enemy import Enemy
from pygame.locals import *
from random import randint
from Stats import StatsPearGame


DOKILL = 1
DONTKILL = 0

def cruiserCollision(cruiser, enemies):
    collisions = pygame.sprite.spritecollide(cruiser, enemies, DONTKILL)
    if len(collisions) > 0:
        cruiser.beenHit()
    

def checkCollisions(lasers, enemies, Stats):
    '''checks for collisions between two groups, the lasers and pears, and calls the ncessary functions for each collision'''

    collisionsL = pygame.sprite.groupcollide(lasers, enemies, DONTKILL, DONTKILL)
    collisionsE = pygame.sprite.groupcollide(enemies, lasers, DONTKILL, DONTKILL)

    for laser in collisionsL:
        #create an explosion w sound and convert laser to explosion gif
        Stats.total_collisions += 100
        laser.collideExplosion()

    for enemies in collisionsE:
        enemies.beenHit()


def load_image(image_name):
    ''' The proper way to load an image '''
    try:
        image = pygame.image.load(image_name)
    except pygame.error, message:
        print "Cannot load image: " + image_name
        raise SystemExit, message
    return image.convert_alpha()



def main():
    #check for sound and font
    if not pygame.font:
        print "Warning, fonts disabled"
    if not pygame.mixer:
        print "Warning, sound disabled"

    #Constants
    FPS = 50
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    COUNTERCLOCK = 1
    CLOCKWISE = -1


    #INIT pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('Battlecruiser demo')
    clock = pygame.time.Clock()

    #get background image
    BACKGROUND_IMAGE = load_image('assets/ram_aras.png')
    back_imagex = 0
    back_imagey = 0

    game_score = 0

    #set pygame keyboard repeat
    pygame.key.set_repeat(100,100 )

    #creates a class that holds the game stats
    Stats = StatsPearGame(screen, 0, 0, 0, 0, 0, 280, 2)

    #creates a battlecruiser
    cruiser = Battlecruiser(screen, 337, 100, 0, 0, Stats)

    #create a group of mutalisks
    mutalisks = pygame.sprite.Group()
    
    #boolean to let us know whether we should keep updating things (ie the game is still going on
    updates = True

    #other variables
    tick = 0


    while True:
        tick += 1

        if tick % 10 == 0:
            mutalisks.add(Enemy(screen, randint(30, screen.get_size()[0] - 80), screen.get_size()[1] + 10, randint(-1, 1), randint(-4, -1), cruiser))
        
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


        #update and move background
        if updates == True:
            #check for collisions between lasers and mutalisks
            checkCollisions(cruiser.lasers, mutalisks, Stats)
            #check for collision between cruiser and mutalisks
            cruiserCollision(cruiser, mutalisks)

            cruiser.update()
            cruiser.lasers.update()
            mutalisks.update()
            #keep moving image
            back_imagey -= 1

        #check to see if we should keep moving ships
        if (back_imagey + BACKGROUND_IMAGE.get_size()[1]) - screen.get_size()[1] <= 0:
            updates = False

        #redraw background
        screen.blit(BACKGROUND_IMAGE, (back_imagex,back_imagey))
        
        cruiser.draw()
        cruiser.lasers.draw(screen)
        mutalisks.draw(screen)

        #print game score
        font = pygame.font.Font(None, 24)
        text = font.render("Game Score: " + str(Stats.total_collisions), 1, (255, 255, 255))
        screen.blit(text, (20, 5))

        if updates == False:
            #print game over
            font = pygame.font.Font(None, 48)
            text = font.render("GAME OVER ", 1, (255, 255, 255))
            screen.blit(text, ((screen.get_size()[0]/2) - 100, (screen.get_size()[1]/2) - 20))
            if cruiser.active == True:
                text = font.render("You win!", 1, (255, 255, 255))
                screen.blit(text, ((screen.get_size()[0]/2) - 80, (screen.get_size()[1]/2)+ 10))
            else:
                text = font.render("You lose!", 1, (255, 255, 255))
                screen.blit(text, ((screen.get_size()[0]/2) - 80, (screen.get_size()[1]/2)+ 10))


        #draw sprites
        pygame.display.update()

        #clean up all the dead lasers and exploded mutalisks
        for laser in cruiser.lasers:
            laser.killTime()
            
        for muta in mutalisks:
            muta.killTime()

        if cruiser.active == False:
            updates = False

if __name__ == "__main__":
    while True:
        main()
