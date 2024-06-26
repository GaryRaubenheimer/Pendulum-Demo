# Import--------------------------------------------
import pygame
import math

from Rod import *
from colour import *

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


def draw_rods(screen, pen_array, input):
    # print("draw rods")
    for pen in pen_array:
        for rod in pen.rods:
            # draw trace points
            if len(pen.rods)>1:
                for i in range(len(rod.trace_points)):
                    if rod == pen.rods[1]:
                        pygame.draw.circle(screen, DARK_GREEN, rod.trace_points[i], 1)
                    elif rod == pen.rods[0]:
                        pygame.draw.circle(screen, BLUE, rod.trace_points[i], 1)
            else:
                for i in range(len(pen.rods[0].trace_points)):
                    pygame.draw.circle(screen, DARK_GREEN, pen.rods[0].trace_points[i], 1)

            # draw line
            pygame.draw.line(screen, rod.bar.bar_colour, rod.pin1.position, rod.pin2.position, rod.bar.bar_width)

            # draw begin point
            if rod.origin_rod == True:
                pygame.draw.circle(screen, rod.pin1.colour, rod.pin1.position, rod.pin1.pin_radius)

            # draw end point
            pygame.draw.circle(screen, rod.pin2.colour, rod.pin2.position, rod.pin2.pin_radius)

            #draw mouse click
            if(input.mouse.left_click_held):
                pygame.draw.circle(screen, DARK_YELLOW, input.mouse.get_position(), 3)
    return screen, pen_array
    