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
def create_wall_sprite():

    surf = pygame.Surface((TILE_SIZE, TILE_SIZE))

    surf.fill((40, 50, 75))

    pygame.draw.rect(
        surf,
        (25, 30, 45),
        (4, 4, TILE_SIZE - 8, TILE_SIZE - 8)
    )

    pygame.draw.rect(
        surf,
        (70, 85, 115),
        (0, 0, TILE_SIZE, TILE_SIZE),
        2
    )

    return surf

def create_player_sprite():

    surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)

    cx = TILE_SIZE // 2
    cy = TILE_SIZE // 2

    pygame.draw.circle(surf, (57, 255, 20), (cx, cy), 16)
    pygame.draw.circle(surf, WHITE, (cx - 5, cy - 5), 4)
    pygame.draw.circle(surf, BLACK, (cx - 5, cy + 2), 3)
    pygame.draw.circle(surf, BLACK, (cx + 5, cy + 2), 3)

    return surf

def create_enemy_sprite():

    surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)

    cx = TILE_SIZE // 2
    cy = TILE_SIZE // 2

    # Outer frame
    pygame.draw.rect(
        surf,
        (255, 0, 127),
        (4, 4, TILE_SIZE - 8, TILE_SIZE - 8),
        3,
        border_radius=5
    )

    # Core
    pygame.draw.circle(surf, (255, 0, 127), (cx, cy), 8)

    # Eye
    pygame.draw.circle(surf, WHITE, (cx, cy), 3)

    return surf

def create_exit_sprite():

    surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)

    cx = TILE_SIZE // 2
    cy = TILE_SIZE // 2

    pygame.draw.circle(surf, (255, 215, 0), (cx, cy), 18, 3)
    pygame.draw.circle(surf, (255, 255, 200), (cx, cy), 10, 2)
    pygame.draw.circle(surf, WHITE, (cx, cy), 4)

    return surf

wall_img = create_wall_sprite()
player_img = create_player_sprite()
enemy_img = create_enemy_sprite()
exit_img = create_exit_sprite()

DIRECTIONS = [
    (-1, 0),   # Up
    (1, 0),    # Down
    (0, -1),   # Left
    (0, 1)     # Right
]

running = True
game_over = False
game_win = False
game_started = False
font = pygame.font.SysFont(None, 36)
title_font = pygame.font.SysFont(None, 72)

level1 = [
"####################",
"#P        #       E#",
"# ######  #  ####  #",
"#      #  #  #     #",
"###### # ##### ### #",
"#      #         # #",
"# #### ####### # # #",
"#    #       # #   #",
"# ## ######  # ### #",
"# X          #     #",
"#        #######   #",
"####################"
]

level2 = [
"####################",
"#     #         #E #",
"# ### # ###### ### #",
"# #   #      #     #",
"# # ####### ###### #",
"# #                #",
"# ###### ####### # #",
"#            #     #",
"###### ### # # ### #",
"#P         # #    X#",
"# ########## #######",
"####################"
]

level3 = [
"####################",
"#P     #       #  E#",
"# ###### ##### # ###",
"#      # #   # #   #",
"###### # # # # ### #",
"#    # # # # #     #",
"# ## # # # # ##### #",
"# ## #     #     # #",
"# ####### # ### #  #",
"#X         #     # #",
"# ##################",
"####################"
]

levels = [level1, level2, level3]

current_level = 0

maze = levels[current_level]


player_x = 0 
player_y = 0

def get_neighbors(row, col):

    neighbors = []

    for dr, dc in DIRECTIONS:

        new_row = row + dr
        new_col = col + dc

        if (
            0 <= new_row < len(maze)
            and
            0 <= new_col < len(maze[0])
            and
            maze[new_row][new_col] != "#"
        ):

            neighbors.append((new_row, new_col))

    return neighbors

def heuristic(a, b):

    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, goal):

    open_list = [start]

    came_from = {}

    g_score = {start: 0}

    f_score = {start: heuristic(start, goal)}

    while open_list:

        current = min(open_list, key=lambda node: f_score.get(node, float("inf")))

        if current == goal:

            path = [current]

            while current in came_from:
                current = came_from[current]
                path.append(current)

            path.reverse()
            return path

        open_list.remove(current)

        for neighbor in get_neighbors(current[0], current[1]):

            tentative_g = g_score[current] + 1

            if neighbor not in g_score or tentative_g < g_score[neighbor]:

                came_from[neighbor] = current

                g_score[neighbor] = tentative_g

                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)

                if neighbor not in open_list:
                    open_list.append(neighbor)

    return []

def load_level():

    global maze
    global player_row, player_col
    global player_x, player_y
    global enemy_row, enemy_col
    global enemy_x, enemy_y
    global exit_x, exit_y

    maze = levels[current_level]

    for row in range(len(maze)):
        for col in range(len(maze[row])):

            if maze[row][col] == "P":
                player_row = row
                player_col = col
                player_x = col * TILE_SIZE
                player_y = row * TILE_SIZE

            elif maze[row][col] == "X":
                enemy_row = row
                enemy_col = col
                enemy_x = col * TILE_SIZE
                enemy_y = row * TILE_SIZE

            elif maze[row][col] == "E":
                exit_x = col * TILE_SIZE
                exit_y = row * TILE_SIZE

                
load_level()


SPEED=TILE_SIZE
ENEMY_SPEED = 1

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)
small_font = pygame.font.SysFont(None, 30)
enemy_timer = 0
enemy_delay = 500   # milliseconds

while running:

    if not game_started:

        screen.fill(BLACK)

        title = title_font.render("AI MAZE ESCAPE", True, (255,255,0))
        start = small_font.render("Press SPACE to Start", True, WHITE)

        screen.blit(title, (180,200))
        screen.blit(start, (200,300))

        pygame.display.update()

        for event in pygame.event.get():

           if event.type == pygame.QUIT:
                running = False

           elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                   game_started = True

        continue
    

    old_row = player_row
    old_col = player_col

    moved = False

    # ---------- EVENTS ----------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                player_col -= 1
                moved = True

            elif event.key == pygame.K_RIGHT:
                player_col += 1
                moved = True

            elif event.key == pygame.K_UP:
                player_row -= 1
                moved = True

            elif event.key == pygame.K_DOWN:
                player_row += 1
                moved = True

    # ---------- COLLISION WITH WALL ----------
    if maze[player_row][player_col] == "#":
        player_row = old_row
        player_col = old_col

    player_x = player_col * TILE_SIZE
    player_y = player_row * TILE_SIZE

 
        # ---------- DRAW ----------
    enemy_timer += clock.get_time()

    if enemy_timer >= enemy_delay:

        enemy_timer = 0

        enemy_row = enemy_y // TILE_SIZE
        enemy_col = enemy_x // TILE_SIZE

        path = a_star(
            (enemy_row, enemy_col),
            (player_row, player_col)
        )

        if len(path) > 1:
            enemy_row, enemy_col = path[1]
            enemy_x = enemy_col * TILE_SIZE
            enemy_y = enemy_row * TILE_SIZE
    screen.fill(BLACK)
    if game_over:
        text = font.render("GAME OVER", True, (255, 50, 50))
    
        restart = small_font.render("Press R to Restart", True, (255,255,255))
        quit_text = small_font.render("Press ESC to Quit", True, (255,255,255))

        screen.blit(text, (280, 180))
        
        screen.blit(restart, (290, 280))
        screen.blit(quit_text, (290, 320))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_r:
                    current_level = 0
                    game_over = False
                    load_level()

        continue
    
    if game_win:

        screen.fill(BLACK)

        text = font.render("CONGRATULATIONS!", True, (0,255,0))
        text2 = small_font.render("You Escaped All Mazes!", True, WHITE)
        restart = small_font.render("Press R to Play Again", True, WHITE)
        quit_text = small_font.render("Press ESC to Quit", True, WHITE)

        screen.blit(text, (270,180))
        screen.blit(text2, (210,260))
        screen.blit(restart, (280,310))
        screen.blit(quit_text, (290,350))

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_r:

                    current_level = 0
                    game_win = False
                    load_level()

        continue
    for row in range(len(maze)):
        for col in range(len(maze[row])):

            if maze[row][col] == "#":

                screen.blit(
                    wall_img,
                    (col * TILE_SIZE, row * TILE_SIZE)
                    )

    exit_rect = pygame.Rect(exit_x, exit_y, TILE_SIZE, TILE_SIZE)
    screen.blit(exit_img, (exit_x, exit_y))

    enemy = pygame.Rect(enemy_x, enemy_y, TILE_SIZE, TILE_SIZE)
    screen.blit(enemy_img, (enemy_x, enemy_y))   

    player = pygame.Rect(player_x, player_y, TILE_SIZE, TILE_SIZE)
    screen.blit(player_img, (player_x,player_y))

    if player.colliderect(enemy):
        game_over = True
      

    if player.colliderect(exit_rect):
        
        if current_level < len(levels) - 1:

            current_level += 1
            load_level()

        else:
            game_win = True
            
    level_text = font.render(f"Level: {current_level + 1}", True, (0, 255, 255))
    screen.blit(level_text, (10, 10))
    pygame.display.update()
    clock.tick(5)

pygame.quit()
sys.exit()
