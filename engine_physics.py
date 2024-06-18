# Import--------------------------------------------
import sys
import pygame
import math
import time

GRAVITY = 0.1          # 9.81 m per second^2
DAMPING_FACTOR = 0.99   # friction

def update_rods(rods):
    # print("update rod")
    for rod in rods:
        update_angular_position(rod)
        update_p2_position(rod)
        # rod.print_rod_attributs()
    return rods


def update_angular_position(rod):
    torque = -rod.weight*GRAVITY*rod.lenght*math.sin(rod.angular_position)
    rod.angular_accaleration = torque/rod.moment_of_inertia

    rod.angular_velocity += rod.angular_accaleration
    rod.angular_position += rod.angular_velocity
    rod.angular_velocity *= DAMPING_FACTOR

    # limit angle for stability
    if rod.angular_position>(2*math.pi):
        rod.angular_position = rod.angular_position - (2*math.pi)
    elif rod.angular_position<(-2*math.pi):
        rod.angular_position = rod.angular_position + (2*math.pi)


def update_p2_position(rod):
    rod.p2_position[0] = rod.p1_position[0] + rod.lenght*math.sin(rod.angular_position)
    rod.p2_position[1] = rod.p1_position[1] + rod.lenght*math.cos(rod.angular_position)

    return rod.p2_position