import pygame, os, sys
from pygame.locals import *
import time


def load_image(image_name):
    ''' The proper way to load an image '''
    try:
        image = pygame.image.load(image_name)
    except pygame.error, message:
        print "Cannot load image: " + image_name
        raise SystemExit, message
    return image.convert_alpha()
    
def toMoveOn():

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_RETURN:
                return True
    return False

def playKey():
    try:
        sound = pygame.mixer.Sound('assets/typewriter_key.wav')
        sound.play()
    except pygame.error, message:
        print "Error"
        pass

def PlayIntroScreen(screen):
    nextScreen = False #start off with a intro screen
    allPrinted = False
    #this will loop until user presses enter or quits

    while nextScreen == False:
        #the text positions, to be changed as they bounce around
        instr1_x = 100
        instr1_y = 300
        instr2_x = 200
        instr2_y = 330
        instr3_x = 290
        instr3_y = 360

        #background star image
        introImage = load_image("assets/space_small.jpg")
        screen.blit(introImage, (0, 0))
        
        text1 = "WELCOME TO BATTLESHIP:THE EVIL PEARS"
        text2 = "Kill as many Evil Pears as possible"
        text3 = "Press ENTER to play"
        printText1, printText2, printText3 = "", "", ""

        font1 = pygame.font.Font(None, 36)
        font2 = pygame.font.Font(None, 30)


        #these for statements slowly print out the text like someone is typing
        #they have to continually check to see if the user has pressed enter
        if allPrinted == False:
            for char in text1:
                printText1 = printText1 + char
                instructions1 = font1.render(printText1, 1, (255, 255, 255))
                screen.blit(instructions1, (instr1_x, instr1_y))
                pygame.display.update()
                if char != " ":
                    playKey()
                    time.sleep(.05)
                nextScreen = toMoveOn()
                if nextScreen == True:
                    break
                time.sleep(.2)

            if nextScreen == False:
                for char in text2:
                    printText2 = printText2 + char
                    instructions2 = font2.render(printText2, 1, (255, 255, 255))
                    screen.blit(instructions2, (instr2_x, instr2_y))
                    pygame.display.update()
                    if char != " ":
                        playKey()
                        time.sleep(.05)
                    nextScreen = toMoveOn()
                    if nextScreen == True:
                        break
                    time.sleep(0.2)

            if nextScreen == False:
                for char in text3:
                    printText3 = printText3 + char
                    instructions3 = font2.render(printText3, 1, (255, 255, 255))
                    screen.blit(instructions3, (instr3_x, instr3_y))
                    pygame.display.update()
                    if char != " ":
                        playKey()
                        time.sleep(.05)
                    nextScreen = toMoveOn()
                    if nextScreen == True:
                        break
                    time.sleep(0.2)
            allPrinted = True
                



        instructions1 = font1.render(text1, 1, (255, 255, 255))
        screen.blit(instructions1, (instr1_x, instr1_y))        

        instructions2 = font2.render(text2, 1, (255,255,255))
        screen.blit(instructions2, (instr2_x, instr2_y))

        instructions3 = font2.render(text3, 1, (255,255,255))
        screen.blit(instructions3, (instr3_x, instr3_y))

        #print control text
        font = pygame.font.Font(None, 24)
        text = font.render("f - rotate clockwise, d - rotate counter clockwise, space - fire lasers, arrow keys - move", 1, (255, 255, 255))
        screen.blit(text, ((screen.get_size()[0]/2) - 340, 500))


        pygame.display.update()

        nextScreen = toMoveOn()
