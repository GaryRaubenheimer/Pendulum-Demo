# Import--------------------------------------------
import sys
import pygame
import math

from Rod import *
from colour import *
from pendulum import screen


TRACE_POINT_LENGHT = 50
WIDTH,HEIGHT = 800,600
ORIGIN_POINT = [WIDTH/2, HEIGHT/3]


def init_screen():
    # Ensure pygame is initialized
    if not pygame.get_init():
        pygame.init()

    # Set the display mode
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Single Pedulum')

    screen.fill(WHITE)

    return screen


def draw_rods(screen, rods):
    # print("draw rods")

    for rod in rods:
        # draw line
        pygame.draw.line(screen, rod.bar.bar_colour, rod.pin1.position, rod.pin2.position, rod.bar.bar_width)

        # draw begin point
        pygame.draw.circle(screen, rod.pin1.colour, rod.pin1.position, rod.pin1.pin_radius)

        # draw trace points
        if len(rod.trace_points)<TRACE_POINT_LENGHT:
            rod.trace_points.append(rod.pin2.position[:]) # [:]Create copy of the current position
        else:
            rod.trace_points.pop(0)

        for i in range(len(rod.trace_points)):
            pygame.draw.circle(screen, GREEN, rod.trace_points[i], 1)


        # draw end point
        pygame.draw.circle(screen, rod.pin2.colour, rod.pin2.position, rod.pin2.pin_radius)
        # print(rod.pin2.position)

    return screen
    