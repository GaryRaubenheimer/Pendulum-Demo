# Import--------------------------------------------
import sys
import pygame
import math

from Rod import *
from engine_physics import *
from draw import *
from Input import *
from colour import *
from Time import *


# Initialise global variable------------------------
GAME_SPEED = 60         # 60 updates per second

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


def event_handeling(running, input, rods):
# event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:              # is key pressed
            keys = pygame.key.get_pressed()                 # get pressed keys
            if keys[pygame.K_ESCAPE]:
                running = False       
        elif event.type == pygame.MOUSEMOTION:          # is mouse on window
            # print("on window")
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:      # is mouse button clicked
            input.mouse.is_mouse_button_held = True
            if event.button == 1:                           # is left click held
                input.mouse.left_click_held = True
                input.mouse.collision(rods)  
        elif event.type == pygame.MOUSEBUTTONUP:        # is mouse button released
            # check if left button is release
            input.mouse.is_mouse_button_held = False
            if event.button == 1:                           # is left click released
                input.mouse.left_click_held = False
                input.mouse.collision(rods)

    return running, input


# Main--------------------------------------------
def main():
    print("pedulum")

    screen = init_screen()
    input = Input()
    Time = Time()
    rods = create_rod_array(1)

    running = True
    while running:
        # update time 
        Time.update()

        # pygame event handeling
        running, input = event_handeling(running, input, rods)

        # update game
        if input.mouse.is_mouse_button_held:        # perform action when held
            if input.mouse.left_click_held:
                if input.mouse.collision_item != None:   # mouse is holding item
                    if input.mouse.collision_item == rods[0].pin1:
                        # print("Holding p1")
                        rods[0].pin1.update_pin(input.mouse.get_position())
                    elif input.mouse.collision_item == rods[0].pin2:
                        # print("Holding p2")
                        mouse_x, mouse_y = input.mouse.get_position()
                        p2 = [mouse_x, mouse_y]
                        dx = p2[0]-rods[0].pin1.x
                        dy = p2[1]-rods[0].pin1.y
        
                        angle = math.atan2(dx, dy)
                        angle_with_vertical =  angle
        
                        rods[0].angular_velocity = 0
                        rods[0].angular_position = angle_with_vertical
                    else:
                        pass
            else:
                if input.mouse.collision_item != None:   # mouse is releasing item        
                    if input.mouse.collision_item == rods[0].pin1:
                        # print("Releasing p1")
                        rods[0].pin1.update_pin_position(pygame.mouse.get_pos())
                    elif input.mouse.collision_item == rods[0].pin2:
                        # print("Releasing p2")

                        mouse_velocity = input.mouse.get_velocity()
                        rods[0].pin2.x_speed = mouse_velocity[0]
                        rods[0].pin2.y_speed = mouse_velocity[1]
                        
                    else:
                        pass
        
        rods = update_rods(rods)
        input.update()

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

