# Import--------------------------------------------
import sys
import pygame
import math
import time

from engine_physics import update_p2_position

#Classes--------------------------------------------
class Bar:   
    
    p1_position = [0,0]
    p2_position = [0,0]
    trace_points = []

    def __init__(self, p1_position, lenght, weight, angular_position, colour ):
        self.p1_position = p1_position
        self.lenght = lenght
        self.weight = weight
        self.angular_position = angular_position
        self.p2_position = update_p2_position(self)
        self.angular_velocity = 0
        self.angular_accaleration = 0
        self.colour = colour
        self.angular_momentum = 0
        self.moment_of_inertia = (1/3)*self.weight*self.lenght**2
    

    def get_p2_position(self):
        return self.p2_position


    def print_bar_attributs(self):
        print(self.__dict__)
