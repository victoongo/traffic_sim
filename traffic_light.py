import pygame as pg
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


class TrafficLight:
    def __init__(self, screen, pos, color, next_change):
        self.screen = screen
        self.color = color
        self.pos = pos
        self.next_change = next_change

    def draw(self):
        return pg.draw.circle(self.screen, self.color, self.pos, 3)

    def update_color(self):
        current_time = pg.time.get_ticks()
        if current_time > self.next_change:
            self.color = "green" if self.color == "red" else "red"
            self.next_change = current_time + light_intervel

    def get_pos(self):
        return self.pos

    def get_color(self):
        return self.color
