import math

from constants import *

FRICTION_COEFFICIENT = 1

def update_rods(rods, isSplit, pen_type):
    """
    Update the state of the rods based on their type (single or double pendulum) and split status.
    """
    if pen_type == SINGLE:
        for rod in rods:
            if rod.pin_1.friction != FRICTION_COEFFICIENT:
                rod = update_angular_position_SINGLE(rod)
            rod.update()
    elif pen_type == DOUBLE:
        if not isSplit:
            rods = update_angular_position_DOUBLE(rods)
            rods[0].update()
            rods[1].update()
            pos = rods[0].pin_2.position
            rods[1].pin_1.update_pos(pos)
        else:
            for rod in rods:
                if rod.type == SINGLE:
                    if rod.pin_1.friction != FRICTION_COEFFICIENT:
                        rod = update_angular_position_SINGLE(rod)
                    rod.update()
    return rods

def stabilise_angle(rod):
    """
    Normalize the angular position of the rod to be within -pi to pi.
    """
    if rod.angular_position > math.pi:
        rod.angular_position -= 2 * math.pi
    elif rod.angular_position < -math.pi:
        rod.angular_position += 2 * math.pi
    return rod 

def stabilise_speed(rod):
    """
    Limit the angular velocity of the rod to a predefined speed limit for stability.
    """
    rod.angular_velocity = max(min(rod.angular_velocity, SPEED_LIMIT), -SPEED_LIMIT)
    return rod

def stabilise_DOUBLE(rods):
    """
    Apply angle and speed stabilization to both rods in a double pendulum.
    """
    for rod in rods:
        rod = stabilise_angle(rod)
        rod = stabilise_speed(rod)
    return rods

def stabilise_SINGLE(rod):
    """
    Apply angle and speed stabilization to a single rod.
    """
    rod = stabilise_angle(rod)
    rod = stabilise_speed(rod)
    return rod

def stabilise_small_angle(rod):
    """
    Set angular position and velocity to zero if they are very small, to prevent unnecessary oscillations.
    """
    if -0.0005 < rod.angular_position / math.pi < 0.0005 and -0.00005 < rod.angular_velocity / math.pi < 0.00005:
        rod.angular_position = 0
        rod.angular_velocity = 0
    return rod

def update_angular_position_DOUBLE(rods):
    """
    Calculate the new angular positions and velocities for double pendulums.
    """
    t1, t2 = rods[0].angular_position, rods[1].angular_position
    w1, w2 = rods[0].angular_velocity, rods[1].angular_velocity
    m1, m2 = rods[0].pin_2.weight, rods[1].pin_2.weight
    L1, L2 = rods[0].bar.length, rods[1].bar.length
    g  = GRAVITY
    DAMPING_FACTOR_1 = 1 - rods[0].pin_1.friction
    DAMPING_FACTOR_2 = 1 - rods[1].pin_1.friction

    term1 = -g * (2 * m1 + m2) * math.sin(t1)
    term2 = m2 * g * math.sin(t1 - 2 * t2)
    term3 = 2 * math.sin(t1 - t2) * m2 * (w2 ** 2 * L2 + w1 ** 2 * L1 * math.cos(t1 - t2))
    a1 = (term1 - term2 - term3) / (L1 * (2 * m1 + m2 - m2 * math.cos(2 * t1 - 2 * t2)))

    term1 = 2 * math.sin(t1 - t2)
    term2 = w1 ** 2 * L1 * (m1 + m2)
    term3 = g * (m1 + m2) * math.cos(t1)
    term4 = w2 ** 2 * L2 * m2 * math.cos(t1 - t2)
    a2 = (term1 * (term2 + term3 + term4)) / (L2 * (2 * m1 + m2 - m2 * math.cos(2 * t1 - 2 * t2)))

    rods[0].angular_velocity += a1
    rods[0].angular_position += rods[0].angular_velocity
    rods[0].angular_velocity *= DAMPING_FACTOR_1
    if rods[0].pin_1.friction == FRICTION_COEFFICIENT:
        rods[0].angular_position -= rods[0].angular_velocity

    rods[1].angular_velocity += a2
    rods[1].angular_position += rods[1].angular_velocity
    rods[1].angular_velocity *= DAMPING_FACTOR_2
    if rods[1].pin_1.friction == FRICTION_COEFFICIENT:
        rods[1].angular_position -= rods[0].angular_velocity

    rods = stabilise_DOUBLE(rods)
    rods[0] = stabilise_small_angle(rods[0])
    rods[1] = stabilise_small_angle(rods[1])

    return rods

def update_angular_position_SINGLE(rod):
    """
    Calculate the new angular position and velocity for a single pendulum.
    """
    DAMPING_FACTOR = 1 - rod.pin_1.friction
    theta = rod.angular_position
    angular_acceleration = -(GRAVITY / rod.bar.length) * math.sin(theta)

    rod.angular_velocity += angular_acceleration
    rod.angular_position += rod.angular_velocity
    rod.angular_velocity *= DAMPING_FACTOR

    rod = stabilise_SINGLE(rod)
    rod = stabilise_small_angle(rod)

    return rod
