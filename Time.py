# Import--------------------------------------------
import sys
import pygame
import math

class Time:   
    def __init__(self):
        if not pygame.get_init():
            pygame.init()
            # TO DO: test if not clock then activate clock 
            # clock = pygame.time.Clock() 
            
        self.prev_time = pygame.time.get_ticks()    
        #Return the number of milliseconds since pygame.init() was called. initialized this will always be 0.

        self.curr_time = 0
        self.elapsed_time = 0
    
    def update(self):
        self.prev_time = self.curr_time 
        self.curr_time = pygame.time.get_ticks()
        self.elapsed_time = self.curr_time - self.prev_time
