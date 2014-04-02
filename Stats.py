import pygame, os, sys
from pygame.locals import *

#define a stats class that holds the game statistics
class StatsPearGame():
    '''a stats class to hold game statistics and the health bar of the batteleshp'''
    def __init__(self, screen, pearsPassed, pearsKilled, lasersFired, healthBar, totalPears, x_coord, y_coord):

        self.screen = screen
        self.pearsPassed = pearsPassed
        self.pearsKilled = pearsKilled
        self.lasersFired = lasersFired
        self.healthBar = healthBar
        self.totalPears = totalPears

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)

        self.x_coord = x_coord
        self.y_coord = y_coord
        self.rect_h = 40
        self.rect1_w = 215

        #coords of outer rectangel for healthbar [x, y, w, h]  
        self.rect1_coords = [self.x_coord, self.y_coord, self.rect1_w + 2, self.rect_h + 2]
        #coords of inner rectangle for healthbar
        self.rect2_w = 215 #this decreases as health bar decreases
        self.rect2_coords = [self.x_coord + 2, self.y_coord + 2, self.rect2_w, self.rect_h]
        #boolean to keep track of whether game is still going
        self.stillGame = True

        self.total_collisions = 0

    def incre_pearsPassed(self):
        self.pearsPassed = self.pearsPassed + 1
        #decrement health bar for each pear that has passed
        self.decre_healthBar()
        
    def incre_pearsKilled(self):
        self.pearsKilled = self.pearsKilled + 1
        #increment health bar for each pear killed
        self.incre_healthBar()
        
    def incre_lasersFired(self):
        self.lasersFired = self.lasersFired + 2 #lasers fired in pairs
        
    def incre_healthBar(self):
        #self.healthBar = self.healthBar + 1
        #increment rect2w if it is less than the total width of health bar
        if self.rect2_w < self.rect1_w:
            self.rect2_w = self.rect2_w + 5

    def decre_healthBar(self):
        #self.healthBar = self.healthBar - 1
        self.rect2_w = self.rect2_w - 5 #43
        if self.rect2_w < 0:
            self.rect2_w = 0

    def incre_totalPears(self):
        self.totalPears =  self.totalPears + 1

    def draw_healthBar(self):
        pygame.draw.rect(self.screen, self.WHITE, self.rect1_coords , 2)
        if(self.rect2_w < 30):
            pygame.draw.rect(self.screen, self.RED, self.rect2_coords)
        else:
            pygame.draw.rect(self.screen, self.GREEN, self.rect2_coords)


        healthPercent = int((float(self.rect2_w) / float(self.rect1_w)) * 100)
        font = pygame.font.Font(None, 20)
        text = "Health Bar " + str(healthPercent) + "%"
        printText = font.render(text, 1, self.WHITE)
        self.screen.blit(printText, (self.x_coord + 60, self.y_coord + 50))
            
            

    def update_healthBar(self):
        #coords of outer rectangel for healthbar [x, y, w, h] need offset of +2
        self.rect1_coords = [self.x_coord, self.y_coord, self.rect1_w + 2, self.rect_h + 2]
        #coords of inner rectangle for healthbar
        self.rect2_coords = [self.x_coord + 2, self.y_coord + 2, self.rect2_w, self.rect_h]
        #check health bar to see if game still going
        if (self.rect2_w <= 0):
            self.stillGame = False


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

    Stats = StatsPearGame(screen, 0, 0, 0, 0, 0, 75, 10)

    while Stats.stillGame:
        time_passed = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                       pygame.quit()
                       sys.exit()
                    if event.key == K_RETURN:
                        Stats.incre_healthBar()
                    if event.key == K_SPACE:
                        Stats.decre_healthBar()

        #redraw background
        screen.fill(BACKGROUND_COLOR)

        #update stats rectangle
        Stats.update_healthBar()
        Stats.draw_healthBar()
 
        #draw sprites
        pygame.display.update()


