import pygame, os, sys
from pygame.locals import *
from random import randint

#question: I want to play a sound when a laser is fired, should I include that in here, if so where? in a seperate function or in init? 

class Laser(pygame.sprite.Sprite):
    ''' A laser class  '''
    def load_image(self, image_name):
        try:
            image = pygame.image.load(image_name)
        except pygame.error, message:
            print "Cannot load image: " + image_name
            raise SystemExit, message
        return image.convert_alpha() #why do I do this?

    def __init__(self, screen, init_x, init_y, init_x_speed, init_y_speed, init_x_accel, init_y_accel, angle) :
        '''makes a laser at the x,y coords, moving at given speeds, and sets the screen'''
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer

        self.active = True
        self.screen = screen

        self.angle = angle
        
        self.image = self.load_image('assets/laser.gif')
        #rotate image if the degree is 90 or 270
        if self.angle == 90 or self.angle == 270:
            self.image = pygame.transform.rotate(self.image, 90) 
        self.image_w = self.image.get_width()
        self.image_h = self.image.get_height()
        
        self.rect = self.image.get_rect()
        self.rect.x = init_x
        self.rect.y = init_y

        self.dy = init_y_speed
        self.dx = init_x_speed

        self.x_accel = init_x_accel
        self.y_accel = init_y_accel

        #boolean to show that the laser has not been hit
        self.beenHit = False


        #play a sound when its created
        #self.playBlast()

    def update(self):
        '''for moving sprite'''
        
        if self.angle == 180:
            self.rect.y += self.dy #adjust position according to veloc
            #self.rect.x += self.dx
            #self.dx += self.x_accel#adjust velocity 
            self.dy += self.y_accel
            self.rect.move(self.rect.x, self.rect.y)

        if self.angle == 0:
            self.rect.y -= self.dy #adjust position according to veloc
            #self.rect.x -= self.dx
            #self.dx += self.x_accel#adjust velocity 
            self.dy += self.y_accel
            self.rect.move(self.rect.x, self.rect.y)

        if self.angle == 90:
            #self.rect.y -= self.dy #adjust position according to veloc
            self.rect.x += self.dx
            self.dx += self.x_accel#adjust velocity 
            #self.dy += self.y_accel
            self.rect.move(self.rect.x, self.rect.y)

        if self.angle == 270:
            #self.rect.y -= self.dy #adjust position according to veloc
            self.rect.x -= self.dx
            self.dx += self.x_accel#adjust velocity 
            #self.dy += self.y_accel
            self.rect.move(self.rect.x, self.rect.y)


        #keep within bounds
        if self.rect.y <= -30:
            self.kill()
        if self.rect.y > self.screen.get_size()[1] + 30:
            self.kill()
        if self.rect.x <= -30:
            self.kill()
        if self.rect.x > self.screen.get_size()[0] + 30:
            self.kill()

    def draw(self):
        #draw_pos = self.image.get_rect()
        draw_pos = self.rect
        self.screen.blit(self.image, draw_pos)

    def setAccelerate(self, new_x_accel, new_y_accel):
        '''To change the acceleration of laser '''
        self.x_accel = new_x_accel
        self.y_accel = new_y_accel

    def changeActivate(self):
        if self.active == False:
            self.active = True
        if self.active == True:
            self.active == False

    def playBlast(self):
        try:
            sound = pygame.mixer.Sound("assets/laser.wav")
            sound.play()
        except pygame.error, message:
            pass

    def collideExplosion(self):

        self.beenHit = True
        #stop the laser form moving and change its gif to explosion
        self.dx = 0
        self.dy = 0
        self.image = self.load_image("assets/laser_explosion.gif")

        tempRect = self.image.get_rect()
        self.image_w = self.image.get_width()
        self.image_h = self.image.get_height()

        #is this working?
        tempRect = self.image.get_rect()
        tempRect.x = self.rect.x - 30 #adjust so the explosion happens in middle of laser
        tempRect.y = self.rect.y
        self.rect = tempRect
        
        
        try:
            sound = pygame.mixer.Sound("assets/death_explosion.wav")
            sound.play()
        except pygame.error, message:
            pass

    def killTime(self):
        if self.beenHit == True:
            self.kill()


if __name__ == "__main__":
    # Check if sound and font are supported
    if not pygame.font:
        print "Warning, fonts disabled"
    if not pygame.mixer:
        print "Warning, sound disabled"


    #Constants
    FPS = 50
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    BACKGROUND_COLOR = (0, 0, 0)

    #Init pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0 , 32)
    pygame.display.set_caption('Laser demo')
    clock = pygame.time.Clock()

    #create group of lasers
    lasers = pygame.sprite.Group()

    #keep track of ticks
    tick = 0

    #Game Loop
    while True:
        time_passed = clock.tick(FPS)
        tick = tick + 1

        #Add new laser periodically, takes screen, x,y, dx, dy, xaccel, yaccel every frame
        if tick % 20 == 0:
            lasers.add(Laser(screen, randint(2, screen.get_size()[0]), screen.get_size()[1], 0, -randint(1,10), 0, 0, 180))

        #Event handling here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_SPACE:
                    lasers.add(Laser(screen, randint(2, screen.get_size()[0]), screen.get_size()[1], 0, -randint(1,10), 0, 0, 180))


        #redraw background
        screen.fill(BACKGROUND_COLOR)

        #update and redraw lasers
        lasers.update()
        lasers.draw(screen)

        #draw the sprites
        pygame.display.update()


                    
                    
                

        
            
