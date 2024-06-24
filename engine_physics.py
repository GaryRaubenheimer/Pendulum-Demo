# Import--------------------------------------------
import sys
import pygame
import math

from Time import *

GRAVITY = 0.3#9.81          # 9.81 m per second^2
DAMPING_FACTOR =  1#0.999   # friction
SPEED_LIMIT = 0.8

"""
FOR SINGLE PENDULUM
FROM: pressbooks.online.ucf.edu/phy2048tjb/chapter/15-4-pendulums

torque = L * net force
torque = -L(m * g * sin(theta))  <-negative because torque is opposite of the movement
torque = inertia * angular_acceleration
inertia = m * L^2   ??
-->
angular_acceleration = -(g/L)sin(theta)

theta small angle approx <15 deg--> sin(theta) = theta
->angular_acceleration = -(g/L) * theta

from Simple harmonic motion --> angular frequency =SQR(g/L)

---

FOR DOUBLE PENDULUM
FROM: web.mit.edu/jorloff/www/chaosTalk/double-pendulum/double-pendulum-en.html

angular position of top rod = t1
angular position of bottom rod = t2

angular velocity of top rod = w1
angular velocity of bottom rod = w2

mass top = m1
mass bottom = m2

lenght top = L1
lenght bottom = l2

angular acceleration of top rod
num= -g(2*m1+m2)sint1 - m2*g*sin(t1-2*t2) - 2sin(t1-t2)*m2*(w2*w2*L2+w1*w1*L1*cos(t1-t2))
denom = L1(2*m1+m2-m2cos(2*t1-2t2))

angular acceleration of bottom rod
num = 2sin(t1-t2)*(w1*w1*L1*(m1+m2) + g(m1+m2)cost1 + w2*w2*L2*m2*cos(t1-t2))
denom = L2*(2*m1 + m2 - m2cos(2*t1-2*t2))


"""

def update_rods(rods):
    # print("update rods")
    if len(rods) == 1:
        rods[0] = update_angular_position_SINGLE(rods[0])
        rods[0].update_p2_position()
    elif len(rods) == 2:
        # print(rods[1].p1_position)
        # rods[1].p1_position=rods[0].p2_position
        
        update_angular_position_DOUBLE(rods)
        rods[0].update_p2_position()
        rods[1].update_p2_position()

        pos=rods[0].pin2.position
        rods[1].pin1.update_pin(pos)

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

  
def update_angular_position_DOUBLE(rods):

    t1 = rods[0].angular_position
    t2 = rods[1].angular_position

    w1 = rods[0].angular_velocity
    w2 = rods[1].angular_velocity

    m1 = rods[0].rod_weight
    m2 = rods[1].rod_weight

    L1 = rods[0].rod_lenght
    L2 = rods[1].rod_lenght

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

    if rods[0].angular_position>(2*math.pi):
        print("error rod[0] > 2*pi: " + str(rods[0].angular_position)+ " " + str(rods[0].angular_velocity))
    if rods[1].angular_position>(2*math.pi):
        print("error rod[1] > 2*pi: " + str(rods[1].angular_position)+" " + str(rods[1].angular_velocity))
    
    if -0.0005<rods[0].angular_position/math.pi<0.0005 and -0.00005<rods[0].angular_velocity/math.pi<0.00005:
        rods[0].angular_position=0
        rods[0].angular_velocity=0
    if -0.0005<rods[1].angular_position/math.pi<0.0005 and -0.00005<rods[1].angular_velocity/math.pi<0.00005:
        rods[1].angular_position=0
        rods[1].angular_velocity=0

    # print(str(rods[1].angular_position/math.pi) + " " +str(rods[1].angular_velocity))
    return rods


def update_angular_position_SINGLE(rod):
    theta = rod.angular_position #- math.pi      # minus - 90deg to het from horizontal
    angular_acceleration = -(GRAVITY/rod.rod_lenght)*math.sin(theta)
    rod.angular_velocity += angular_acceleration

    if -0.0005<rod.angular_position/math.pi<0.0005:
       rod.angular_position=0

    rod.angular_position += rod.angular_velocity
    rod.angular_velocity *= DAMPING_FACTOR

    # print(rod.angular_position/math.pi)

    # limit angle for stability
    rod = stabilise_SINGLE(rod)

    return rod
