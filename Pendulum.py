# -Import--------------------------------------------
import pygame
import math

from colour import *
from constants import *
from Physics import *

# -Classes--------------------------------------------
class Pendulum:   
    def __init__(self,type,origin_pos):
        # print("make pendulum")
        self.type=type
        self.origin_pos = origin_pos

        rods_info = self.create_rod_info()
        self.rods = self.create_rod_array(rods_info)


    def create_rod_info(self):
        rods_info = []
        friction = 0.0
        friction_coeficient = friction * 0.5
        
        if self.type == SINGLE:
            #rod 1
            pin2_weight = 5
            pin2_radius = 15
            pins_colour = [GREY,RED]
            pin1_friction = friction_coeficient
            pin1_position = self.origin_pos
            pins_info = [pin2_weight,pin2_radius,pins_colour,pin1_friction,pin1_position]

            bar_weight = 0
            bar_lenght = 100
            bar_width = 3
            bar_colour = BLACK
            bar_info = [bar_weight,bar_lenght,bar_width,bar_colour]
            angular_positions = math.pi/3

            list = [pins_info,bar_info,angular_positions]
            rods_info.append(list)
        elif self.type == DOUBLE:
            #rod 1
            pin2_weight = 5
            pin2_radius = 15
            pins_colour = [GREY,RED]
            pin1_friction = friction_coeficient
            pin1_position = self.origin_pos
            pin1_info = [pin2_weight,pin2_radius,pins_colour,pin1_friction,pin1_position]

            bar_weight = 0
            bar_lenght = 100
            bar_width = 3
            bar_colour = BLACK
            bar_info = [bar_weight,bar_lenght,bar_width,bar_colour]
            angular_positions = math.pi/3
            list1 = [pin1_info,bar_info,angular_positions]
            rods_info.append(list1)

            #rod 2
            pin2_weight = 1
            pin2_radius = 5
            pins_colour = [GREY,RED]
            pin1_friction = friction_coeficient

            bar_weight = 0
            bar_lenght = 100
            bar_width = 3
            bar_colour = BLACK
            bar_info = [bar_weight,bar_lenght,bar_width,bar_colour]
            angular_positions = math.pi

            pin = [0,0]
            pin[0] = rods_info[0][0][4][0] + bar_info[1]*math.sin(rods_info[0][2])
            pin[1] = rods_info[0][0][4][1] + bar_info[1]*math.cos(rods_info[0][2])
            pin2_info = [pin2_weight,pin2_radius,pins_colour,pin1_friction,pin]

            list2 = [pin2_info,bar_info,angular_positions]
            rods_info.append(list2)

        return rods_info

    def create_rod_array(self,rods_info):
        #print("create rod array")
        rods = []
        if self.type == SINGLE:
            pins_info = rods_info[0][0]
            bar_info = rods_info[0][1]
            angular_position = rods_info[0][2]
            rod1 = Rod(1,self.type,pins_info,bar_info,angular_position)
            rods.append(rod1)
        elif self.type == DOUBLE:
            pins_info = rods_info[0][0]
            bar_info = rods_info[0][1]
            angular_position = rods_info[0][2]
            rod1 = Rod(1,self.type,pins_info,bar_info,angular_position)
            rods.append(rod1)

            pins_info = rods_info[1][0]
            bar_info = rods_info[1][1]
            angular_position = rods_info[1][2]
            rod2 = Rod(2,self.type,pins_info,bar_info,angular_position)
            rods.append(rod2)
        return rods

    def split(self):
        self.rods[0].type = SINGLE
        self.rods[1].type = SINGLE

    def unsplit(self):
        self.rods[0].type = DOUBLE
        self.rods[1].type = DOUBLE

    def update(self):
        self.rods = update_rods(self.rods,self.type)

    

#---
class Rod(Pendulum):   
    def __init__(self,rod_id,type,pins_info,bar_info,angular_position):
        # print("make rod")

        self.angular_position = angular_position
        self.angular_velocity = 0
        self.rod_id = rod_id
        self.type = type

        pin2_weight = pins_info[0]
        pin2_radius = pins_info[1]
        pins_colour = pins_info[2]
        pin1_friction = pins_info[3]
        pin1_position = pins_info[4]

        bar_weight = bar_info[0]
        bar_lenght = bar_info[1]
        bar_width = bar_info[2]
        bar_colour = bar_info[3]

        self.bar = Bar(bar_weight,bar_lenght,bar_width,bar_colour)

        self.pin_1 = Pin(1,pin1_position,0,5,pins_colour[0],pin1_friction)
        pin2_position = self.create_pin2_position(self.bar.lenght)
        self.pin_2 = Pin(2,pin2_position,pin2_weight,pin2_radius,pins_colour[1],0)


    def create_pin2_position(self,lenght):
        p2_position = [0,0]
        p2_position[0] = self.pin_1.x + lenght*math.sin(self.angular_position)
        p2_position[1] = self.pin_1.y + lenght*math.cos(self.angular_position)
        return p2_position

    def update(self):
        # print("update position")
        p2_position = [0,0]
        p2_position[0] = self.pin_1.x + self.bar.lenght*math.sin(self.angular_position)
        p2_position[1] = self.pin_1.y + self.bar.lenght*math.cos(self.angular_position)
        self.pin_2.update_pos(p2_position)

#---
class Bar(Rod):   
    def __init__(self,weight,lenght,width,colour):
        #print("make bar")
        self.lenght=lenght
        self.weight=weight
        self.width=width
        self.colour=colour

    def update(self):
        print("update bar")

#---
class Pin(Rod):
    def __init__(self,pin_id,position,weight,radius,colour,pin_friction = None):
        # print("make pin")
        self.pin_vector=pygame.math.Vector2(position)
        self.x=self.pin_vector.x
        self.y=self.pin_vector.y
        self.position=[self.x,self.y]
        # self.speed=self.pin_vector.magnitude()

        self.pin_id=pin_id
        self.weight=weight
        self.radius=radius
        self.colour=colour
        
        if pin_id == 1:
            self.friction = pin_friction
        self.trace_points = []
        self.trace_points_lenght = 50
        self.trace_points_colour = GREEN

    def update_pos(self,new_pos):
        # print("update pin pos")
        self.pin_vector.update(new_pos[0],new_pos[1])
        self.x=self.pin_vector.x
        self.y=self.pin_vector.y
        self.position=[self.x,self.y]

