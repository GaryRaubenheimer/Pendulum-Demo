# Import--------------------------------------------
import sys
import pygame
import math
import time


# Initialise global variable------------------------
pygame.init()

WIDTH,HEIGHT = 800,600

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('n-ple pedulum')
clock = pygame.time.Clock()

GAME_SPEED = 60         # 60 updates per second
GRAVITY = 0.1          # 9.81 m per second^2
DAMPING_FACTOR = 0.99   # friction

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

BAR_WIDTH = 5
TRACE_POINT_LENGHT = 50

ORIGIN_POINT = [WIDTH/2, HEIGHT/3]

#Classes--------------------------------------------
class Bar:   
    
    p1_position = [0,0]
    trace_points = []

    def __init__(self, p1_position, lenght, weight, angular_position, colour =(100,100,100)):
        self.p1_position = p1_position
        self.lenght = lenght
        self.weight = weight
        self.angular_position = angular_position
        self.angular_velocity = 0
        self.angular_accaleration = 0
        self.colour = colour
        self.angular_momentum = 0
        self.moment_of_inertia = (1/3)*self.weight*self.lenght**2
    

    def update_angular_position(self):
        torque = -self.weight*GRAVITY*self.lenght*math.sin(self.angular_position)
        self.angular_accaleration = torque/self.moment_of_inertia
    
        self.angular_velocity += self.angular_accaleration
        self.angular_position += self.angular_velocity

        self.angular_velocity *= DAMPING_FACTOR

        # limit angle for stability
        if self.angular_position>(2*math.pi):
            self.angular_position = self.angular_position - (2*math.pi)
        elif self.angular_position<(-2*math.pi):
            self.angular_position = self.angular_position + (2*math.pi)

        print(self.get_p2_position())

    def get_p2_position(self):
        p2_position = [0,0]
        p2_position[0] = self.p1_position[0] + self.lenght*math.sin(self.angular_position)
        p2_position[1] = self.p1_position[1] + self.lenght*math.cos(self.angular_position)
        return p2_position
    
    def print_bar_attributs(self):
        print(self.__dict__)


# Functions--------------------------------------------
def create_bar_array(number_of_bars): 
    # print("create bars") 
    
    # initialise values per bar
    p1_pos = [0,0]
    lenght = 100
    weight = 5
    angular_position = 0
    
    bars=[]
    
    for i in range(number_of_bars):
        if i == 0:
            p1_pos = [0,0]
            lenght = 100
            weight = 100
            angular_position = math.pi
            colour = BLACK
            bars.append(Bar(p1_pos, lenght, weight, angular_position, colour))
            continue

        p1_pos = bars[i-1].p2_posistion[1]
        colour = (100,100,100)

        bars.append(Bar(p1_pos, lenght, weight, angular_position, colour))
    
    return bars


def update_bars(bars):
    # print("update bar")
    for bar in bars:
        bar.update_angular_position()
    return bars


def draw_bar(b):
    # print("draw bar")
    p2_position = b.get_p2_position()
    p1_from_ORIGIN = [b.p1_position[0] + ORIGIN_POINT[0], 
                      b.p1_position[1] + ORIGIN_POINT[1]]
    p2_from_ORIGIN = [p2_position[0] + ORIGIN_POINT[0], 
                      p2_position[1] + ORIGIN_POINT[1]]

    # draw line
    pygame.draw.line(screen, b.colour, p1_from_ORIGIN, p2_from_ORIGIN, BAR_WIDTH)
    
    # draw begin point
    pygame.draw.circle(screen, RED, p1_from_ORIGIN, BAR_WIDTH)

    # draw trace points
    if len(b.trace_points)<TRACE_POINT_LENGHT:
        b.trace_points.append(p2_from_ORIGIN)
    else:
        b.trace_points.pop(0)

    for i in range(len(b.trace_points)):
        pygame.draw.circle(screen, GREEN, b.trace_points[i], 1)
    
    # draw end point
    pygame.draw.circle(screen, RED, p2_from_ORIGIN, BAR_WIDTH)
    

def get_mouse_speed(prev_x, prev_y, prev_time):
    curr_mouse_x, curr_mouse_y = pygame.mouse.get_pos()
    dx = curr_mouse_x - prev_x
    dy = curr_mouse_y - prev_y

    # print (curr_mouse_x, prev_x , dx)
    
    distance = (dx**2 + dy**2)**0.5

    curr_time = time.time()
    elapsed_time = curr_time - prev_time

    if elapsed_time > 0:                # divide by zero error
        speed = distance/elapsed_time
        dx_speed = dx/elapsed_time
        dy_speed = dy/elapsed_time
    else:
        speed = 0
        dx_speed = 0
        dy_speed = 0

    prev_time = curr_time

    # print(f"mouse speed : {speed} pixels/second")
    # print(f"mouse dx speed : {dx_speed} pixels/second")
    # print(f"mouse dy speed : {dy_speed} pixels/second")
    # print("----------")
    # print (curr_mouse_x, prev_x , dx)
    # print("------")


# Main--------------------------------------------
def main():
    print("n-ple pedulum")

    bars = create_bar_array(1)

    running = True

    mouse_x = 0
    mouse_y = 0
    is_button_held = False
    is_p1_clicked = False
    is_p2_clicked = False
    
    prev_mouse_x, prev_mouse_y = pygame.mouse.get_pos()
    curr_mouse_x = 0 
    curr_mouse_y = 0
    prev_time = time.time()

    while running:
        screen.fill(WHITE)

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # check if left button is pressed
                if event.button == 1:
                    is_button_held = True
                    mouse_x, mouse_y = event.pos
                    # print(f"mouse held at ({mouse_x},{mouse_y})")

                    # Check if clicked on p1
                    p1_position = bars[0].p1_position
                    p1_from_ORIGIN = [p1_position[0] + ORIGIN_POINT[0], 
                                      p1_position[1] + ORIGIN_POINT[1]]
                    
                    upper_bound_x = p1_from_ORIGIN[0] + BAR_WIDTH
                    lower_bound_x = p1_from_ORIGIN[0] - BAR_WIDTH
                    upper_bound_y = p1_from_ORIGIN[1] + BAR_WIDTH
                    lower_bound_y = p1_from_ORIGIN[1] - BAR_WIDTH

                    if   lower_bound_x <= mouse_x <= upper_bound_x:
                        if  lower_bound_y <= mouse_y <= upper_bound_y:
                            is_p1_clicked = True
                            # print(f"mouse held at ({mouse_x},{mouse_y})")

                    # Check if clicked on p2
                    p2_position = bars[0].get_p2_position()
                    p2_from_ORIGIN = [p2_position[0] + ORIGIN_POINT[0], 
                                      p2_position[1] + ORIGIN_POINT[1]]
                    
                    upper_bound_x = p2_from_ORIGIN[0] + BAR_WIDTH
                    lower_bound_x = p2_from_ORIGIN[0] - BAR_WIDTH
                    upper_bound_y = p2_from_ORIGIN[1] + BAR_WIDTH
                    lower_bound_y = p2_from_ORIGIN[1] - BAR_WIDTH

                    if   lower_bound_x <= mouse_x <= upper_bound_x:
                        if  lower_bound_y <= mouse_y <= upper_bound_y:
                            is_p2_clicked = True
                            # print(f"mouse held at ({mouse_x},{mouse_y})")

                    
            elif event.type == pygame.MOUSEBUTTONUP:
                # check if left button is release
                if event.button == 1:
                    is_button_held = False
                    mouse_x, mouse_y = event.pos
                    # print(f"mouse released at ({mouse_x},{mouse_y})")

                    # release p1 if held
                    if is_p1_clicked:
                        is_p1_clicked = False
                        # print("release p1")

                    # release p2 if held
                    if is_p2_clicked:
                        is_p2_clicked = False
                        # print("release p2")


        if is_button_held:
            # perform action when held
            if is_p1_clicked:
                # print("Holding p1")
                mouse_x, mouse_y = pygame.mouse.get_pos()

                bars[0].p1_position[0] = mouse_x -WIDTH/2
                bars[0].p1_position[1] = mouse_y -HEIGHT/3

            elif is_p2_clicked:
                # print("Holding p2")

                mouse_x, mouse_y = pygame.mouse.get_pos()

                p1 = bars[0].p1_position

                p1_from_ORIGIN = [p1[0] + ORIGIN_POINT[0], 
                                  p1[1] + ORIGIN_POINT[1]]

                p2 = [mouse_x, mouse_y]
                dx = p2[0]-p1_from_ORIGIN[0]
                dy = p2[1]-p1_from_ORIGIN[1]

                angle = math.atan2(dx, dy)
                angle_with_vertical =  angle

                # bars[0].angular_acceleration = 0
                # bars[0].angular_velocity = 0
                bars[0].angular_position = angle_with_vertical
            pass


        # draw graphics
        for bar in bars:
            draw_bar(bar)


        # update game
        bars = update_bars(bars)

        

        get_mouse_speed(prev_mouse_x, prev_mouse_y, prev_time)
        curr_mouse_x, curr_mouse_y = pygame.mouse.get_pos()
        prev_mouse_x = curr_mouse_x
        prev_mouse_y = curr_mouse_y

        # update the display
        pygame.display.flip()
        clock.tick(GAME_SPEED)   

    pygame.quit()
    sys.exit()


if __name__=="__main__":
    main()

