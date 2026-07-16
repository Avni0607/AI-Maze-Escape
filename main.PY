import pygame
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Maze Escape")

BLACK = (0, 0, 0)
WHITE =(255,255,255)
TILE_SIZE=40

running = True

maze = [
    "####################",
    "#  P    #        E##",
    "# ###  #  ######   #",
    "# #       #        #",
    "# ######  #######  #",
    "#      X           #",
    "####################"
]

player_x = 0
player_y = 0

for row in range(len(maze)):
    for col in range(len(maze[row])):
        if maze[row][col] == "P":
            player_x = col * TILE_SIZE
            player_y = row * TILE_SIZE

exit_x = 0
exit_y = 0

for row in range(len(maze)):
    for col in range(len(maze[row])):
        if maze[row][col] == "E":
            exit_x = col * TILE_SIZE
            exit_y = row * TILE_SIZE

enemy_x = 0
enemy_y = 0

for row in range(len(maze)):
    for col in range(len(maze[row])):
        if maze[row][col] == "X":
            enemy_x = col * TILE_SIZE
            enemy_y = row * TILE_SIZE            
SPEED=1
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    old_x = player_x
    old_y = player_y
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x-=SPEED

    if keys[pygame.K_RIGHT]:
        player_x+=SPEED

    if keys[pygame.K_UP]:
        player_y-=SPEED

    if keys[pygame.K_DOWN]:
        player_y+=SPEED
        
    if player_x<0:
        player_x=0

    if player_y<0:
        player_y=0

    if player_x > WIDTH - TILE_SIZE:
        player_x = WIDTH - TILE_SIZE

    if player_y > HEIGHT - TILE_SIZE:
        player_y = HEIGHT - TILE_SIZE
    screen.fill(BLACK)

    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == "#":
                wall = pygame.Rect(
                col * TILE_SIZE,
                row * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )
                pygame.draw.rect(screen, WHITE, wall)

    exit_rect = pygame.Rect(exit_x, exit_y, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, (255, 0, 0), exit_rect)
    enemy = pygame.Rect(enemy_x, enemy_y, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, (0, 0, 255), enemy)
    player=pygame.Rect(player_x,player_y,TILE_SIZE,TILE_SIZE)
    if player.colliderect(exit_rect):
        print("You Win!")
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == "#":

                wall = pygame.Rect(
                col * TILE_SIZE,
                row * TILE_SIZE, 
                TILE_SIZE,
                TILE_SIZE
            )

            if player.colliderect(wall):
                player_x = old_x
                player_y = old_y
                player = pygame.Rect(player_x, player_y, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen,(0,255,0),player)


    pygame.display.update()

pygame.quit()
sys.exit()
