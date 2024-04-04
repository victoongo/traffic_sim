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
light_intervel = 3000
car_id = 0
car_gap = 40


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


def get_intersections(grid):
    intersections = []
    for h in grid[0]:
        for v in grid[1]:
            intersections.append([h, v])
    return intersections


def get_traffic_lights(intersections):
    light_group = []
    for i in intersections:
        color1 = random.choice(["red", "green"])
        color2 = "red" if color1 == "green" else "green"
        next_change = pygame.time.get_ticks() + random.randint(1, light_intervel)
        light_group.append(
            TrafficLight(screen, (i[1] + 20, i[0] + 10), color1, next_change)
        )
        light_group.append(
            TrafficLight(screen, (i[1] + 10, i[0] - 20), color2, next_change)
        )
        light_group.append(
            TrafficLight(screen, (i[1] - 10, i[0] + 20), color2, next_change)
        )
        light_group.append(
            TrafficLight(screen, (i[1] - 20, i[0] - 10), color1, next_change)
        )
    return light_group


def car_spawner():
    car_group.append(Car(screen, grid, car_id))


def gen_random_entry(grid):
    hv = random.randint(0, 1)
    road_num = random.randint(0, len(grid[hv]) - 1)
    hl = random.randint(0, 1)
    # print(hv, road_num, hl)
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


class TrafficLight:
    def __init__(self, screen, pos, color, next_change):
        self.screen = screen
        self.color = color
        self.pos = pos
        self.next_change = next_change

    def draw(self):
        return pygame.draw.circle(self.screen, self.color, self.pos, 3)

    def update_color(self):
        current_time = pygame.time.get_ticks()
        if current_time > self.next_change:
            self.color = "green" if self.color == "red" else "red"
            self.next_change = current_time + light_intervel

    def get_pos(self):
        return self.pos

    def get_color(self):
        return self.color


class Car:
    def __init__(self, screen, grid, id):
        self.screen = screen
        self.grid = grid
        self.id = id
        self.pos, self.direction = gen_random_entry(grid)
        self.vel = [0, 0]
        self.color = random.choice(
            ["red", "blue", "white", "yellow", "orange", "purple", "green"]
        )

    def draw(self):
        return pygame.draw.circle(
            self.screen, self.color, (self.pos[0], self.pos[1]), 10
        )

    def get_pos(self):
        return self.pos

    def get_id(self):
        return self.id

    def get_direction(self):
        return self.direction

    def update_vel(self, has_car_blocking):
        if self.direction in ["r", "l"]:
            if has_car_blocking:
                self.vel[0] = self.vel[0] - 1 if self.vel[0] > 0 else self.vel[0]
            else:
                self.vel[0] = self.vel[0] + 1 if self.vel[0] < 5 else self.vel[0]
        elif self.direction in ["d", "u"]:
            if has_car_blocking:
                self.vel[1] = self.vel[1] - 1 if self.vel[1] > 0 else self.vel[1]
            else:
                self.vel[1] = self.vel[1] + 1 if self.vel[1] < 5 else self.vel[1]

        if self.direction == "r":
            for light in light_group:
                light_pos = light.get_pos()
                light_color = light.get_color()
                if (
                    light_pos[1] == self.pos[1]
                    and self.pos[0] <= light_pos[0] - 40
                    and self.pos[0] >= light_pos[0] - 46
                    and light_color == "red"
                ):
                    self.vel[0] = 0
        elif self.direction == "l":
            for light in light_group:
                light_pos = light.get_pos()
                light_color = light.get_color()
                if (
                    light_pos[1] == self.pos[1]
                    and self.pos[0] >= light_pos[0] + 40
                    and self.pos[0] <= light_pos[0] + 46
                    and light_color == "red"
                ):
                    self.vel[0] = 0
        elif self.direction == "d":
            for light in light_group:
                light_pos = light.get_pos()
                light_color = light.get_color()
                if (
                    light_pos[0] == self.pos[0]
                    and self.pos[1] <= light_pos[1] - 40
                    and self.pos[1] >= light_pos[1] - 46
                    and light_color == "red"
                ):
                    self.vel[1] = 0
        elif self.direction == "u":
            for light in light_group:
                light_pos = light.get_pos()
                light_color = light.get_color()
                if (
                    light_pos[0] == self.pos[0]
                    and self.pos[1] >= light_pos[1] + 40
                    and self.pos[1] <= light_pos[1] + 46
                    and light_color == "red"
                ):
                    self.vel[1] = 0

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
# print(grid)

intersections = get_intersections(grid)
print("Intersections are: ", intersections)

car_group = []
light_group = get_traffic_lights(intersections)


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
        car_id += 1

    for car in car_group:
        has_car_blocking = False
        car_pos = car.get_pos()
        car_direction = car.get_direction()
        for other_car in car_group:
            other_car_pos = other_car.get_pos()
            if (
                car.get_id() > other_car.get_id()
                and car_direction == other_car.get_direction()
            ):
                print(car_pos, other_car_pos, car_direction)
                if (
                    (
                        car_direction == "r"
                        and car_pos[1] == other_car_pos[1]
                        and car_pos[0] < other_car_pos[0]
                        and car_pos[0] > other_car_pos[0] - car_gap
                    )
                    or (
                        car_direction == "l"
                        and car_pos[1] == other_car_pos[1]
                        and car_pos[0] > other_car_pos[0]
                        and car_pos[0] < other_car_pos[0] + car_gap
                    )
                    or (
                        car_direction == "d"
                        and car_pos[0] == other_car_pos[0]
                        and car_pos[1] < other_car_pos[1]
                        and car_pos[1] > other_car_pos[1] - car_gap
                    )
                    or (
                        car_direction == "u"
                        and car_pos[0] == other_car_pos[0]
                        and car_pos[1] > other_car_pos[1]
                        and car_pos[1] < other_car_pos[1] + car_gap
                    )
                ):
                    print(2)
                    has_car_blocking = True
                    break
        # keep distance based on car vel
        car.update_vel(has_car_blocking)
        car.update_pos()
        car.draw()

    for light in light_group:
        light.update_color()
        light.draw()

    pygame.display.flip()
    dt = clock.tick(60) / 1000
pygame.quit()
