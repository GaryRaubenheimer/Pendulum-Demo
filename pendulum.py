# Import--------------------------------------------
import sys
import pygame
import math
import time

from Rod import *
from engine_physics import *
from draw import *
from input import *
from colour import *


# Initialise global variable------------------------
GAME_SPEED = 60         # 60 updates per second
"""
loop_check=0
        global loop_check
        if loop_check in range(1000):
            loop_check+=1
        else:
            loop_check = 0
        print(loop_check)
"""
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.init()


#Classes--------------------------------------------


# Functions--------------------------------------------
def create_rod_array(number_of_rods): 
    # print("create rods") 
    
    # initialise values per rod
    p1_pos = [0,0]
    lenght = 100
    weight = 5
    angular_position = 0
    
    rods=[]
    
    for i in range(number_of_rods):
        if i == 0:
            p1_pos = ORIGIN_POINT
            lenght = 100
            weight = 100
            angular_position = math.pi/4
            colour = BLACK
            rods.append(Rod(p1_pos, lenght, weight, angular_position, colour))
            continue

        p1_pos = rods[i-1].p2_posistion[1]
        colour = (100,100,100)

        rods.append(Rod(p1_pos, lenght, weight, angular_position, colour))
    
    return rods


def event_handeling(running, rods, is_button_held,is_p1_clicked, is_p2_clicked):
# event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False       
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # check if left button is pressed
            if event.button == 1:
                is_button_held = True
                mouse_x, mouse_y = event.pos
                # print(f"mouse held at ({mouse_x},{mouse_y})")

                # Check if clicked on p1
                upper_bound_x = rods[0].p1_position[0] + ROD_WIDTH
                lower_bound_x = rods[0].p1_position[0] - ROD_WIDTH
                upper_bound_y = rods[0].p1_position[1] + ROD_WIDTH
                lower_bound_y = rods[0].p1_position[1] - ROD_WIDTH
                if   lower_bound_x <= mouse_x <= upper_bound_x:
                    if  lower_bound_y <= mouse_y <= upper_bound_y:
                        is_p1_clicked = True
                        # print(f"mouse held at ({mouse_x},{mouse_y})")

                # Check if clicked on p2               
                upper_bound_x = rods[0].p2_position[0] + ROD_WIDTH
                lower_bound_x = rods[0].p2_position[0] - ROD_WIDTH
                upper_bound_y = rods[0].p2_position[1] + ROD_WIDTH
                lower_bound_y = rods[0].p2_position[1] - ROD_WIDTH
                if   lower_bound_x <= mouse_x <= upper_bound_x:
                    if  lower_bound_y <= mouse_y <= upper_bound_y:
                        is_p2_clicked = True
                        # print(f"mouse held at ({mouse_x},{mouse_y})") 
                                    
        elif event.type == pygame.MOUSEBUTTONUP:
            # check if left button is release
            if event.button == 1:
                is_button_held = False
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
    
    return running, rods, is_button_held,is_p1_clicked, is_p2_clicked


# Main--------------------------------------------
def main():
    print("n-ple pedulum")

    screen = init_screen()
    init_mouse()

    is_button_held = False
    is_p1_clicked = False
    is_p2_clicked = False

    rods = create_rod_array(1)
    running = True
    prev_time = time.time()

    while running:
        # pygame event handeling
        running, rods, is_button_held,is_p1_clicked, is_p2_clicked = event_handeling(running, rods, is_button_held,is_p1_clicked, is_p2_clicked)

        if is_button_held:
            # perform action when held
            if is_p1_clicked:
                # print("Holding p1")
                mouse_x, mouse_y = pygame.mouse.get_pos()

                rods[0].p1_position[0] = mouse_x
                rods[0].p1_position[1] = mouse_y

            elif is_p2_clicked:
                # print("Holding p2")
                mouse_x, mouse_y = pygame.mouse.get_pos()

                p2 = [mouse_x, mouse_y]
                dx = p2[0]-rods[0].p1_position[0]
                dy = p2[1]-rods[0].p1_position[1]

                angle = math.atan2(dx, dy)
                angle_with_vertical =  angle

                rods[0].angular_acceleration = 0
                rods[0].angular_velocity = 0
                rods[0].angular_position = angle_with_vertical
            pass

        # update game
        rods = update_rods(rods)
        get_mouse_speed(prev_mouse_x, prev_mouse_y, prev_time)
        update_mouse()


        # draw graphics
        for rod in rods:
            screen, rod= draw_rod(screen, rod)


        # update the display
        clock.tick(GAME_SPEED)
        # print(clock.get_fps())
        pygame.display.flip() # update surface
        screen.fill(WHITE)    # refresh screen


    pygame.quit()
    sys.exit()


if __name__=="__main__":
    main()

