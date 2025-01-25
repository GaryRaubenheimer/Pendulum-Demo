import pygame

from colour import *
from constants import *


def draw_rods(screen, pen_array):
    for pen in pen_array:
        for rod in pen.rods:
            draw_trace_points(screen, rod)
            draw_bar(screen, rod)
            draw_pins(screen, rod)

    return screen, pen_array

def draw_trace_points(screen, rod):
    if rod.pin_2.trace_points_isOn:
        # draw trace points as points
        if not rod.pin_2.trace_points_isLine:
            for point in rod.pin_2.trace_points:
                pygame.draw.circle(screen, rod.pin_2.trace_points_colour, point, 1)
        else:
        # draw trace points as line
            for i in range(len(rod.pin_2.trace_points)):
                if i > 0:
                    pygame.draw.line(screen, rod.pin_2.trace_points_colour, rod.pin_2.trace_points[i-1], rod.pin_2.trace_points[i])

def draw_bar(screen, rod):
    pygame.draw.line(screen, rod.bar.colour, rod.pin_1.position, rod.pin_2.position, rod.bar.width)

def draw_pins(screen, rod):
    if rod.rod_id == 1:
        pygame.draw.circle(screen, rod.pin_1.colour, rod.pin_1.position, rod.pin_1.radius)
    pygame.draw.circle(screen, rod.pin_2.colour, rod.pin_2.position, rod.pin_2.radius)
