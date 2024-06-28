# Import--------------------------------------------
import math

from constants import *

def update_rods(rods,pen_type):
    # print("update rods")
    if pen_type == SINGLE:
        for rod in rods:
            #calc_trace_points(rod)
            if rod.pin_1.friction!= 1*0.5:
                rod = update_angular_position_SINGLE(rod)
            rod.update()
    elif pen_type == DOUBLE:
        rods =  update_angular_position_DOUBLE(rods)
        rods[0].update()
        rods[1].update()
        pos=rods[0].pin_2.position
        rods[1].pin_1.update_pos(pos)

        # for rod in rods:
        #     #calc_trace_points(rod)
        #     if rod.type == SINGLE:
        #         if rod.pin_1.friction!= 1*0.5:
        #             rod = update_angular_position_SINGLE(rod)
        #         rod.update_pin2_position()
        #     elif rod.type == DOUBLE:
        #         if rod.pin_1.friction!= 1*0.5:
        #            rods =  update_angular_position_DOUBLE(rods)

        #         rods[0].update_pin2_position()
        #         rods[1].update_pin2_position()
        #         pos=rods[0].pin2.position
        #         rods[1].pin1.update_pos(pos)
    return rods


def stabilise_angle(rod):
    if rod.angular_position > math.pi:
        rod.angular_position -= 2 * math.pi 
    elif rod.angular_position < -math.pi:
        rod.angular_position += 2 * math.pi
    return rod 

def stabilise_speed(rod):
    if rod.angular_velocity>SPEED_LIMIT:
        rod.angular_velocity = SPEED_LIMIT
    elif rod.angular_velocity<-SPEED_LIMIT:
        rod.angular_velocity = -SPEED_LIMIT
    return rod

def stabilise_DOUBLE(rods):
    # limit angle and speed for stability
    rods[0] = stabilise_angle(rods[0])
    rods[1] = stabilise_angle(rods[1])
    rods[0] = stabilise_speed(rods[0])
    rods[1] = stabilise_speed(rods[1])    
    return rods

def stabilise_SINGLE(rod):
    rod = stabilise_angle(rod)
    rod = stabilise_speed(rod)
    return rod

def stabilise_small_angle(rod):
    if -0.0005<rod.angular_position/math.pi<0.0005 and -0.00005<rod.angular_velocity/math.pi<0.00005:
       rod.angular_position=0
       rod.angular_velocity=0
    return rod

 
def update_angular_position_DOUBLE(rods):
    t1 = rods[0].angular_position
    t2 = rods[1].angular_position

    w1 = rods[0].angular_velocity
    w2 = rods[1].angular_velocity

    m1 = rods[0].pin_2.weight
    m2 = rods[1].pin_2.weight

    L1 = rods[0].bar.lenght
    L2 = rods[1].bar.lenght

    DAMPING_FACTOR =  1 - rods[0].pin_1.friction 
    g = GRAVITY

    term1 = -g*(2*m1+m2)*math.sin(t1)
    term2 = m2*g*math.sin(t1-2*t2)
    term3 = 2*math.sin(t1-t2)*m2*(w2*w2*L2+w1*w1*L1*math.cos(t1-t2))

    num = term1 - term2 - term3
    denom = L1*(2*m1+m2-m2*math.cos(2*t1-2*t2))
    a1 = num/denom

    term1 = 2*math.sin(t1-t2)
    term2 = w1*w1*L1*(m1+m2)
    term3 = g*(m1+m2)*math.cos(t1)
    term4 = w2*w2*L2*m2*math.cos(t1-t2)

    num = term1*(term2 + term3 + term4)
    denom = L2*(2*m1 + m2 - m2*math.cos(2*t1-2*t2))
    a2 = num/denom
    
    rods[0].angular_velocity += a1
    rods[0].angular_position += rods[0].angular_velocity
    rods[0].angular_velocity *= DAMPING_FACTOR

    rods[1].angular_velocity += a2
    rods[1].angular_position += rods[1].angular_velocity
    rods[1].angular_velocity *= DAMPING_FACTOR

    rods = stabilise_DOUBLE(rods)
    rods[0] = stabilise_small_angle(rods[0])
    rods[1] = stabilise_small_angle(rods[1])

    return rods


def update_angular_position_SINGLE(rod):
    DAMPING_FACTOR =  1 - rod.pin_1.friction 
    theta = rod.angular_position 
    angular_acceleration = -(GRAVITY/rod.bar.lenght)*math.sin(theta)

    rod.angular_velocity += angular_acceleration
    rod.angular_position += rod.angular_velocity
    rod.angular_velocity *= DAMPING_FACTOR

    rod = stabilise_SINGLE(rod)
    rod = stabilise_small_angle(rod)

    return rod

