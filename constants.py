window_width = 1600
window_height = 900
num_h_roads = 4
num_v_roads = 6
rand_adj = int((window_width / num_v_roads) / 4)
lane_width = 12

light_intervel = 5000

max_cars = 100
max_speed = 4
car_size = lane_width / 2
car_gap = car_size * 2 * 3
stop_distance_near = lane_width * 2 + car_size / 2
stop_distance_far = lane_width * 2 + car_size / 2 + max_speed - 1
