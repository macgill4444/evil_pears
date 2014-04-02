import pygame, os, sys
from pygame.locals import *
from random import randint
from Stats import StatsPearGame


class EvilPear(pygame.sprite.Sprite):
    '''a pear'''
    def load_image(self, image_name):
        try:
            image = pygame.image.load(image_name)
            image = image.convert_alpha()
        except pygame.error, message:
            print "Cannot load image " + image_name
            raise SystemExit, message
        return image

    def add_Stats(self, stats):
        '''for adding a stats class that holds statistics of the game'''
        self.stats = stats
        
    def __init__(self, screen, init_x, init_y, init_dx, init_dy, stats):
        '''makes a pear takes the x,y coords and the initial speed'''

        pygame.sprite.Sprite.__init__(self)

        self.screen = screen

        self.image = self.load_image('assets/pear2.png')
        self.image_w = self.image.get_width()
        self.image_h = self.image.get_height()

        self.rect = self.image.get_rect()
        self.rect.x = init_x
        self.rect.y = init_y

        self.x = init_x
        self.y = init_y

        self.dx = init_dx
        self.dy = init_dy

        #this is the number of laser hits that pear has received, starts at 0
        self.num_hits = 0
        self.passedZero = False
        self.checkPassed = False

        #this is the game stats
        self.stats = stats

    def update(self):
        '''for moving'''
        self.rect.y += self.dy #adjust position according to veloc
        self.rect.x += self.dx
        self.rect.move(self.rect.x, self.rect.y)

        if self.rect.y < 0:
            if self.passedZero == False:
                self.stats.incre_pearsPassed()
            self.passedZero = True
        if self.rect.y < -60:
            self.kill()
        if self.rect.y > (self.screen.get_size()[1] + 10):
            self.kill()

    def draw(self):
        draw_pos = self.rect
        self.screen.blit(self.image, draw_pos)

    def beenHit(self):
        self.num_hits = self.num_hits + 1

        #need to change the rect for the new pics

        if self.num_hits == 1:
            self.image = self.load_image("assets/pear3.png")
            
        if self.num_hits == 2:
            self.image = self.load_image("assets/pear4.png")
            
        if self.num_hits == 3:
            self.image = self.load_image("assets/pear5.png")
            
        if self.num_hits == 4:
            self.stats.incre_pearsKilled()
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

    #init pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('Pear demo')
    clock = pygame.time.Clock()

    #create group of pears
    pears = pygame.sprite.Group()

    #create stat
    Stats = StatsPearGame(screen, 0, 0, 0, 0, 0, 0, 0) 

    tick = 0

    #Game loop
    while True:
        time_passed = clock.tick(FPS)
        tick = tick + 1

        if tick % 20 == 0:
            pears.add(EvilPear(screen, randint(2, screen.get_size()[0]), screen.get_size()[1], 0, -1, Stats)) #with speed at -.2 the pears never went below 0

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

        #UPDATE AND draw pears
        pears.update()
        pears.draw(screen)

        #draw the sprite
        pygame.display.update()
        
