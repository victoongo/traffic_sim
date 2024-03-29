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
    print(h_gap, v_gap)
    h_roads = []
    v_roads = []
    for i in range(h):
        h_roads.append((i + 1) * h_gap + random.randint(-rand_adj, rand_adj))
    for i in range(v):
        v_roads.append((i + 1) * v_gap + random.randint(-rand_adj, rand_adj))

    return (h_roads, v_roads)


class Car:
    def __init__(self, screen, grid):
        self.pos = (random.randint(0, window_width), random.randint(0, window_height))
        self.screen = screen
        self.grid = grid
        self.vel = random.randint(1, 3)
        self.color = random.choice(
            ["red", "blue", "white", "yellow", "orange", "purple", "green"]
        )

    def draw(self):
        return pygame.draw.rect(
            self.screen, self.color, (self.pos[0], self.pos[1], 20, 10)
        )

    def update_vel(self):
        self.vel = self.vel + 0

    def update_pos(self):
        self.pos = (self.pos[0] + self.vel, self.pos[1] + self.vel)


grid = get_grid(2, 3, window_width, window_height)

car_group = []


def car_spawner():
    car_group.append(Car(screen, grid))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    for v in grid[0]:
        pygame.draw.line(screen, "yellow", (v, 0), (v, window_height))
        pygame.draw.line(
            screen, "white", (v - lane_width, 0), (v - lane_width, window_height)
        )
        pygame.draw.line(
            screen, "white", (v + lane_width, 0), (v + lane_width, window_height)
        )
    for h in grid[1]:
        pygame.draw.line(screen, "yellow", (0, h), (window_width, h))
        pygame.draw.line(
            screen, "white", (0, h - lane_width), (window_width, h - lane_width)
        )
        pygame.draw.line(
            screen, "white", (0, h + lane_width), (window_width, h + lane_width)
        )

    if len(car_group) < 12:
        car_spawner()

    for car in car_group:
        car.update_pos()
        car.draw()

    pygame.display.flip()
    dt = clock.tick(60) / 1000
pygame.quit()
