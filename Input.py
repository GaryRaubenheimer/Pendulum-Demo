# Import--------------------------------------------
import sys
import pygame
import math


class Input:
    def __init__(self):
        self.mouse=mouse()
    
    def update(self):
        self.mouse.update()


class mouse:
    def __init__(self):
        self.is_mouse_button_held = pygame.mouse.get_pressed(3)[0]
        self.left_click_held = pygame.mouse.get_pressed(3)[0]
        self.collision_item = None
        self.prev_time = pygame.time.get_ticks()
        self.curr_time = 0
        self.elapsed_time = 0


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


    def collision(self,rods):
        # Check collision on p1
        if self.collision_bound_check(rods[0].pin1) == True:
            self.collision_item = rods[0].pin1
        # Check collision on p2               
        elif self.collision_bound_check(rods[0].pin2) == True:
            self.collision_item = rods[0].pin2
        else:
            self.collision_item = None


    def update(self):
        # print(self.get_velocity())
        self.get_displaysment()
        self.is_mouse_button_held = pygame.mouse.get_pressed(3)[0]
        self.left_click_held = pygame.mouse.get_pressed(3)[0]
    

    def get_position(self):
        return pygame.mouse.get_pos()
    

    def get_displaysment(self):
        self.curr_time = pygame.time.get_ticks()
        self.elapsed_time = self.curr_time - self.prev_time
        self.prev_time = self.curr_time
        return pygame.mouse.get_rel()
    

    def get_velocity(self):
        displaysment = self.get_displaysment()
        dx = displaysment[0]
        dy = displaysment[1]

        if self.elapsed_time>0:
            dx_speed = dx/self.elapsed_time
            dy_speed = dy/self.elapsed_time

        return [dx_speed,dy_speed]


'''
                mouse_x, mouse_y = event.pos
                # print(f"mouse released at ({mouse_x},{mouse_y})")
                # release p1 if held
                if is_p1_clicked:
                    is_p1_clicked = False
                    # print("release p1")
                # release p2 if held
                if is_p2_clicked:
                    is_p2_clicked = False
                    # print("release p2")
'''