from Pendulum_Demo import pygame
import math

from constants import *

def pygame_event_buffer(running):
    # pygame event handling
    events = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        # Keyboard events
        elif event.type == pygame.KEYDOWN:              # is key pressed
            # keys = pygame.key.get_pressed()           # get all pressed keys
            if event.key == pygame.K_ESCAPE:
                running = False  
                break  
        # Mouse events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            events.append(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            events.append(event)
        elif event.type == pygame.MOUSEMOTION:
            events.append(event)
        

    return running,events

def handle_event_buffer(events,M,pen_array,gui_widget_list):
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:                       #Left mouse button pressed
                #print("Left mouse button pressed")
                M.left_held = True
                for pen in pen_array:
                    M.collision_pen_check(pen)
            elif event.button == 2:                     #Middle mouse button pressed
                #print("Middle mouse button pressed")
                pass
            elif event.button == 3:                     #Right mouse button pressed
                #print("Right mouse button pressed")
                M.right_held = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                M.prev_state = M.left_held
                M.left_held = False
            elif event.button == 2:
                pass
            elif event.button == 3:
                M.right_held = True
        #handle gui widget events
        for widget in gui_widget_list:
            widget.handle_event(event)




def update_pedulum_events(M,dt):
    mo = M.get_position()
    pos = []
    pos.append(mo[0] - WIDTH/4)
    pos.append(mo[1])

    if M.left_held == True:
        if M.collision_item != None:  # mouse is holding item
            held_pendulum = M.collision_item[0]
            held_pin = M.collision_item[1]
            if held_pin == held_pendulum.rods[0].pin_1:  #first rods pin 1
                #print("Holding p1")
                if (BORDER_THICKNESS+2.5)<pos[0]<(WIDTH/4*3-BORDER_THICKNESS-2.5):
                    if (BORDER_THICKNESS+2.5)<pos[1]<(HEIGHT-BORDER_THICKNESS-2.5):
                        held_pendulum.rods[0].pin_1.update_pos(pos)
                        held_pendulum.rods[0].update()
                        if held_pendulum.type ==DOUBLE:
                            held_pendulum.rods[1].pin_1.update_pos(held_pendulum.rods[0].pin_2.position)
                            held_pendulum.rods[1].update()
            elif held_pin == held_pendulum.rods[0].pin_2 and held_pendulum.type == DOUBLE:   
                #first pin p2 double
                #print("Holding split")
                held_pendulum.split()
                rod1 = held_pendulum.rods[0]
                rod2 = held_pendulum.rods[1]
                dx = pos[0]-rod1.pin_1.x
                dy = pos[1]-rod1.pin_1.y
                angle = math.atan2(dx, dy)
                angle_with_vertical =  angle
                rod1.angular_velocity = 0
                rod1.angular_position = angle_with_vertical
                rod1.update()
                rod2.pin_1.update_pos(rod1.pin_2.position)
                rod2.update()
            elif held_pin == held_pendulum.rods[held_pendulum.type-1].pin_2: 
                #last rods pin 2
                #print("Holding p2")
                rod = held_pendulum.rods[held_pendulum.type-1]
                dx = pos[0]-rod.pin_1.x
                dy = pos[1]-rod.pin_1.y
                angle = math.atan2(dx, dy)
                angle_with_vertical =  angle
                rod.angular_velocity = 0
                rod.angular_position = angle_with_vertical
                rod.update()

    if M.left_held == False and M.prev_state == True:
        if M.collision_item != None:  #mouse is releasing 
            held_pendulum = M.collision_item[0]
            held_pin = M.collision_item[1]
            if held_pin == held_pendulum.rods[0].pin_1:  #first rods pin 1
                print("Release p1")
                M.collision_item = None
            elif held_pin == held_pendulum.rods[0].pin_2 and held_pendulum.type == DOUBLE:   
                #first pin p2 double
                print("Release split")
                held_pendulum.unsplit()
                rod = held_pendulum.rods[0]
                mouse_velocity = M.get_velocity(dt)
                mouse_velocity_angnle = M.direction_angle_from_vertical()
                beta = 0                              
                if mouse_velocity_angnle!=0:
                    beta = (mouse_velocity_angnle-((3*math.pi-rod.angular_position)%(2*math.pi)))
                    mouse_mag = (mouse_velocity[0]**2+mouse_velocity[1]**2)**0.5
                    new_angular_velocity = mouse_mag*math.sin(beta)*rod.bar.lenght*0.0003
                    rod.angular_velocity = -new_angular_velocity
                else:
                    rod.angular_velocity = 0
                M.collision_item = None
            elif held_pin == held_pendulum.rods[held_pendulum.type-1].pin_2: #last rods pin 2
                print("Releasing p2")
                rod = held_pendulum.rods[held_pendulum.type-1]
                mouse_velocity = M.get_velocity(dt)
                mouse_velocity_angnle = M.direction_angle_from_vertical()
                beta = 0                              
                if mouse_velocity_angnle!=0:
                    beta = (mouse_velocity_angnle-((3*math.pi-rod.angular_position)%(2*math.pi)))
                    mouse_mag = (mouse_velocity[0]**2+mouse_velocity[1]**2)**0.5
                    new_angular_velocity = mouse_mag*math.sin(beta)*rod.bar.lenght*0.0003
                    rod.angular_velocity = -new_angular_velocity
                else:
                    rod.angular_velocity = 0
                M.collision_item = None
        M.prev_state == False
    
