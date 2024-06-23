# Import--------------------------------------------
import sys
import pygame
import math
import time

GRAVITY = 1.1          # 9.81 m per second^2
DAMPING_FACTOR = 0.98   # friction

def update_rods(rods):
    # print("update rod")
    at_end=True
    for rod in rods:
        rod = update_angular_velocity(rod)
        rod = update_angular_position(rod,at_end)
        rod.update_p2_position()
        # rod.print_rod_attributs()
    return rods

def update_angular_velocity(rod):
    #rod.angular_velocity=rod.pin2.speed/rod.rod_lenght
    return rod

def update_angular_position(rod, at_end):
    if at_end:
        torque = -rod.rod_weight*GRAVITY*rod.rod_lenght*math.sin(rod.angular_position)
        # print(torque)
        if -100<torque<100:
            torque=0

        # print(torque)
        # print("-------")
        rod.angular_accaleration = torque/rod.moment_of_inertia_at_end
    else:
        torque = -rod.rod_weight*GRAVITY*rod.rod_lenght*math.sin(rod.angular_position)
        #if -0.1<torque<0.1:
        #    torque=0
        rod.angular_accaleration = torque/rod.moment_of_inertia_at_center

    rod.angular_velocity += rod.angular_accaleration
    rod.angular_position += rod.angular_velocity
    # print(rod.angular_position/math.pi)
    if -0.0005<rod.angular_position/math.pi<0.0005:
       rod.angular_position=0
    # print(rod.angular_position/math.pi)
    rod.angular_velocity *= DAMPING_FACTOR

    # limit angle for stability
    if rod.angular_position>(2*math.pi):
        rod.angular_position = rod.angular_position - (2*math.pi)
    elif rod.angular_position<(-2*math.pi):
        rod.angular_position = rod.angular_position + (2*math.pi)

    return rod


