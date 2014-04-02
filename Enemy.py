import pygame, os, sys
from pygame.locals import *
from random import randint
from Battlecruiser import Battlecruiser
#trouble with collisions because mutalisk collides with itself, just make a list instead of using a group and reverse x 


class Enemy(pygame.sprite.Sprite):
    '''An enemy flying mutalisk'''
    def load_image(self, image_name):
        try:
            image = pygame.image.load(image_name)
            image = image.convert_alpha()
        except pygame.error, message:
            print "Cannot load image " + image_name
            raise SystemExit, message
        return image

    def __init__(self, screen, init_x, init_y, init_dx, init_dy, battleShip):
        '''makes a enemy class at the x,y coords and initial x,y speed, and a copy of the battlecruiser'''
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen

        self.image = self.load_image('assets/mutalisk.gif')
        self.image_w = self.image.get_width()
        self.image_h = self.image.get_height()

        self.rect = self.image.get_rect()

        self.rect.x = init_x
        self.rect.y = init_y

        self.x = init_x
        self.y = init_y

        self.dx = init_dx
        self.dy = init_dy

        self.active = True

        self.thePlayer = battleShip

        self.collidedMuta = False #boolean that 

    def update(self):
        ''' for moving '''
        if self.thePlayer == None:
            self.rect.y += self.dy
            self.y += self.dy
            self.rect.x += self.dx
            self.x += self.dx
            self.rect.move(self.rect.x, self.rect.y)
        else:
            if self.thePlayer.rect.x < self.rect.x:
                self.rect.x = self.rect.x - 2
            if self.thePlayer.rect.x > self.rect.x:
                self.rect.x = self.rect.x + 2
            if self.thePlayer.rect.y < self.rect.y:
                self.rect.y = self.rect.y - 2
            if self.thePlayer.rect.y > self.rect.y:
                self.rect.y = self.rect.y + 2

        if self.rect.y <= 0:
            self.dy = self.dy * -1
        if (self.rect.y + self.image_h) >= self.screen.get_size()[1]:
            self.dy = self.dy * -1
        if self.rect.x <= 0:
            self.dx = self.dx * -1
        if (self.rect.x + self.image_w) > self.screen.get_size()[0]:
            self.dx = self.dx * -1

    def draw(self):
        draw_pos = self.rect
        self.screen.blit(self.image, draw_pos)


    def beenHit(self):
        '''mutalisk must explode if collided with a laser'''
        self.active = False
        #stop the mutalisk form moving and change its gif to explosion
        self.dx = 0
        self.dy = 0
        self.image = self.load_image("assets/laser_explosion.gif")
        pass

    def killTime(self):
        if self.active == False:
            self.kill()

    def uncollided(self):
        self.collidedMuta = False

def checkCollisions(mutalisks, lasers):
    ''' checks to see if there have been collisions between mutalisks'''
    #for i in range(0, 10):
        #for j in range(0, 10):
            #if(mutalisks[i].rect.colliderect(mutalisks[j].rect) and (i  != j)):
                #if(mutalisks[i].rect.collidepoint(mutalisks[j].rect.x, mutalisks[j].rect.y)):
                    #mutalisks[i].mutaliskCollision(mutalisks[j].rect.x, mutalisks[j].rect.y)


    #DOKILL = 1
    #DONTKILL = 0
    #collided = pygame.sprite.groupcollide(mutalisks, mutalisks, DONTKILL, DONTKILL)

    #for mutalisk in collided:
        #mutalisk.mutaliskCollision()
    pass

    def mutaliskCollision(self, other_x, other_y):
        '''checks to see if mutalisk collision between two mutalisks'''
        #a work in progress
            

        #if self.collidedMuta == False:
         #   if (self.rect.x < (other_x + self.image_w)) and self.dx < 0:
          #      self.rect.x = self.rect.x + ((other_x + self.image_w) - self.rect.x)
           # self.dx = self.dx * -1
            #self.dy = self.dy * -1
            #self.collidedMuta = True

        


if __name__ == "__main__":
    # Check if sound and font are supported
    if not pygame.font:
        print "Warning, fonts disabled"
    if not pygame.mixer:
        print "Warning, sound disabled"
    
    #Constants
    FPS = 50
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    BACKGROUND_COLOR = (255, 255, 255)

    #init pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('Mutalisk Demo')
    clock = pygame.time.Clock()

    mutalisks = []

    for i in range(0, 10):
        mutalisks.append(Enemy(screen, screen.get_size()[0]/2, screen.get_size()[1]/2, randint(-5, 5), randint(-5, 5), None))

    #Game loop
    while True:
        #check to make sure that collided bools in mutalisk are set to false
        for muta in mutalisks:
            muta.uncollided()
        
        time_passed = clock.tick(FPS)
                      
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        #redraw background
        screen.fill(BACKGROUND_COLOR)

        #check for collisions
        checkCollisions(mutalisks, None)

        #UPDATE AND enemies
        for muta in mutalisks:
            muta.update()
            muta.draw()

        #draw the sprite
        pygame.display.update()


    

