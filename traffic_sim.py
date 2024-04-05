import pygame as pg
import random

from car import Car
from traffic_light import TrafficLight
import constants

# get constants
window_width = constants.window_width
window_height = constants.window_height
num_h_roads = constants.num_h_roads
num_v_roads = constants.num_v_roads
max_cars = constants.max_cars
max_speed = constants.max_speed
rand_adj = constants.rand_adj
lane_width = constants.lane_width
car_gap = constants.car_gap
light_intervel = constants.light_intervel

dt = 0
car_id = 0
running = True


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
        next_change = pg.time.get_ticks() + random.randint(1, light_intervel)
        light_group.append(
            TrafficLight(
                screen, (i[1] + lane_width, i[0] + lane_width / 2), color1, next_change
            )
        )
        light_group.append(
            TrafficLight(
                screen, (i[1] + lane_width / 2, i[0] - lane_width), color2, next_change
            )
        )
        light_group.append(
            TrafficLight(
                screen, (i[1] - lane_width / 2, i[0] + lane_width), color2, next_change
            )
        )
        light_group.append(
            TrafficLight(
                screen, (i[1] - lane_width, i[0] - lane_width / 2), color1, next_change
            )
        )
    return light_group


def car_spawner(car_id):
    car_group.add(Car(screen, light_group, grid, car_id))


pg.init()
screen = pg.display.set_mode((window_width, window_height))
clock = pg.time.Clock()
traffic_area = pg.Rect(0, 0, window_width, window_height)

grid = get_grid(num_h_roads, num_v_roads, window_width, window_height)

intersections = get_intersections(grid)
print("Intersections are: ", intersections)
light_group = get_traffic_lights(intersections)
car_group = pg.sprite.Group()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill("black")
    for h in grid[0]:
        pg.draw.line(screen, "yellow", (0, h), (window_width, h))
        pg.draw.line(
            screen, "white", (0, h - lane_width), (window_width, h - lane_width)
        )
        pg.draw.line(
            screen, "white", (0, h + lane_width), (window_width, h + lane_width)
        )
    for v in grid[1]:
        pg.draw.line(screen, "yellow", (v, 0), (v, window_height))
        pg.draw.line(
            screen, "white", (v - lane_width, 0), (v - lane_width, window_height)
        )
        pg.draw.line(
            screen, "white", (v + lane_width, 0), (v + lane_width, window_height)
        )

    if len(pg.sprite.Group.sprites(car_group)) < max_cars:
        car_spawner(car_id)
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
                    has_car_blocking = True
                    break
        # keep distance based on car vel
        car.update_vel(has_car_blocking)
        car.update_pos()
        car.draw()

    car_group.update()

    for light in light_group:
        light.update_color()
        light.draw()

    pg.display.flip()
    dt = clock.tick(60) / 1000
pg.quit()
