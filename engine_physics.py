# Import--------------------------------------------
import sys
import pygame
import math
import time

GRAVITY = 0.1          # 9.81 m per second^2
DAMPING_FACTOR = 0.99   # friction

def update_bars(bars):
    # print("update bar")
    for bar in bars:
        update_angular_position(bar)
        update_p2_position(bar)
        # bar.print_bar_attributs()
    return bars


def update_angular_position(bar):
    torque = -bar.weight*GRAVITY*bar.lenght*math.sin(bar.angular_position)
    bar.angular_accaleration = torque/bar.moment_of_inertia

    bar.angular_velocity += bar.angular_accaleration
    bar.angular_position += bar.angular_velocity
    bar.angular_velocity *= DAMPING_FACTOR

    # limit angle for stability
    if bar.angular_position>(2*math.pi):
        bar.angular_position = bar.angular_position - (2*math.pi)
    elif bar.angular_position<(-2*math.pi):
        bar.angular_position = bar.angular_position + (2*math.pi)


def update_p2_position(bar):
    bar.p2_position[0] = bar.p1_position[0] + bar.lenght*math.sin(bar.angular_position)
    bar.p2_position[1] = bar.p1_position[1] + bar.lenght*math.cos(bar.angular_position)

    return bar.p2_position