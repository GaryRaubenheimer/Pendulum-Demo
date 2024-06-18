# Import--------------------------------------------
import sys
import pygame
import math
import time

from bar import *
from colour import *
from pendulum import screen


BAR_WIDTH = 5
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


def draw_bar(screen, bar):
    # print("draw bar")

    # draw line
    pygame.draw.line(screen, bar.colour, bar.p1_position, bar.p2_position, BAR_WIDTH)
    
    # draw begin point
    pygame.draw.circle(screen, RED, bar.p1_position, BAR_WIDTH)

    # draw trace points
    if len(bar.trace_points)<TRACE_POINT_LENGHT:
        bar.trace_points.append(bar.p2_position[:]) # [:]Create copy of the current position
    else:
        bar.trace_points.pop(0)

    for i in range(len(bar.trace_points)):
        pygame.draw.circle(screen, GREEN, bar.trace_points[i], 1)
        
    
    # draw end point
    pygame.draw.circle(screen, RED, bar.p2_position, BAR_WIDTH)

    return screen, bar
    