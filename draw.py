# Import--------------------------------------------
import sys
import pygame
import math
import time

from Rod import *
from colour import *
from pendulum import screen


ROD_WIDTH = 5
TRACE_POINT_LENGHT = 50
WIDTH,HEIGHT = 800,600
ORIGIN_POINT = [WIDTH/2, HEIGHT/3]


def init_screen():
    # Ensure pygame is initialized
    if not pygame.get_init():
        pygame.init()

    # Set the display mode
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('n-ple pedulum')

    screen.fill(WHITE)

    return screen


def draw_rod(screen, rod):
    # print("draw rod")

    # draw line
    pygame.draw.line(screen, rod.colour, rod.p1_position, rod.p2_position, ROD_WIDTH)
    
    # draw begin point
    pygame.draw.circle(screen, RED, rod.p1_position, ROD_WIDTH)

    # draw trace points
    if len(rod.trace_points)<TRACE_POINT_LENGHT:
        rod.trace_points.append(rod.p2_position[:]) # [:]Create copy of the current position
    else:
        rod.trace_points.pop(0)

    for i in range(len(rod.trace_points)):
        pygame.draw.circle(screen, GREEN, rod.trace_points[i], 1)
        
    
    # draw end point
    pygame.draw.circle(screen, RED, rod.p2_position, ROD_WIDTH)

    return screen, rod
    