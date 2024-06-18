# Import--------------------------------------------
import sys
import pygame
import math
import time


#Classes--------------------------------------------
class Rod:   
    
    p1_position = [0,0]
    p2_position = [0,0]
    trace_points = []


    def __init__(self, p1_position, lenght, weight, angular_position, colour ):

        self.angular_position = angular_position        # from vertical

        # create pins
        # pin 1
        pin1_weight=0
        pin1_radius=0
        pin1_position=p1_position
        self.pin1=pin(1,pin1_position, pin1_weight,pin1_radius)
        # pin 2
        pin2_weight=0
        pin2_radius=0
        pin2_position=self.create_p2_position(lenght)
        self.pin2=pin(2,pin2_position, pin2_weight,pin2_radius)

        # create bar
        bar_weight=weight
        bar_width=5
        bar_lenght=lenght
        bar_colour = colour
        self.bar=bar(bar_lenght, bar_weight, bar_width,bar_colour)
        self.bar_vector = self.pin2.pin_vector-self.pin2.pin_vector # vect from p1 to p2

        # create rod
        self.rod_lenght = self.bar.bar_lenght #+ self.pin1.pin_radius + self.pin2.pin_radius
        self.rod_weight = self.bar.bar_weight #+ self.pin1.pin_weight + self.pin2.pin_weight
        
        self.angular_velocity = 0
        self.angular_accaleration = 0
        self.angular_momentum = 0
        self.moment_of_inertia_at_end = (1/3)*self.rod_weight*self.rod_lenght**2
        self.moment_of_inertia_at_center = (1/12)*self.rod_weight*self.rod_lenght**2
    

    def create_p2_position(self,lenght):
        self.p2_position[0] = self.pin1.x + lenght*math.sin(self.angular_position)
        self.p2_position[1] = self.pin1.y + lenght*math.cos(self.angular_position)

        return self.p2_position

    def update_p2_position(self):
        self.p2_position[0] = self.pin1.x + self.rod_lenght*math.sin(self.angular_position)
        self.p2_position[1] = self.pin1.y + self.rod_lenght*math.cos(self.angular_position)

        self.pin2.update_pin_position(self.p2_position)


    def get_p2_position(self):
        return self.p2_position


    def print_rod_attributs(self):
        print(self.__dict__)


class bar:
    def __init__(self,lenght, weight, width,colour):
        print("bar")
        # self.bar_vector=pygame.math.Vector2()
        self.bar_lenght=lenght
        self.bar_weight=weight
        self.bar_width=width
        self.bar_colour=colour


class pin:
    def __init__(self,pin_id,position,weight,radius):
        print("pin", pin_id)
        self.pin_vector=pygame.math.Vector2(position)
        self.x=self.pin_vector.x
        self.y=self.pin_vector.y
        self.position=[self.x,self.y]
        self.pin_id=pin_id
        self.pin_weight=weight
        self.pin_radius=radius

    def update_pin_position(self,new_position):
        self.pin_vector.x=new_position[0]
        self.pin_vector.y=new_position[1]
        self.x=self.pin_vector.x
        self.y=self.pin_vector.y
        self.position=[self.x,self.y]