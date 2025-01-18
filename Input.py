import math

from Pendulum_Demo import pygame
from constants import *

class Mouse:
    def __init__(self):
        self.check_buttons()
        self.collision_item = None
        self.prev_mouse_pos = self.get_position()
        self.curr_mouse_pos = [0, 0]
        self.velocity = [0, 0]
        self.prev_state = False

    def update(self, time):
        self.prev_mouse_pos = self.curr_mouse_pos
        self.curr_mouse_pos = self.get_position()
        self.velocity = self.get_velocity(time)
        if self.collision_item != None:
            self.prev_state = False

    def get_position(self):
        return pygame.mouse.get_pos()

    def check_buttons(self):
        mouse_buttons = pygame.mouse.get_pressed()
        self.left_held = mouse_buttons[0]
        self.middle_held = mouse_buttons[1]
        self.right_held = mouse_buttons[2]

    def collision_pin_check(self, pin):
        mouse_x, mouse_y = self.get_position()
        upper_bound_x = WIDTH / 4 + pin.x + pin.radius
        lower_bound_x = WIDTH / 4 + pin.x - pin.radius
        upper_bound_y = pin.y + pin.radius
        lower_bound_y = pin.y - pin.radius
        return lower_bound_x <= mouse_x <= upper_bound_x and lower_bound_y <= mouse_y <= upper_bound_y

    def collision_pen_check(self, pen):
        for rod in pen.rods:
            if self.collision_pin_check(rod.pin_1) and not (pen.type == DOUBLE and rod.rod_id == 2):
                self.collision_item = [pen, rod.pin_1]
            elif self.collision_pin_check(rod.pin_2):
                self.collision_item = [pen, rod.pin_2]

    def get_displaysment(self):
        dx = self.curr_mouse_pos[0] - self.prev_mouse_pos[0]
        dy = self.curr_mouse_pos[1] - self.prev_mouse_pos[1]
        return [dx, dy]

    def get_velocity(self, time):
        distance = self.get_displaysment()
        dx_speed = distance[0] / time if time > 0 else 0
        dy_speed = distance[1] / time if time > 0 else 0
        return [dx_speed, dy_speed]

    def direction_angle_from_vertical(self):
        distance = self.get_displaysment()
        if distance[0] == 0 and distance[1] == 0:
            return 0
        return math.pi - math.atan2(distance[0], distance[1])
