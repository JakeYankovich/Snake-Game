import pygame
import random
pygame.init()


size = 25
gWidth = 650
gHeight = 450

win = pygame.display.set_mode((gWidth, gHeight))

pygame.display.set_caption("Snake")


totalArea = gWidth * gHeight

xHead = 50
yHead = 50
godMode = False


gameSpeed = 55 # lower is faster

tail = [False]*totalArea
tailCount = 0
xPrev = [0]*totalArea
yPrev = [0]*totalArea

lastPressed = "r"

xFood = random.randint(1, ((gWidth  / size) -2)) * size
yFood = random.randint(1, ((gHeight / size) -2)) * size

quarterArea = int(totalArea/4)
rRainbow = [0]*quarterArea
bRainbow = [0]*quarterArea
gRainbow = [0]*quarterArea
i = 0
while i < (totalArea / 4):
    rRainbow[i] = (random.randint(0, 255))
    bRainbow[i] = (random.randint(0, 255))
    gRainbow[i] = (random.randint(0, 255))
    i += 1
rainbowCount = 0

lose = False
loseTimer = 5

scores = open("scores.txt","a")

def gameOver():
    pygame.draw.rect(win, (0, 0, 0), (25, 50, 450, 125))
        
    pygame.draw.rect(win, (255, 150, 150), (25, 50, 100, 125)) #G
    pygame.draw.rect(win, (0, 0, 0), (50, 75, 75, 25))
    pygame.draw.rect(win, (0, 0, 0), (50, 100, 50, 50))

    pygame.draw.rect(win, (255, 150, 150), (150, 50, 75, 125)) #A
    pygame.draw.rect(win, (0, 0, 0), (175, 75, 25, 25))
    pygame.draw.rect(win, (0, 0, 0), (175, 125, 25, 50))
    
    pygame.draw.rect(win, (255, 150, 150), (250, 50, 125, 125)) #M
    pygame.draw.rect(win, (0, 0, 0), (275, 75, 75, 100))
    pygame.draw.rect(win, (255, 150, 150), (300, 75, 25, 100))

    pygame.draw.rect(win, (255, 150, 150), (400, 50, 75, 125)) #E
    pygame.draw.rect(win, (0, 0, 0), (425, 75, 50, 75))
    pygame.draw.rect(win, (255, 150, 150), (425, 100, 50, 25))


run = True

while run:
    pygame.time.delay(gameSpeed)

    win.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    '''
    x = 0
    while x < (gWidth/size): #drawing grid
        pygame.draw.line(win, (100, 100, 100), ((size*x), 0), ((size*x), gHeight), 1)
        x = x + 1
    x = 0
    while x < gHeight/size:
        pygame.draw.line(win, (100, 100, 100), (0, (size*x)), (gWidth, (size*x)), 1)
        x = x + 1
    '''

    j = tailCount + 1 #setting tail coordinates
    while j >= 0:
        yPrev[j] = yPrev[j-1]
        xPrev[j] = xPrev[j-1]
        j = j - 1
        
    yPrev[0] = yHead
    xPrev[0] = xHead

    
    if lastPressed == "r":
        xHead += size
    if lastPressed == "l":
        xHead -= size
    if lastPressed == "u":
        yHead -= size
    if lastPressed == "d":
        yHead += size


    if keys[pygame.K_RIGHT] and lastPressed != "l": # can't go backwards
        #xHead += size
        lastPressed = "r"
    if keys[pygame.K_LEFT] and lastPressed != "r":
        #xHead -= size
        lastPressed = "l"
    if keys[pygame.K_UP] and lastPressed != "d":
        #yHead -= size
        lastPressed = "u"
    if keys[pygame.K_DOWN] and lastPressed != "u":
        #yHead += size
        lastPressed = "d"

    
    pygame.draw.rect(win, (255, 50, 50), (xFood, yFood, size, size)) #drawing first food

        
    if xHead < 0: #no leaving the map
        xHead = 0
    if yHead < 0:
        yHead = 0
    if yHead > (gHeight - size):
        yHead = (gHeight - size)
    if xHead > (gWidth - size):
        xHead = (gWidth - size)

    if (xHead == xFood) and (yHead == yFood): #when you get food
        xFood = random.randint(1, (gWidth  / size -2)) * size #new food spawned
        yFood = random.randint(1, (gHeight / size -2)) * size
        
        while (xFood, yFood) in list(zip(xPrev, yPrev)):
            xFood = random.randint(1, (gWidth  / size -2)) * size #IF food spawns inside snake body,
            yFood = random.randint(1, (gHeight / size -2)) * size #redo it
        tail[tailCount] = True #tail count ++
        tailCount += 1

    
    if (xHead, yHead) in list(zip(xPrev, yPrev)):
        gameOver()
        if godMode == False:
            lose = True
            
            
            
    if lose == True:
        gameOver()
        loseTimer -= 1
        if loseTimer < 0:
            scores.write(str(tailCount))
            scores.write("\n")
            scores.close()
            pygame.quit()

            
    i = 0
    while i < tailCount:
        if tail[i] == True:
            if i % 4:
                pygame.draw.rect(win, (150, 255, 150), (xPrev[i], yPrev[i], size, size))
            else:
                pygame.draw.rect(win, (rRainbow[i], bRainbow[i], gRainbow[i]), (xPrev[i], yPrev[i], size, size))
        i = i + 1
        
        
    
    pygame.draw.rect(win, (150, 255, 150), (xHead, yHead, size, size))

    
    pygame.display.update()

pygame.quit()
