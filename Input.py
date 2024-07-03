import math

from Pendulum_Demo import pygame
from constants import *

class Mouse:
    def __init__(self):
        print("create mouse")
        self.check_buttons()
        self.collision_item = None
        self.prev_mouse_pos = self.get_position()
        self.curr_mouse_pos = [0,0]
        self.velocity =  [0,0]
        self.prev_state = False

    def update(self,time):
        self.prev_mouse_pos = self.curr_mouse_pos
        self.curr_mouse_pos = self.get_position()
        self.velocity = self.get_velocity(time)
    
    def get_position(self):
        return pygame.mouse.get_pos()


    def check_buttons(self):
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:    #Left mouse
            self.left_held = True
        else:
            self.left_held = False
        if mouse_buttons[1]:    #Middle mouse
            self.middle_held = True
        else:
            self.middle_held = False
        if mouse_buttons[2]:    #Right mouse
            self.right_held = True
        else:
            self.right_held = False
        

    def collision_pin_check(self,pin):
        mouse_x, mouse_y = self.get_position()
        upper_bound_x = WIDTH/4 +pin.x + pin.radius
        lower_bound_x = WIDTH/4 +pin.x - pin.radius
        upper_bound_y = pin.y + pin.radius
        lower_bound_y = pin.y - pin.radius
        if   lower_bound_x <= mouse_x <= upper_bound_x:
            if  lower_bound_y <= mouse_y <= upper_bound_y:
                return True
        return False

    def collision_pen_check(self,pen):    
        for rod in pen.rods:
            # Check collision on p1 for rod
            if self.collision_pin_check(rod.pin_1) == True:
                if not(pen.type == DOUBLE and rod.rod_id == 2):
                    self.collision_item = [pen,rod.pin_1]
            # Check collision on p2 for rod       
            elif self.collision_pin_check(rod.pin_2) == True:
                self.collision_item = [pen,rod.pin_2]

    def get_displaysment(self):
        dx = self.curr_mouse_pos[0] - self.prev_mouse_pos[0]
        dy = self.curr_mouse_pos[1] - self.prev_mouse_pos[1]
        distance = [dx,dy]
        return distance

    def get_velocity(self,time):
        distance = self.get_displaysment()
        dx = distance[0]
        dy = distance[1]
        dx_speed = 0
        dy_speed = 0
        if time>0:
            dx_speed = dx/time
            dy_speed = dy/time
        velocity = [dx_speed, dy_speed]
        return velocity
    
    def direction_angle_from_vertical(self):
        distance = self.get_displaysment()
        delta_x = distance[0]
        delta_y = distance[1]
        if delta_y == 0 and delta_x == 0:
            angle =0
        else:
            angle = math.pi - math.atan2(delta_x, delta_y)
        return angle

