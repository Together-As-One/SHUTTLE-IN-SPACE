import pygame, random, sys ,os,time
from pygame.locals import *

width = 800
height = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 60
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 8
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 30
PLAYERMOVERATE = 5
count=3
def terminate():
    pygame.quit()
    sys.exit()
def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
#quitin with escape key
                if event.key == K_ESCAPE:
                    terminate()
                return
def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((width, height),FULLSCREEN)
pygame.display.set_caption('SHUTTLE DODGES PLANETS')
pygame.mouse.set_visible(False)
font = pygame.font.SysFont(None, 30)
#Loading
gameOverSound = pygame.mixer.Sound('library/audio/crash.wav')
pygame.mixer.music.load('library/audio/music.ogg')
laugh = pygame.mixer.Sound('library/audio/laugh.wav')
playerImage = pygame.image.load('library/images/shuttle.png')
planet1 = pygame.image.load('library/images/black.png')
planet2 = pygame.image.load('library/images/pluto.png')
planet3 = pygame.image.load('library/images/satan.png')
planet4 = pygame.image.load('library/images/jupiter.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('library/images/satan.png')
sample = [planet1,planet2,planet3,planet4,baddieImage]
wallLeft = pygame.image.load('library/images/sides.png')
wallRight = pygame.image.load('library/images/sides.png')

drawText('DO YOU WANT TO PLAY SHUTTLE?', font, windowSurface, (width / 3) - 30, (height / 3))
drawText('JUST PRESS ANY KEY', font, windowSurface, (width / 3), (height / 3)+100)
pygame.display.update()
waitForPlayerToPressKey()
zero=0
if not os.path.exists("library/data/save.dat"):
    f=open("library/data/save.dat",'w')
    f.write(str(zero))
    f.close()   
v=open("library/data/save.dat",'r')
topScore = int(v.readline())
v.close()
while (count>0):
    baddies = []
    score = 0
    playerRect.topleft = (width /2, height - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)
    while True: 
        score += 1
        for event in pygame.event.get():
            
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                        terminate()        
                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize =3
            newBaddie = {'rect': pygame.Rect(random.randint(140, 485), 0 - baddieSize, 23, 47),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface':pygame.transform.scale(random.choice(sample), (60, 60)),
                        }
            baddies.append(newBaddie)
            sideLeft= {'rect': pygame.Rect(0,0,126,600),
                       'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                       'surface':pygame.transform.scale(wallLeft, (126, 599)),
                       }
            baddies.append(sideLeft)
            sideRight= {'rect': pygame.Rect(497,0,303,600),
                       'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                       'surface':pygame.transform.scale(wallRight, (303, 599)),
                       }
            baddies.append(sideRight)
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < width:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < height:
            playerRect.move_ip(0, PLAYERMOVERATE)
        
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)        
        for b in baddies[:]:
            if b['rect'].top > height:
                baddies.remove(b)
        windowSurface.fill(BACKGROUNDCOLOR)
        drawText('Score: %s' % (score), font, windowSurface, 128, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface,128, 20)
        drawText('Rest Life: %s' % (count), font, windowSurface,128, 40) 
        windowSurface.blit(playerImage, playerRect)     
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])
        pygame.display.update()
        if playerHasHitBaddie(playerRect, baddies):
            if score > topScore:
                g=open("data/save.dat",'w')
                g.write(str(score))
                g.close()
                topScore = score
            break
        mainClock.tick(FPS)
    pygame.mixer.music.stop()
    count=count-1
    gameOverSound.play()
    time.sleep(1)
    if (count==0):
     laugh.play()
     drawText('LIFE TIME OUT!', font, windowSurface, (width / 3), (height / 3))
     drawText('PRESS KEY TO PLAY AGAIN.', font, windowSurface, (width / 3) - 80, (height / 3) + 100)
     pygame.display.update()
     time.sleep(2)
     waitForPlayerToPressKey()
     count=3
     gameOverSound.stop()
