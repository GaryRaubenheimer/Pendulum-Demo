# Import--------------------------------------------
import sys
import pygame
import math
import time



mouse_x = 0
mouse_y = 0
is_button_held = False

prev_mouse_x = 0
prev_mouse_y = 0

curr_mouse_x = 0 
curr_mouse_y = 0

def init_mouse():
    global prev_mouse_x
    global prev_mouse_y
    global mouse_x
    global mouse_y 
    global is_button_held 
    global is_p1_clicked 
    global is_p2_clicked

    mouse_x = 0
    mouse_y = 0
    is_button_held = False
    is_p1_clicked = False
    is_p2_clicked = False

    prev_mouse_x = 0
    prev_mouse_y = 0
    
    prev_mouse_x, prev_mouse_y = pygame.mouse.get_pos()


def get_mouse_speed(prev_x, prev_y, prev_time):
    global curr_mouse_x
    global curr_mouse_y

    curr_mouse_x, curr_mouse_y = pygame.mouse.get_pos()
    dx = curr_mouse_x - prev_x
    dy = curr_mouse_y - prev_y

    # print (curr_mouse_x, prev_x , dx)
    
    distance = (dx**2 + dy**2)**0.5

    curr_time = time.time()
    elapsed_time = curr_time - prev_time

    if elapsed_time > 0:                # divide by zero error
        speed = distance/elapsed_time
        dx_speed = dx/elapsed_time
        dy_speed = dy/elapsed_time
    else:
        speed = 0
        dx_speed = 0
        dy_speed = 0

    prev_time = curr_time

    # print(f"mouse speed : {speed} pixels/second")
    # print(f"mouse dx speed : {dx_speed} pixels/second")
    # print(f"mouse dy speed : {dy_speed} pixels/second")
    # print("----------")
    # print (curr_mouse_x, prev_x , dx)
    # print("------")


def update_mouse():
    curr_mouse_x, curr_mouse_y = pygame.mouse.get_pos()

    global prev_mouse_x
    prev_mouse_x = curr_mouse_x

    global prev_mouse_y 
    prev_mouse_y = curr_mouse_y