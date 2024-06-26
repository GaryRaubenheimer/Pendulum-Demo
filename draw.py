# Import--------------------------------------------
import pygame
import math

from Rod import *
from colour import *

TRACE_POINT_LENGHT = 50
WIDTH,HEIGHT = 800,600
ORIGIN_POINT = [WIDTH/2, HEIGHT/3]

def init_screen():
    # Ensure pygame is initialized
    if not pygame.get_init():
        pygame.init()
    # Set the display mode
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Pedulum')
    screen.fill(LIGHT_GREY)
    return screen


def draw_rods(screen, rods,input):
    # print("draw rods")
    for rod in rods:
         # draw trace points
        if len(rod.trace_points)<TRACE_POINT_LENGHT:
            rod.trace_points.append(rod.pin2.position[:]) # [:]Create copy of the current position
        else:
            rod.trace_points.pop(0)

        if len(rods)>1:
            for i in range(len(rod.trace_points)):
                if rod == rods[1]:
                    pygame.draw.circle(screen, DARK_GREEN, rod.trace_points[i], 1)
                elif rod == rods[0]:
                    pygame.draw.circle(screen, BLUE, rod.trace_points[i], 1)
        else:
            for i in range(len(rods[0].trace_points)):
                pygame.draw.circle(screen, DARK_GREEN, rods[0].trace_points[i], 1)

        # draw line
        pygame.draw.line(screen, rod.bar.bar_colour, rod.pin1.position, rod.pin2.position, rod.bar.bar_width)

        # draw begin point
        if rod == rods[0]:
            pygame.draw.circle(screen, rod.pin1.colour, rod.pin1.position, rod.pin1.pin_radius)

        # draw end point
        pygame.draw.circle(screen, rod.pin2.colour, rod.pin2.position, rod.pin2.pin_radius)

        #draw mouse click
        if(input.mouse.left_click_held):
            pygame.draw.circle(screen, DARK_YELLOW, input.mouse.get_position(), 3)
    return screen, rods
    