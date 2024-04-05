import pygame as pg
import random
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
car_size = constants.car_size
stop_distance_near = constants.stop_distance_near
stop_distance_far = constants.stop_distance_far


def gen_random_entry(grid):
    hv = random.randint(0, 1)
    road_num = random.randint(0, len(grid[hv]) - 1)
    hl = random.randint(0, 1)
    if hv == 0:
        if hl == 0:
            return [1, grid[hv][road_num] + lane_width / 2], "r"
        elif hl == 1:
            return [window_width - 1, grid[hv][road_num] - lane_width / 2], "l"
    elif hv == 1:
        if hl == 0:
            return [grid[hv][road_num] - lane_width / 2, 1], "d"
        elif hl == 1:
            return [grid[hv][road_num] + lane_width / 2, window_height - 1], "u"


class Car(pg.sprite.Sprite):
    def __init__(self, screen, light_group, grid, id):
        super().__init__()
        self.screen = screen
        self.light_group = light_group
        self.grid = grid
        self.id = id
        self.pos, self.direction = gen_random_entry(grid)
        self.vel = [0, 0]
        self.color = random.choice(
            ["red", "blue", "white", "yellow", "orange", "purple", "green"]
        )

    def draw(self):
        return pg.draw.circle(
            self.screen, self.color, (self.pos[0], self.pos[1]), car_size
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
                self.vel[0] = (
                    self.vel[0] + 1 if self.vel[0] < max_speed else self.vel[0]
                )
        elif self.direction in ["d", "u"]:
            if has_car_blocking:
                self.vel[1] = self.vel[1] - 1 if self.vel[1] > 0 else self.vel[1]
            else:
                self.vel[1] = (
                    self.vel[1] + 1 if self.vel[1] < max_speed else self.vel[1]
                )

        if self.direction == "r":
            for light in self.light_group:
                light_pos = light.get_pos()
                light_color = light.get_color()
                if (
                    light_pos[1] == self.pos[1]
                    and self.pos[0] <= light_pos[0] - stop_distance_near
                    and self.pos[0] >= light_pos[0] - stop_distance_far
                    and light_color == "red"
                ):
                    self.vel[0] = 0
        elif self.direction == "l":
            for light in self.light_group:
                light_pos = light.get_pos()
                light_color = light.get_color()
                if (
                    light_pos[1] == self.pos[1]
                    and self.pos[0] >= light_pos[0] + stop_distance_near
                    and self.pos[0] <= light_pos[0] + stop_distance_far
                    and light_color == "red"
                ):
                    self.vel[0] = 0
        elif self.direction == "d":
            for light in self.light_group:
                light_pos = light.get_pos()
                light_color = light.get_color()
                if (
                    light_pos[0] == self.pos[0]
                    and self.pos[1] <= light_pos[1] - stop_distance_near
                    and self.pos[1] >= light_pos[1] - stop_distance_far
                    and light_color == "red"
                ):
                    self.vel[1] = 0
        elif self.direction == "u":
            for light in self.light_group:
                light_pos = light.get_pos()
                light_color = light.get_color()
                if (
                    light_pos[0] == self.pos[0]
                    and self.pos[1] >= light_pos[1] + stop_distance_near
                    and self.pos[1] <= light_pos[1] + stop_distance_far
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

    def update(self):
        if not (0 <= self.pos[0] <= window_width and 0 <= self.pos[1] <= window_height):
            self.kill()
