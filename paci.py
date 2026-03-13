import pygame
import random
import math
import numpy  as np
from Agent import Agent
import matplotlib.pyplot as plt

# Initialize pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
CELL_SIZE = 40

# Define colors
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Labyrinth as a string
labyrinth = [
    "##########",
    "#........#",
    "#.##..##.#",
    "#........#",
    "##########"
]

# Get labyrinth dimensions
ROWS = len(labyrinth)
COLS = len(labyrinth[0])

# Initialize game screen
screen = pygame.display.set_mode((COLS * CELL_SIZE, ROWS * CELL_SIZE))
pygame.display.set_caption("Micro-Pacman")

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def scale_direction(x1, y1, x2, y2):
    direc = 0
    vec1 = np.array([x1, y1])
    vec2 = np.array([x2, y2])
    t = vec2 - vec1  # Richtungsvektor

    if abs(t[0]) > abs(t[1]):
        if t[0] < 0:
            direc = 1  # left
        else:
            direc = 2  # right
    else:
        if t[1] < 0:
            direc = 3  # up
        else:
            direc = 4  # down

    return direc

def scale_distance(distance):
    if distance >=4:
        return 2
    elif distance >=2:
        return 1
    else: return 0


def get_state(paci, ghost, laby,max_values):
    # --- Geist-Infos ---
    dist = manhattan_distance(paci.x, paci.y, ghost.x, ghost.y)
    distance_scaled = scale_distance(dist)
    ghost_direction = scale_direction(paci.x, paci.y, ghost.x, ghost.y)
    
    #scaled_cookie_distance =0
    cookie_positions = []
    for y in range(len(laby)):
        for x in range(len(laby[y])):
            if laby[y][x] == ".":
                cookie_positions.append((x, y))

    if not cookie_positions:
        cookie_direction = 0 


    else:
        nearest_cookie = min(cookie_positions, key=lambda c: abs(paci.x - c[0]) + abs(paci.y - c[1]))
        cookie_direction = scale_direction(paci.x, paci.y, nearest_cookie[0], nearest_cookie[1])
        #scaled_cookie_distance  = scale_distance(manhattan_distance(paci.x,paci.y,nearest_cookie[0],nearest_cookie[1]))
    
    # --- Zustandsvektor ---
    x= [ghost_direction, cookie_direction,distance_scaled,paci.x,paci.y]
    
    s = x[0] 
    for i in range(1, len(x)): 
        s = s * max_values[i] + x[i] 
    
    return s
    
def get_reward(laby, paci , ghost):  
    reward = -0.1
    won = True
    if paci.x == ghost.x and paci.y == ghost.y:
        reward -= 1
    for i in  range(len(laby)):
        if "."  in laby[i]:
            won= False
    if won == True:
        reward += 1
    
    if laby[paci.y][paci.x] == ".":
        reward +=0.25
    
    return reward


# Pacman class
class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.count = 0

    def move(self, dx, dy):
        new_x, new_y = self.x + dx, self.y + dy
        if labyrinth[new_y][new_x] != "#":
            self.x = new_x
            self.y = new_y

    def draw(self):
        radius = CELL_SIZE // 2 - 4
        start_angle = math.pi / 6
        end_angle = -math.pi / 6
        pygame.draw.circle(screen, YELLOW, (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 4)
            # Calculate the points for the mouth
        start_pos = (self.x* CELL_SIZE + CELL_SIZE // 2 + int(radius*1.3 * math.cos(start_angle)),
                     self.y* CELL_SIZE + CELL_SIZE // 2 - int(radius*1.3 * math.sin(start_angle)))
        end_pos = (self.x* CELL_SIZE + CELL_SIZE // 2 + int(radius*1.3 * math.cos(end_angle)),
                   self.y* CELL_SIZE + CELL_SIZE // 2 - int(radius*1.3 * math.sin(end_angle)))
        self.count += 1
        if self.count%2==0:
            # Draw the mouth by filling a polygon
            pygame.draw.polygon(screen, BLACK, [(self.x* CELL_SIZE + CELL_SIZE // 2, self.y* CELL_SIZE + CELL_SIZE // 2), start_pos, end_pos])
# Ghost class with pixel art
class Ghost:
    # Define the pixel art for the ghost using strings
    ghost_pixels = [
        " #### ",
        "######",
        "## # #",
        "######",
        "######",
        "# # # "
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_towards_pacman(self, pacman):
        if self.x < pacman.x and labyrinth[self.y][self.x + 1] != "#":
            self.x += 1
        elif self.x > pacman.x and labyrinth[self.y][self.x - 1] != "#":
            self.x -= 1
        elif self.y < pacman.y and labyrinth[self.y + 1][self.x] != "#":
            self.y += 1
        elif self.y > pacman.y and labyrinth[self.y - 1][self.x] != "#":
            self.y -= 1

    def draw(self):
        pixel_size = CELL_SIZE // len(self.ghost_pixels)  # Size of each pixel in the ghost art
        for row_idx, row in enumerate(self.ghost_pixels):
            for col_idx, pixel in enumerate(row):
                if pixel == "#":
                    pixel_x = self.x * CELL_SIZE + col_idx * pixel_size
                    pixel_y = self.y * CELL_SIZE + row_idx * pixel_size
                    pygame.draw.rect(screen, RED, (pixel_x, pixel_y, pixel_size, pixel_size))
# Draw walls and cookies
def draw_labyrinth():
    for y, row in enumerate(labyrinth):
        for x, cell in enumerate(row):
            if cell == "#":
                pygame.draw.rect(screen, BLUE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif cell == ".":
                pygame.draw.circle(screen, WHITE, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), 5)
# Main game function


def main():
    global labyrinth
    clock = pygame.time.Clock()
    bot = Agent(1800, learning=0.25,epsilon=0.45)  # Agent instanziieren
    game =0
    win_counter = 0
    win_count = []
    episode = []
    states = set()
    

    
    
    while True:  # Episoden-Schleife
        # Labyrinth zurücksetzen
        screen.fill(BLACK)
        labyrinth = [
            "##########",
            "#........#",
            "#.##..##.#",
            "#........#",
            "##########"
        ]

        # Pacman und Ghost initialisieren
        y,x = random.randint(1,3), random.randint(1,8)
        while labyrinth[y][x] =="#":
            y,x = random.randint(1,3), random.randint(1,8)

        pacman = Pacman(x,y)
        ghost = Ghost(COLS - 2, ROWS - 2)

        running = True
        iter = 0
        
        # Anfangszustand
        state = get_state(pacman, ghost, labyrinth, max_values = [4,4,2,8,3])
    
        bot.cool_down()
    
        while running:  # Spiel-Schleife
            screen.fill(BLACK)
            iter += 1
            
            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return

            # Agent wählt Aktion
            action = bot.choose_action_greedy(state)

            # Pacman Bewegung
            if action == "LEFT":
                pacman.move(-1, 0)
            if action == "RIGHT":
                pacman.move(1, 0)
            if action == "UP":
                pacman.move(0, -1)
            if action == "DOWN":
                pacman.move(0, 1)

            # Ghost Bewegung
            if iter % 3 == 0:
                ghost.move_towards_pacman(pacman)

            # Reward und Update
            reward = get_reward(labyrinth, pacman, ghost)
            future_state = get_state(pacman, ghost, labyrinth, max_values = [4,4,2,8,3])
            bot.TD_update(action, state, reward, future_state)
            state = future_state
            if state not in states:
                states.add(state)
           
            

            # Check Kollision / Sieg
            if pacman.x == ghost.x and pacman.y == ghost.y:
                #print("Game Over! The ghost caught Pacman."
                running = False
            if all("." not in row for row in labyrinth):   
                    win_counter += 1 
                    #print("You Win! Pacman ate all the cookies.")
                    running = False
                    
            
            
            # Eat cookies
            if labyrinth[pacman.y][pacman.x] == ".":  # y = Zeile, x = Spalte
                row = labyrinth[pacman.y]              # aktuelle Zeile
                labyrinth[pacman.y] = row[:pacman.x] + " " + row[pacman.x + 1:]

        
            if game > 6000 or game <15 :
                draw_labyrinth()
                pacman.draw()
                ghost.draw()
                pygame.display.flip()
                clock.tick(20) # langsam genug, um das Spiel zu sehen'''
    

        # Nach Episode fertig:
        if game >= 6020:
            plt.plot( episode,win_count, "red")
            plt.show()
            
            break  

        
        game += 1
        # episode.append(game)
        win_count.append(win_counter)
        print(game)
        episode.append(game)
    
        
 
    # pygame erst am Ende komplett schließen:
    pygame.quit()


if __name__ == "__main__":
    main()
