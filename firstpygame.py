import pygame
import random
import math
from pygame import mixer
#intialize
pygame.init()

#create a screen
screen = pygame.display.set_mode((800,600))

#title and screen
pygame.display.set_caption("Zatura")


#background image
background_img =  pygame.image.load("bk2.png")

#backbround music
mixer.music.load("background.wav")
mixer.music.play(-1)

#player img
player_img =  pygame.image.load("ship1.png")
playerX = 370
playerY = 450
playerX_change = 0
playerY_change = 0

#bullet img
bullet_img = pygame.image.load("bullet1.png")
bulletX = 845
bulletY = 675
bulletX_change = 0
bulletY_change = 0
bullet_state = "ready"

#multiple enemies
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6
for i in range(num_enemies):
    #enemy image
    enemy_img.append(pygame.image.load("enemy1.png"))
    enemyX.append(random.randint(0,736))
    enemyY.append( random.randint(50,150))
    enemyX_change.append(0.5)
    enemyY_change.append(0)

def player(x,y):
    screen.blit(player_img,(x,y))
def bullet(x,y):
    screen.blit(bullet_img,(x,y))
def enemy(x,y,i):
    screen.blit(enemy_img[i],(x,y))

#fuc for fire
def fire_bullet(x,y):
    global bullet_state 
    bullet_state = "fire"
    print(bullet_state)
    screen.blit(bullet_img,(x+16,y+10))

#collision between bullet ans enemy
def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
    if distance < 27:
        return True
    else:
        return False
#game over text
over = pygame.font.Font('freesansbold.ttf',64)

def game_over():
    overtext = over.render("GAME OVER ",True,(255,255,255))
    screen.blit(overtext ,(200,250))

def show_score(x,y):
    score = font.render("Score :"+str(score_value),True,(255,255,255))
    screen.blit(score ,(x,y))

score_value = 0 
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY =10
running = True
while running:
    screen.fill((0,0,0))
    screen.blit(background_img,(0,0)) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #if keystroke is pressed to check whether is left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change += -1
            if event.key == pygame.K_RIGHT:
                playerX_change += 1
            if event.key == pygame.K_SPACE:
                
                if bullet_state=="ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX +16 
                    bulletY = playerY +10  
                    fire_bullet(bulletX,bulletY)
                    bulletY_change = 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change=0
            

    playerX += playerX_change
    
    if playerX <=0:
        playerX = 0
        
    elif playerX >= 736:
        playerX = 736
        

    if bulletX <0:
        bulletX = 0
    elif bulletX >= 736:
        bulletX = 736
    #rnrmymovement
    for i in range(num_enemies):
        #game over
        if enemyY[i] > 440:
            for j in range(num_enemies):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <=0:
            enemyX_change[i] = 0.5
            enemyY[i] += 50
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.5
            enemyY[i] += 50

        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 675
            bullet_state = "ready"
            score_value += 1
            
            enemyX[i] = random.randint(0,736)
            enemyY[i] = random.randint(50,150)
        enemy(enemyX[i] ,enemyY[i] ,i)
    #resetting the bullet
    if bulletY <= 0:
        bulletY = 675
        bullet_state = "ready"
    #bullet movement
    if bullet_state == "fire":
        bulletY -= bulletY_change
    

    bullet(bulletX,bulletY)
    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()