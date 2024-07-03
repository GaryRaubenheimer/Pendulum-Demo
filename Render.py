# Import--------------------------------------------
import pygame
import math

from colour import *
from constants import *


# Define screen functions
# def draw_screen1():
#     screen.fill(RED)
#     font = pygame.font.Font(None, 74)
#     text = font.render("Screen 1", True, WHITE)
#     screen.blit(text, (300, 250))


def draw_rods(screen, pen_array):
    # print("draw rods")
    for pen in pen_array:
        for rod in pen.rods:
            # draw trace points
            if rod.pin_2.trace_points_isLine == False:
                for i in range(len(rod.pin_2.trace_points)):
                    pygame.draw.circle(screen, rod.pin_2.trace_points_colour, rod.pin_2.trace_points[i], 1)
            else:
                for i in range(len(rod.pin_2.trace_points)):
                    if i > 0:
                        pygame.draw.line(screen,rod.pin_2.trace_points_colour,rod.pin_2.trace_points[i-1],rod.pin_2.trace_points[i])


            # draw line
            pygame.draw.line(screen, rod.bar.colour, rod.pin_1.position, rod.pin_2.position, rod.bar.width)

            # draw begin point
            if rod.rod_id == 1:
                pygame.draw.circle(screen, rod.pin_1.colour, rod.pin_1.position, rod.pin_1.radius)

            # draw end point
            pygame.draw.circle(screen, rod.pin_2.colour, rod.pin_2.position, rod.pin_2.radius)

    return screen, pen_array

