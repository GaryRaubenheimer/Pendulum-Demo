# Import--------------------------------------------
import sys
import pygame
import math

class Time:   
    def __init__(self):
        self.prev_time = pygame.time.get_ticks()
        self.curr_time = 0
        self.elapsed_time = 0
    
    def update(self):
        self.prev_time = self.curr_time 
        self.curr_time = pygame.time.get_ticks()
        self.elapsed_time = self.curr_time - self.prev_time
