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
GAME_FRAME_SPEED = 60         # 60 updates frames per second
GAME_PHYSICS_SPEED =20       # update physics every 20 milliseconds
SINGLE = 1
DOUBLE = 2

pygame.init()
clock_GAME = pygame.time.Clock()
screen = pygame.display.init()


# Classes--------------------------------------------
class Pendulum:
    def __init__(self,pendulum_type):
        self.type = pendulum_type
        if self.type == SINGLE:
            self.rods = self.create_rod_array(SINGLE)
        elif self.type == DOUBLE:
            self.rods = self.create_rod_array(DOUBLE)

    def update(self):
        self.rods = update_rods(self.rods,self.type)

    def split(self):
        self.rods[0].type = SINGLE
        self.rods[1].type = SINGLE

    def unsplit(self):
        self.rods[0].type = DOUBLE
        self.rods[1].type = DOUBLE

    def create_rod_array(self,number_of_rods): 
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
                Rod1 = Rod(p1_pos, lenght, weight, angular_position, colour, self.type,True)
                rods.append(Rod1)
            if i == 1:
                p1_pos = rods[0].p2_position
                lenght = 150
                weight = 1
                angular_position = math.pi
                colour = BLACK
                Rod2 = Rod(p1_pos, lenght, weight, angular_position, colour,self.type,False)
                rods.append(Rod2)
        return rods

# Functions--------------------------------------------
def event_handeling(running, input, pen_array):
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
            #print("MOUSEBUTTONDOWN")
            if event.button == 1:                           # is left click held
                input.mouse.is_mouse_button_held = True
                input.mouse.prev_state=input.mouse.is_mouse_button_held
                input.mouse.left_click_held = True
                input.mouse.collision(pen_array)  
        elif event.type == pygame.MOUSEBUTTONUP:        # is mouse button released
            #print("MOUSEBUTTONUP")
            # check if left button is release
            if event.button == 1:                           # is left click released
                input.mouse.prev_state=input.mouse.is_mouse_button_held
                input.mouse.is_mouse_button_held = False
                input.mouse.left_click_held = False
    return running, input

# Main--------------------------------------------
def main():
    print("pedulum")

    time = Time()
    screen = init_screen()
    input = Input()

    pen_array = []
    pen_SINGLE = Pendulum(SINGLE)
    pen_DOUBLE = Pendulum(DOUBLE)

    pen_array.append(pen_DOUBLE)

    physics_acc = 0

    running = True
    while running:
        # update time 
        time.update()
        dt = clock_GAME.tick(GAME_FRAME_SPEED)
        physics_acc += dt

        # update input state
        input.update(time)

        # pygame event handeling
        running, input = event_handeling(running, input, pen_array)

        # update game
        # handle input
        if input.mouse.is_mouse_button_held:# perform action when held
            if input.mouse.left_click_held:
                if input.mouse.collision_item != None:  # mouse is holding item
                    held_pendulum = input.mouse.collision_item[0]
                    held_pin = input.mouse.collision_item[1]

                    if held_pin == held_pendulum.rods[0].pin1:  #first rods pin 1
                        print("Holding p1")
                        held_pendulum.rods[0].pin1.update_pin(input.mouse.get_position())
                        held_pendulum.rods[0].update_p2_position()
                    elif held_pin == held_pendulum.rods[0].pin2 and held_pendulum.type == DOUBLE:   #first pin p2 double
                        print("Holding split")
                        held_pendulum.split()
                        rod1 = held_pendulum.rods[0]
                        rod2 = held_pendulum.rods[1]

                        mouse_x, mouse_y = input.mouse.get_position()
                        p2 = [mouse_x, mouse_y]
                        dx = p2[0]-rod1.pin1.x
                        dy = p2[1]-rod1.pin1.y
                        angle = math.atan2(dx, dy)
                        angle_with_vertical =  angle
                        rod1.angular_velocity = 0

                        rod1.angular_position = angle_with_vertical
                        rod1.update_p2_position()

                        rod2.pin1.update_pin(rod1.pin2.position)
                        rod2.update_p2_position()
                    elif held_pin == held_pendulum.rods[held_pendulum.type-1].pin2: #last rods pin 2
                        print("Holding p2")
                        rod = held_pendulum.rods[held_pendulum.type-1]
                        mouse_x, mouse_y = input.mouse.get_position()
                        p2 = [mouse_x, mouse_y]
                        dx = p2[0]-rod.pin1.x
                        dy = p2[1]-rod.pin1.y
                        angle = math.atan2(dx, dy)
                        angle_with_vertical =  angle
                        rod.angular_velocity = 0
                        rod.angular_position = angle_with_vertical
                        rod.update_p2_position()

        elif input.mouse.is_mouse_button_held == False and input.mouse.prev_state:
            if input.mouse.left_click_held==False:
                if input.mouse.collision_item != None:  #mouse is releasing 
                    held_pendulum = input.mouse.collision_item[0]
                    held_pin = input.mouse.collision_item[1]

                    if held_pin == held_pendulum.rods[0].pin1:  #first rods pin 1
                        print("Release p1")
                        input.mouse.collision_item = None
                        input.mouse.prev_state = False
                    elif held_pin == held_pendulum.rods[0].pin2 and held_pendulum.type == DOUBLE:   #first pin p2 double
                        print("Release split")
                        held_pendulum.unsplit()

                        rod = held_pendulum.rods[0]
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
                        input.mouse.collision_item = None
                        input.mouse.prev_state = False

                    elif held_pin == held_pendulum.rods[held_pendulum.type-1].pin2: #last rods pin 2
                        print("Releasing p2")
                        rod = held_pendulum.rods[held_pendulum.type-1]
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
                        input.mouse.collision_item = None
                        input.mouse.prev_state = False
        input.mouse.prev_state = input.mouse.is_mouse_button_held

        n = 1
        while physics_acc>=GAME_PHYSICS_SPEED:
            for i in range(n):
                for pen in pen_array:
                    pen.update()
            physics_acc-=GAME_PHYSICS_SPEED

        screen, pen_array = draw_rods(screen, pen_array, input)
        pygame.display.flip()
        screen.fill(LIGHT_GREY)
        
        print(clock_GAME.get_fps())

    pygame.quit()
    sys.exit()


if __name__=="__main__":
    main()

