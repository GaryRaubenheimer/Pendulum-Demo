import random

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
DARK_GREEN = (0,200,0)
BLUE = (0,0,255)
LIGHT_BLUE = (0,0,150)
GREY = (100,100,100)
LIGHT_GREY = (200,200,200)
DARK_GREY = (150, 150, 150)
CYAN = (0,255,255)
LIGHT_CYAN = (0,150,150)
YELLOW = (255,255,0)
DARK_YELLOW = (200,200,0)
PURPLE = (255,0,255)

RAINBOW = [255, 0, 0]  # Start with red
RAINBOW_step_direction = 0  # 0: Red -> Yellow, 1: Yellow -> Green, 2: Green -> Cyan, etc.

def changeRAINBOW(RAINBOW,RAINBOW_step_direction):
    step_value = 5  # Adjust the step size for smoothness or speed

    if RAINBOW_step_direction == 0:  # Red -> Yellow
        RAINBOW[1] += step_value
        if RAINBOW[1] >= 255:
            RAINBOW[1] = 255
            RAINBOW_step_direction = 1
    elif RAINBOW_step_direction == 1:  # Yellow -> Green
        RAINBOW[0] -= step_value
        if RAINBOW[0] <= 0:
            RAINBOW[0] = 0
            RAINBOW_step_direction = 2
    elif RAINBOW_step_direction == 2:  # Green -> Cyan
        RAINBOW[2] += step_value
        if RAINBOW[2] >= 255:
            RAINBOW[2] = 255
            RAINBOW_step_direction = 3
    elif RAINBOW_step_direction == 3:  # Cyan -> Blue
        RAINBOW[1] -= step_value
        if RAINBOW[1] <= 0:
            RAINBOW[1] = 0
            RAINBOW_step_direction = 4
    elif RAINBOW_step_direction == 4:  # Blue -> Magenta
        RAINBOW[0] += step_value
        if RAINBOW[0] >= 255:
            RAINBOW[0] = 255
            RAINBOW_step_direction = 5
    elif RAINBOW_step_direction == 5:  # Magenta -> Red
        RAINBOW[2] -= step_value
        if RAINBOW[2] <= 0:
            RAINBOW[2] = 0
            RAINBOW_step_direction = 0

    # Ensure values stay in the valid range
    RAINBOW = [max(0, min(255, x)) for x in RAINBOW]
    return RAINBOW,RAINBOW_step_direction


def get_RANDOM_COLOUR():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

RANDOM_COLOUR = get_RANDOM_COLOUR()
