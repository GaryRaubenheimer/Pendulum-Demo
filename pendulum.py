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
GAME_UPDATE_SPEED = 10        # update game ticks every 10 milliseconds 
GAME_FRAME_SPEED = 60         # 60 updates frames per second
GAME_PHYSICS_SPEED = 20       # update physics every 20 milliseconds

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
            weight = 5
            angular_position = math.pi/3
            colour = BLACK
            Rod1 = Rod(p1_pos, lenght, weight, angular_position, colour)
            rods.append(Rod1)
            # rods[0].print_rod_attributs()
            # print("---------")
        if i == 1:
            p1_pos = rods[0].p2_position
            lenght = 50
            weight = 2
            angular_position = math.pi
            colour = BLACK
            Rod2 = Rod(p1_pos, lenght, weight, angular_position, colour)
            rods.append(Rod2)
            # rods[0].print_rod_attributs()

    return rods


def event_handeling(running, input, rods):
# event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN:              # is key pressed
            keys = pygame.key.get_pressed()                 # get pressed keys
            if keys[pygame.K_ESCAPE]:
                running = False  
                break     
        elif event.type == pygame.MOUSEMOTION:          # is mouse on window
            # print("on window")
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:      # is mouse button clicked
            print("MOUSEBUTTONDOWN")
            
            input.mouse.is_mouse_button_held = True
            if event.button == 1:                           # is left click held
                input.mouse.prev_state=input.mouse.is_mouse_button_held
                input.mouse.left_click_held = True
                input.mouse.collision(rods)  
        elif event.type == pygame.MOUSEBUTTONUP:        # is mouse button released
            print("MOUSEBUTTONUP")
            # check if left button is release
            input.mouse.prev_state=input.mouse.is_mouse_button_held
            input.mouse.is_mouse_button_held = False
            if event.button == 1:                           # is left click released
                input.mouse.left_click_held = False
                #input.mouse.collision(rods)
    return running, input


# Main--------------------------------------------
def main():
    print("pedulum")

    time = Time()
    screen = init_screen()
    input = Input()

    rods = create_rod_array(1)

    running = True
    while running:
        # update time 
        time.update()

        # update input state
        input.update(time)

        # pygame event handeling
        running, input = event_handeling(running, input, rods)

        # update game
        # handle input
        if input.mouse.is_mouse_button_held:# perform action when held
            if input.mouse.left_click_held:
                if input.mouse.collision_item != None:  # mouse is holding item
                    for rod in rods:
                        if input.mouse.collision_item == rod.pin1:
                            # print("Holding p1")
                            rod.pin1.update_pin(input.mouse.get_position())
                        elif input.mouse.collision_item == rod.pin2:
                            # print("Holding p2")
                            mouse_x, mouse_y = input.mouse.get_position()
                            p2 = [mouse_x, mouse_y]
                            dx = p2[0]-rod.pin1.x
                            dy = p2[1]-rod.pin1.y

                            angle = math.atan2(dx, dy)
                            angle_with_vertical =  angle

                            rod.angular_velocity = 0
                            rod.angular_position = angle_with_vertical
                        else:
                            pass
        elif input.mouse.is_mouse_button_held == False and input.mouse.prev_state:
            if input.mouse.left_click_held==False:
                if input.mouse.collision_item != None:  #mouse is releasing 
                    for rod in rods:
                        if input.mouse.collision_item == rod.pin1:
                            # print("Releasing p1")
                            rod.pin1.update_pin(input.mouse.get_position())
                            input.mouse.collision_item = None       #release item
                        elif input.mouse.collision_item == rod.pin2:
                            print("Releasing p2")
                            rod.pin2.update_pin(input.mouse.get_position())

                            mouse_velocity = input.mouse.velocity
                            mouse_velocity_angnle = input.mouse.direction_angle_from_vertical()

                            beta = 0
                            
                            if mouse_velocity_angnle!=0:
                                beta = (mouse_velocity_angnle-((3*math.pi-rod.angular_position)%(2*math.pi)))
                                mouse_mag = (mouse_velocity[0]**2+mouse_velocity[1]**2)**0.5
                                new_angular_velocity = mouse_mag*math.sin(beta)*rod.rod_lenght*0.0003
                                rod.angular_velocity = -new_angular_velocity
                            else:
                                rod.angular_velocity = 0

                            input.mouse.collision_item != None
                            #input.mouse.prev_state = False
                        else:
                            pass
        input.mouse.prev_state = input.mouse.is_mouse_button_held

        # udate rods
        rods = update_rods(rods)

        # draw graphics
        screen, rods = draw_rods(screen, rods, input)

        # update the display
        clock.tick(GAME_FRAME_SPEED)
        # print(clock.get_fps())
        pygame.display.flip() # update surface
        screen.fill(LIGHT_GREY)    # refresh screen


    pygame.quit()
    sys.exit()


if __name__=="__main__":
    main()

