import pygame
import random
import math
from pygame import mixer


# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load(r"C:\Users\gawai\OneDrive\Desktop\VSC Files\SpaceInvader\background01.png")

# Background Sound
mixer.music.load(r"C:\Users\gawai\OneDrive\Desktop\VSC Files\SpaceInvader\star-wars-theme-song.wav")
mixer.music.play(-1)


# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load(r"C:\Users\gawai\OneDrive\Desktop\VSC Files\SpaceInvader\ufo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load(r"C:\Users\gawai\OneDrive\Desktop\VSC Files\SpaceInvader\battleship.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load(r"C:\Users\gawai\OneDrive\Desktop\VSC Files\SpaceInvader\people.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load(r"C:\Users\gawai\OneDrive\Desktop\VSC Files\SpaceInvader\bullet.png")
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = "ready"

# Score 

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over Text

over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x,y):
    score = font.render("Score :" + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200, 250))


# Functions
def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow( enemyX-bulletY, 2 )) + (math.pow( enemyY-bulletY, 2 )))
    if distance < 27:
        return True
    return False


# Game Loop
running = True
while running:
    screen.fill((128,128,128))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keystroke events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound(r"C:\Users\gawai\OneDrive\Desktop\VSC Files\SpaceInvader\laser.wav")
                    bullet_Sound.play()
                    # Get the current x cordinate of the spaceship 
                    bulletX = playerX  # Set bulletX to current playerX
                    fire_bullet(bulletX, bulletY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Player movement
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break


        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound(r"C:\Users\gawai\OneDrive\Desktop\VSC Files\SpaceInvader\explosion.wav")
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print("Score:", score_value)  # Print updated score
            enemyX[i] = random.randint(0, 736)  # Reset enemy position
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    # Reset bullet when it goes off-screen

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    
    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()
