import pygame
import random

window_width, window_height = 1400, 900

pygame.init()
screen = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()
running = True
dt = 0
rand_adj = 120
lane_width = 20


def get_grid(h, v, width, height):
    h_gap = int(height / (h + 1))
    v_gap = int(width / (v + 1))
    h_roads = []
    v_roads = []
    for i in range(h):
        h_roads.append((i + 1) * h_gap + random.randint(-rand_adj, rand_adj))
    for i in range(v):
        v_roads.append((i + 1) * v_gap + random.randint(-rand_adj, rand_adj))

    return (h_roads, v_roads)

def gen_random_entry(grid):
    hv = random.randint(0, 1)
    road_num = random.randint(0, len(grid[hv])-1)
    hl = random.randint(0, 1)
    print(hv, road_num, hl)
    if hv == 0:
        if hl == 0:
            return [0, grid[hv][road_num] + lane_width / 2], "r"
        elif hl == 1:
            return [window_width, grid[hv][road_num] - lane_width / 2], "l"
    elif hv == 1:
        if hl == 0:
            return [grid[hv][road_num] - lane_width / 2, 0], "d"
        elif hl == 1:
            return [grid[hv][road_num] + lane_width / 2, window_height], "u"

class Car:
    def __init__(self, screen, grid):
        self.screen = screen
        self.grid = grid
        self.pos, self.direction = gen_random_entry(grid)
        self.vel = [0, 0]
        self.color = random.choice(
            ["red", "blue", "white", "yellow", "orange", "purple", "green"]
        )

    def draw(self):
        return pygame.draw.circle(
            self.screen, self.color, (self.pos[0], self.pos[1]), 10
        )

    def update_vel(self):
        if self.direction in ["r", "l"]:
            self.vel[0] = self.vel[0] + 1 if self.vel[0] < 5 else self.vel[0]
        elif self.direction in ["d", "u"]:
            self.vel[1] = self.vel[1] + 1 if self.vel[1] < 5 else self.vel[1]

    def update_pos(self):
        if self.direction == "r":
            self.pos[0] = self.pos[0] + self.vel[0]
        if self.direction == "l":
            self.pos[0] = self.pos[0] - self.vel[0]
        if self.direction == "d":
            self.pos[1] = self.pos[1] + self.vel[1]
        if self.direction == "u":
            self.pos[1] = self.pos[1] - self.vel[1]


grid = get_grid(2, 3, window_width, window_height)
print(grid)

car_group = []

def car_spawner():
    car_group.append(Car(screen, grid))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    for h in grid[0]:
        pygame.draw.line(screen, "yellow", (0, h), (window_width, h))
        pygame.draw.line(
            screen, "white", (0, h - lane_width), (window_width, h - lane_width)
        )
        pygame.draw.line(
            screen, "white", (0, h + lane_width), (window_width, h + lane_width)
        )
    for v in grid[1]:
        pygame.draw.line(screen, "yellow", (v, 0), (v, window_height))
        pygame.draw.line(
            screen, "white", (v - lane_width, 0), (v - lane_width, window_height)
        )
        pygame.draw.line(
            screen, "white", (v + lane_width, 0), (v + lane_width, window_height)
        )

    if len(car_group) < 12:
        car_spawner()

    for car in car_group:
        car.update_pos()
        car.update_vel()
        car.draw()

    pygame.display.flip()
    dt = clock.tick(60) / 1000
pygame.quit()
