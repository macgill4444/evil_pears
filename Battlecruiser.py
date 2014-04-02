import pygame, os, sys
import Laser
from Laser import Laser
from pygame.locals import *
from Stats import StatsPearGame

#note that self.x/self.y do not get updated only self.rect.x/self.rect.y
#want to add that you hold space and it increases speed of fire
#check for collisions
#hold and it acts like pressing repeatedly

COUNTERCLOCK = 1
CLOCKWISE = -1

class Battlecruiser(pygame.sprite.Sprite):
    '''A battleship class'''
    def load_image(self, image_name):
        try:
            image = pygame.image.load(image_name)
        except pygame.error, message:
            print"Cannot load image " + image_name
            raise SystemExit, message
        return image.convert_alpha()

    def __init__(self, screen, init_x, init_y, init_move_x, init_move_y, stats):

        '''makes a battleship takes x and y coords and the speed at which it moves in either direction when the correct button is pushed '''

        pygame.sprite.Sprite.__init__(self) #call sprite initializer

        self.active = True
        self.screen = screen

        self.image = self.load_image('assets/battlecruiser.gif')
#        self.image = pygame.transform.rotate(self.image, 90)
        self.image_w = self.image.get_width()
        self.image_h = self.image.get_height()

        self.rect = self.image.get_rect()
        self.rect.x = init_x
        self.rect.y = init_y

        self.x = init_x
        self.y = init_y

        self.dx = init_move_x
        self.dy = init_move_y

        #creates a group of laser sprites
        self.lasers = pygame.sprite.Group()

        #creates a stats struct to hold game info
        self.stats = stats

        #create the angle at which the ship is facing for rotating purposes
        self.angle = 180

        #this makes it so you can only shoot 6 lasers with one press
        self.laser_count = 0


    def update(self):
        '''for moving'''
        self.rect.y = self.rect.y + self.dy
        self.rect.x = self.rect.x + self.dx
        self.rect.move(self.rect.x, self.rect.y) #self.rect.y versus self.y

        if self.dy < 0:
            self.dy += .5
        if self.dy > 0:
            self.dy -= .5
        if self.dx < 0:
            self.dx += .5
        if self.dx > 0:
            self.dx -= .5

    def draw(self):
        draw_pos = self.rect
        self.screen.blit(self.image, draw_pos)

    def change_activate(self):
        if self.active == False:
            self.active = True
        if self.active == True:
            self.active == False

    def jump(self, direction):
        if direction == "UP":
            self.dy = self.dy - 8
            if self.dy < -16:
                self.dy = -12
        if direction == 'DOWN':
            self.dy = self.dy + 8
            if self.dy > 16:
                self.dy = 12
        if direction == 'RIGHT':
            self.dx = self.dx + 8
            if self.dx < -16:
                self.dx = -12
        if direction == 'LEFT':
            self.dx = self.dx - 8
            if self.dx > 16:
                self.dx = 12


    def fire(self):
        #include a group of lasers in battlecruiser class in the draw function the lasers will be drawn after the ship

        if self.angle == 180:
            self.lasers.add(Laser(self.screen, (self.rect.x + 5), (self.rect.y + self.image_h - 15), 0, 6, 0 , 0, self.angle))
            self.lasers.add(Laser(self.screen, (self.rect.x + self.image_w - 17), (self.rect.y + self.image_h - 15), 0, 6, 0 , 0, self.angle))

        if self.angle == 0:
            self.lasers.add(Laser(self.screen, (self.rect.x + 5), (self.rect.y - 15), 0, 6, 0 , 0, self.angle))
            self.lasers.add(Laser(self.screen, (self.rect.x + self.image_w - 17), (self.rect.y - 15), 0, 6, 0 , 0, self.angle))

        if self.angle == 90:
            self.lasers.add(Laser(self.screen, (self.rect.x + self.image_h - 15), (self.rect.y + 5), 6, 0, 0 , 0, self.angle))
            self.lasers.add(Laser(self.screen, (self.rect.x + self.image_h - 15), (self.rect.y + self.image_w - 20), 6, 0, 0 , 0, self.angle))

        if self.angle == 270:
            self.lasers.add(Laser(self.screen, (self.rect.x - 15), (self.rect.y + 5), 6, 0, 0 , 0, self.angle))
            self.lasers.add(Laser(self.screen, (self.rect.x - 15), (self.rect.y + self.image_w - 20), 6, 0, 0 , 0, self.angle))


        #incremenet # of lasers fired in stats
        self.stats.incre_lasersFired()

        #this is to play a sound when the laser is fired
        self.playBlast()

    def playBlast(self):
        try:
            sound = pygame.mixer.Sound("assets/laser.wav")
            sound.play()
        except pygame.error, message:
            pass

    def rotate(self, direction):
        ''' handles the rotation of the ship, rotates 90 degrees counterclockwise. resets self.angle appropriately'''

        self.image = pygame.transform.rotate(self.image, (direction * 90)) 
        if self.angle == 0:
            if direction == 1:
                self.angle = 270
            else:
                self.angle = 90
        elif self.angle == 90:
            if direction == 1:
                self.angle = 0
            else:
                self.angle = 180
        elif self.angle == 180:
            if direction == 1:
                self.angle = 90
            else:
                self.angle = 270
        elif self.angle == 270:
            if direction == 1:
                self.angle = 180
            else:
                self.angle = 0


    def beenHit(self):
        self.playCruiserBlast()
        self.active = False
        self.image = self.load_image("assets/laser_explosion.gif")
        
    def playCruiserBlast(self):
        try:
            sound = pygame.mixer.Sound("assets/death_explode.wav")
            sound.play()
        except pygame.error, message:
            pass



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

    #INIT pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('Battlecruiser demo')
    clock = pygame.time.Clock()

    #create Stats, need to do this for my pear game
    Stats = StatsPearGame(screen, 0, 0, 0, 0, 0, 0, 0)

    #create battlecrusier
    cruiser = Battlecruiser(screen, (screen.get_size()[0]/2), (screen.get_size()[1]/2), 0, 0, Stats)

    while True:
        time_passed = clock.tick(FPS)

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

        #update and draw battlecruiser & lasers
        cruiser.update()
        cruiser.draw()
        cruiser.lasers.update()
        cruiser.lasers.draw(screen)

        #draw controls text
        font = pygame.font.Font(None, 24)
        text = font.render("f - rotate counterclockwise, d - rotate  clockwise, space - fire lasers, arrow keys - move", 1, (255, 255, 255))
        screen.blit(text, ((screen.get_size()[0]/2) - 340, 580))

        #draw sprites
        pygame.display.update()

        
            
