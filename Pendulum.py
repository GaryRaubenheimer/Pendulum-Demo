import math
import colour 

from game_context import get_pygame
from constants import *
from Physics import *

# Get pygame instance from game context
pygame = get_pygame()

# Constants
PIN2_WEIGHT_SINGLE = 5
PIN2_RADIUS_SINGLE = 15
BAR_LENGTH_SINGLE = 100
BAR_WIDTH = 3
BAR_COLOUR = colour.BLACK
ANGULAR_POSITION_SINGLE = math.pi / 3

PIN2_WEIGHT_DOUBLE = 1
ANGULAR_POSITION_DOUBLE = math.pi

TRACE_POINTS_LENGTH = 50

class Pendulum:   
    def __init__(self, type, origin_pos, trace_colour,isRainbow = False):
        self.type = type
        self.origin_pos = origin_pos
        self.trace_points_colour = trace_colour
        self.isRainbow = isRainbow
        rods_info = self.create_rod_info()
        self.rods = self.create_rod_array(rods_info,self.trace_points_colour)
        self.isSplit = False
        self.isSelected = False

    def get_info(self):
        info_list = []
        info_list.append(self.type)
        for rod in self.rods:
            info_list.append(rod.get_info())
        return info_list

    def create_rod_info(self):
        rods_info = []
        friction = 0.0

        if self.type == SINGLE:
            rods_info.append(self._create_single_rod_info(friction))
        elif self.type == DOUBLE:
            rods_info.append(self._create_single_rod_info(friction))
            rods_info.append(self._create_double_rod_info(friction, rods_info[0]))

        return rods_info

    def _create_single_rod_info(self, friction_coefficient):
        pins_info = [PIN2_WEIGHT_SINGLE, PIN2_RADIUS_SINGLE, [colour.GREY, colour.RED], friction_coefficient, self.origin_pos]
        bar_info = [0, BAR_LENGTH_SINGLE, BAR_WIDTH, BAR_COLOUR]
        return [pins_info, bar_info, ANGULAR_POSITION_SINGLE]

    def _create_double_rod_info(self, friction_coefficient, first_rod_info):
        pins_info = [PIN2_WEIGHT_DOUBLE, PIN2_RADIUS_SINGLE, [colour.GREY, colour.RED], friction_coefficient, self._calculate_pin_position(first_rod_info)]
        bar_info = [0, BAR_LENGTH_SINGLE, BAR_WIDTH, BAR_COLOUR]
        return [pins_info, bar_info, ANGULAR_POSITION_DOUBLE]

    def _calculate_pin_position(self, rod_info):
        pin_position = [0, 0]
        pin_position[0] = rod_info[0][4][0] + rod_info[1][1] * math.sin(rod_info[2])
        pin_position[1] = rod_info[0][4][1] + rod_info[1][1] * math.cos(rod_info[2])
        return pin_position

    def create_rod_array(self, rods_info,trace_points_colour):
        rods = []
        for rod_id, rod_info in enumerate(rods_info, start=1):
            rods.append(Rod(rod_id, self.isRainbow,self.type,trace_points_colour, *rod_info))
        return rods

    def split(self):
        for rod in self.rods:
            rod.type = SINGLE
        self.isSplit = True

    def unsplit(self):
        for rod in self.rods:
            rod.type = DOUBLE
        self.isSplit = False

    def update(self):
        self.rods = update_rods(self.rods, self.isSplit, self.type)

#--

class Rod:
    def __init__(self, rod_id, isRainbow,type, trace_points_colour, pins_info, bar_info, angular_position):
        self.angular_position = angular_position
        self.angular_velocity = 0
        self.rod_id = rod_id
        self.type = type
        self.pin_1 = Pin(1,rod_id,isRainbow, pins_info[4], 0, 5, pins_info[2][0],trace_points_colour, pins_info[3])
        self.pin_2 = Pin(2, rod_id,isRainbow,self._create_pin2_position(pins_info[4], bar_info[1]), pins_info[0], pins_info[1], pins_info[2][1],trace_points_colour, pin_friction=0)
        self.bar = Bar(*bar_info)

    def get_info(self):
        return [
            self.pin_1.friction,
            self.bar.length,
            self.pin_2.weight,
            self.pin_2.radius,
            self.pin_2.trace_points_isOn,
            self.pin_2.trace_points_isLine]

    def _create_pin2_position(self, pin1_position, bar_length):
        return [pin1_position[0] + bar_length * math.sin(self.angular_position),
                pin1_position[1] + bar_length * math.cos(self.angular_position)]

    def update(self):
        p2_position = self._create_pin2_position(self.pin_1.position, self.bar.length)
        self.pin_2.update_pos(p2_position)

#--

class Bar:
    def __init__(self, weight, length, width, colour):
        self.length = length
        self.weight = weight
        self.width = width
        self.colour = colour

    def update(self):
        #print("update bar")
        pass

    def change_length(self,length):
        self.length = length

#--

class Pin:
    def __init__(self, pin_id, rod_id,isRainbow ,position, weight, radius, colour, trace_pcolour=None, pin_friction=None):
        self.pin_vector = pygame.math.Vector2(position)
        self.x = self.pin_vector.x
        self.y = self.pin_vector.y
        self.position = [self.x, self.y]
        self.pin_id = pin_id
        self.rod_id = rod_id
        self.weight = weight
        self.radius = radius
        self.colour = colour
        self.friction = pin_friction 
        self.trace_points = []
        self.trace_points_length = TRACE_POINTS_LENGTH
        self.trace_points_colour = trace_pcolour
        self.trace_points_isLine = True
        self.trace_points_isOn = True
        self.isRainbow = isRainbow
        self.RAINBOW_step_direction = 0

    def update_pos(self, new_pos):
        self.pin_vector.update(new_pos[0], new_pos[1])
        self.x = self.pin_vector.x
        self.y = self.pin_vector.y
        self.position = [self.x, self.y]
        if self.pin_id == 2:
            self.calc_trace_points()
            if self.isRainbow :
                newColour,self.RAINBOW_step_direction = colour.changeRAINBOW(self.trace_points_colour,self.RAINBOW_step_direction)
                self.trace_points_colour = newColour

    def calc_trace_points(self):
        if len(self.trace_points) < self.trace_points_length:
            self.trace_points.append(self.position[:])
        else:
            self.trace_points.pop(0)

    def change_friction(self,friction):
        self.friction = friction

    def change_weight(self,weight):
        self.weight = weight

    def change_radius(self,radius):
        self.radius = radius

    def change_trace_points(self):
        pass
