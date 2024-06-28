# Import--------------------------------------------
import pygame
import math

class Input:
    def __init__(self):
        self.mouse=mouse()
    
    def update(self,time):
        self.mouse.update(time)


class mouse:
    def __init__(self):
        self.is_mouse_button_held = pygame.mouse.get_pressed(3)[0]
        self.left_click_held = pygame.mouse.get_pressed(3)[0]
        self.collision_item = None
        self.prev_mouse_pos = self.get_position()
        self.curr_mouse_pos = [0,0]
        self.velocity =  [0,0]
        self.prev_state = 0

    def update(self,time):
        self.prev_mouse_pos = self.curr_mouse_pos
        self.curr_mouse_pos = self.get_position()
        self.velocity = self.get_velocity(time)

    def collision_bound_check(self,pin):
        mouse_x, mouse_y = self.get_position()
        # print(f"mouse held at ({mouse_x},{mouse_y})")
        upper_bound_x = pin.x + pin.pin_radius
        lower_bound_x = pin.x - pin.pin_radius
        upper_bound_y = pin.y + pin.pin_radius
        lower_bound_y = pin.y - pin.pin_radius
        if   lower_bound_x <= mouse_x <= upper_bound_x:
            if  lower_bound_y <= mouse_y <= upper_bound_y:
                # print(f"mouse held pin at ({mouse_x},{mouse_y})")
                return True
        return False

    def collision(self,pen_array):
        for pen in pen_array:
            for rod in pen.rods:
                # Check collision on p1
                if self.collision_bound_check(rod.pin1) == True:
                    self.collision_item = [pen,rod.pin1]
                    break
                # Check collision on p2               
                elif self.collision_bound_check(rod.pin2) == True:
                    self.collision_item = [pen,rod.pin2]
                    break
                # else:
                #     self.collision_item = None

    def get_position(self):
        return pygame.mouse.get_pos()
    
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
        if time.elapsed_time>0:
            dx_speed = dx/time.elapsed_time
            dy_speed = dy/time.elapsed_time
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