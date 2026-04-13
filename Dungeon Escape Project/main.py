import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
CELL = WIDTH // COLS

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon Escape RL")

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)
PURPLE = (160,32,240)
GRAY = (150,150,150)

font = pygame.font.SysFont(None, 32)
big_font = pygame.font.SysFont(None, 50)

game_state = "menu"
group_reward = 0
timer = 0
TIME_LIMIT = 400
dragon_escape = False
win_message = ""

door = [19,10]
portal = [0,19]

obstacles = [
    [6,6],[6,8],[6,10],
    [10,6],[10,8],[10,10],
    [14,6],[14,8],[14,10]
]

Q = {}
actions = ["UP","DOWN","LEFT","RIGHT","STAY"]

def get_state(agent):
    return (agent.pos[0], agent.pos[1], agent.has_key)

def choose_action(state, epsilon=0.1):
    if random.random() < epsilon:
        return random.choice(actions)
    return max(actions, key=lambda a: Q.get((state,a),0))

def update_q(state, action, reward, next_state):
    alpha = 0.2
    gamma = 0.9
    old = Q.get((state,action),0)
    future = max([Q.get((next_state,a),0) for a in actions])
    Q[(state,action)] = old + alpha*(reward + gamma*future - old)

# ---------- AGENT ----------
class Agent:
    def __init__(self, x, y):
        self.pos = [x,y]
        self.has_key = False
        self.alive = True

    def step(self, action):
        old = self.pos.copy()

        if action == "UP": self.pos[1] -= 1
        if action == "DOWN": self.pos[1] += 1
        if action == "LEFT": self.pos[0] -= 1
        if action == "RIGHT": self.pos[0] += 1

        self.pos[0] = max(0,min(COLS-1,self.pos[0]))
        self.pos[1] = max(0,min(ROWS-1,self.pos[1]))

        if self.pos in obstacles:
            self.pos = old

    def move_towards(self, target):
        old = self.pos.copy()

        if self.pos[0] < target[0]: self.pos[0] += 1
        elif self.pos[0] > target[0]: self.pos[0] -= 1
        elif self.pos[1] < target[1]: self.pos[1] += 1
        elif self.pos[1] > target[1]: self.pos[1] -= 1

        if self.pos in obstacles:
            self.pos = old

    def draw(self):
        if self.alive:
            pygame.draw.rect(screen, BLUE, (self.pos[0]*CELL,self.pos[1]*CELL,CELL,CELL))

# ---------- DRAGON ----------
class Dragon:
    def __init__(self):
        self.pos = [10,5]
        self.alive = True
        self.path = [(10,5),(12,5),(12,7),(10,7)]
        self.index = 0

    def move(self):
        if not self.alive:
            return

        # semi-random movement
        moves = [(1,0),(-1,0),(0,1),(0,-1)]
        random.shuffle(moves)

        for dx,dy in moves:
            nx = self.pos[0] + dx
            ny = self.pos[1] + dy

            if 0 <= nx < COLS and 0 <= ny < ROWS:
                if [nx,ny] not in obstacles:
                    self.pos = [nx,ny]
                    break

    def escape_to_portal(self):
        if self.pos == portal:
            return True

        # strong directed escape
        if self.pos[0] < portal[0]: self.pos[0]+=1
        elif self.pos[0] > portal[0]: self.pos[0]-=1

        if self.pos[1] < portal[1]: self.pos[1]+=1
        elif self.pos[1] > portal[1]: self.pos[1]-=1

        return False

    def draw(self):
        if self.alive:
            pygame.draw.rect(screen, RED, (self.pos[0]*CELL,self.pos[1]*CELL,CELL,CELL))

# ---------- KEY ----------
class Key:
    def __init__(self):
        self.pos = [10,5]
        self.visible = False

    def draw(self):
        if self.visible:
            pygame.draw.rect(screen, YELLOW, (self.pos[0]*CELL,self.pos[1]*CELL,CELL,CELL))

# ---------- RESET ----------
def reset():
    global agents, dragon, key, timer, group_reward, dragon_escape, win_message, game_state

    agents = [Agent(0,5),Agent(0,10),Agent(0,15)]
    dragon = Dragon()
    key = Key()

    timer = 0
    group_reward = 0
    dragon_escape = False
    win_message = ""
    game_state = "menu"

reset()

# ---------- BUTTON ----------
def button(text, x, y):
    rect = pygame.Rect(x,y,220,70)
    pygame.draw.rect(screen, GRAY, rect, border_radius=12)
    t = font.render(text, True, BLACK)
    screen.blit(t, (x+60,y+20))

    if rect.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0]:
            pygame.time.delay(200)
            return True
    return False

clock = pygame.time.Clock()

# ---------- LOOP ----------
while True:
    screen.fill(BLACK)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_state == "menu":
        if button("START", 190,250):
            game_state = "play"

    elif game_state == "play":

        timer += 1
        screen.blit(font.render(f"Reward: {group_reward}", True, WHITE),(10,10))

        pygame.draw.rect(screen, GREEN, (door[0]*CELL,door[1]*CELL,CELL,CELL))
        pygame.draw.rect(screen, PURPLE, (portal[0]*CELL,portal[1]*CELL,CELL,CELL))

        for obs in obstacles:
            pygame.draw.rect(screen, WHITE, (obs[0]*CELL,obs[1]*CELL,CELL,CELL))

        if not dragon_escape:
            dragon.move()
        else:
            if dragon.escape_to_portal():
                reset()
                continue

        if timer > TIME_LIMIT and dragon.alive:
            dragon_escape = True

        dragon.draw()
        key.draw()

        # sacrifice
        if dragon.alive and not dragon_escape:
            for a in agents:
                if a.alive and abs(a.pos[0]-dragon.pos[0])<=1 and abs(a.pos[1]-dragon.pos[1])<=1:
                    a.alive = False
                    dragon.alive = False
                    key.visible = True
                    break

        for agent in agents:
            if not agent.alive:
                continue

            # 🔥 FIXED STEP MOVEMENT
            if agent.has_key:
                agent.move_towards(door)

            elif key.visible:
                agent.move_towards(key.pos)

            else:
                state = get_state(agent)
                action = choose_action(state)
                agent.step(action)
                next_state = get_state(agent)
                update_q(state, action, -0.01, next_state)

            if key.visible and agent.pos == key.pos:
                agent.has_key = True
                key.visible = False

            if agent.has_key and agent.pos == door:
                group_reward = 1
                win_message = "AGENT WINS!"
                game_state = "over"

            agent.draw()

    elif game_state == "over":
        screen.blit(font.render(f"Reward: {group_reward}", True, WHITE),(10,10))
        screen.blit(big_font.render(win_message, True, GREEN),(150,200))

        if button("RESTART", 190,300):
            reset()

    pygame.display.update()
    clock.tick(15)