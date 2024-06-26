import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mouse Movement Velocity and Angle")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Variables to store mouse positions and velocity
prev_mouse_pos = None
current_mouse_pos = None
velocity = (0, 0)
angle = 0

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the current mouse position
    current_mouse_pos = pygame.mouse.get_pos()
    
    # Calculate velocity if we have a previous mouse position
    if prev_mouse_pos is not None:
        delta_x = current_mouse_pos[0] - prev_mouse_pos[0]
        delta_y = current_mouse_pos[1] - prev_mouse_pos[1]
        velocity = (delta_x, delta_y)
        print(math.degrees(math.atan2(delta_x, delta_y)))
        # Calculate the angle with respect to the vertical axis (y-axis)
        #if delta_y != 0:
        angle = 180 - math.degrees(math.atan2(delta_x, delta_y))
        #else:
        #    angle = 90 if delta_x > 0 else 270
        if delta_y == 0 and delta_x == 0:
            angle =0
        else:
            angle = 180 - math.degrees(math.atan2(delta_x, delta_y))

    # Store the current mouse position as the previous position for the next frame
    prev_mouse_pos = current_mouse_pos

    # Clear the screen
    screen.fill(WHITE)

    # Display the velocity and angle
    font = pygame.font.Font(None, 36)
    text_velocity = font.render(f"Velocity: {velocity}", True, BLACK)
    text_angle = font.render(f"Angle: {angle:.2f} degrees", True, BLACK)
    screen.blit(text_velocity, (20, 20))
    screen.blit(text_angle, (20, 60))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()

'''

import pygame
import math

# Constants
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FPS = 60

# Pendulum parameters
L1 = 100  # Length of the first rod
L2 = 100  # Length of the second rod
M1 = 10   # Mass of the first pendulum
M2 = 10   # Mass of the second pendulum
G = 9.81  # Acceleration due to gravity

# Initial angles
a1 = math.pi / 2
a2 = math.pi / 2
a1_v = 0  # Angular velocity of the first pendulum
a2_v = 0  # Angular velocity of the second pendulum

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Simulation loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Equations of motion for the double pendulum
    num1 = -G * (2 * M1 + M2) * math.sin(a1)
    num2 = -M2 * G * math.sin(a1 - 2 * a2)
    num3 = -2 * math.sin(a1 - a2) * M2
    num4 = a2_v ** 2 * L2 + a1_v ** 2 * L1 * math.cos(a1 - a2)
    denom = L1 * (2 * M1 + M2 - M2 * math.cos(2 * a1 - 2 * a2))
    a1_a = (num1 + num2 + num3 * num4) / denom

    num1 = 2 * math.sin(a1 - a2)
    num2 = (a1_v ** 2 * L1 * (M1 + M2) + G * (M1 + M2) * math.cos(a1) + a2_v ** 2 * L2 * M2 * math.cos(a1 - a2))
    denom = L2 * (2 * M1 + M2 - M2 * math.cos(2 * a1 - 2 * a2))
    a2_a = (num1 * num2) / denom

    # Update velocities and angles
    a1_v += a1_a
    a2_v += a2_a
    a1 += a1_v
    a2 += a2_v

    # Damping
    a1_v *= 0.99
    a2_v *= 0.99

    # Positions of the pendulums
    x1 = WIDTH // 2 + L1 * math.sin(a1)
    y1 = HEIGHT // 2 + L1 * math.cos(a1)
    x2 = x1 + L2 * math.sin(a2)
    y2 = y1 + L2 * math.cos(a2)

    # Drawing
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, (WIDTH // 2, HEIGHT // 2), (x1, y1), 2)
    pygame.draw.line(screen, WHITE, (x1, y1), (x2, y2), 2)
    pygame.draw.circle(screen, WHITE, (int(x1), int(y1)), M1)
    pygame.draw.circle(screen, WHITE, (int(x2), int(y2)), M2)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

'''

'''

import pygame
import math
 
pygame.init()
 
# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotating Object")
 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
 
# Object properties
rod_length = 100
rod_thickness = 10
pivot_radius = 5
 
# Initial position of the rod
rod_x, rod_y = WIDTH // 2, HEIGHT // 2
 
# Initial angle of rotation
angle = 0
 
# Function to rotate a point around another point
def rotate_point(point, pivot, angle):
    """ Rotate a point around a pivot point by a given angle (in radians) """
    px, py = pivot
    x, y = point
    rotated_x = px + math.cos(angle) * (x - px) - math.sin(angle) * (y - py)
    rotated_y = py + math.sin(angle) * (x - px) + math.cos(angle) * (y - py)
    return (rotated_x, rotated_y)
 
# Game loop
running = True
dragging = False
pivot_point = (0, 0)  # Pivot point where the object is clicked
 
while running:
    screen.fill(WHITE)
 
    # Draw pivot point
    pygame.draw.circle(screen, BLACK, pivot_point, pivot_radius)
 
    # Calculate rod endpoints
    rod_end_x = rod_x + rod_length * math.cos(angle)
    rod_end_y = rod_y + rod_length * math.sin(angle)
 
    # Draw rod
    pygame.draw.line(screen, RED, (rod_x, rod_y), (rod_end_x, rod_end_y), rod_thickness)
 
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = event.pos
                dist_to_pivot = math.sqrt((mouse_x - rod_x) ** 2 + (mouse_y - rod_y) ** 2)
                if dist_to_pivot <= rod_length / 2:
                    dragging = True
                    pivot_point = (mouse_x, mouse_y)
                    dx = mouse_x - rod_x
                    dy = mouse_y - rod_y
                    angle = math.atan2(dy, dx)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_x, mouse_y = event.pos
                dx = mouse_x - rod_x
                dy = mouse_y - rod_y
                angle = math.atan2(dy, dx)
 
    # Update rod endpoint based on angle
    rod_end_x = rod_x + rod_length * math.cos(angle)
    rod_end_y = rod_y + rod_length * math.sin(angle)
 
    # Draw updated rod
    pygame.draw.line(screen, RED, (rod_x, rod_y), (rod_end_x, rod_end_y), rod_thickness)
 
    pygame.display.flip()
 
pygame.quit()

'''

'''
import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Vector of Bar Example")

# Define the positions of the points (vectors)
p1 = pygame.math.Vector2(100, 100)
p2 = pygame.math.Vector2(300, 200)

# Calculate the vector representing the bar connecting them
v = p2 - p1

# Print the vector for demonstration
print(f"Vector representing the bar: {v}")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), p1, 5)  # Red circle for p1
    pygame.draw.circle(screen, (0, 0, 255), p2, 5)  # Blue circle for p2
    pygame.draw.line(screen, (0, 0, 0), p1, p2, 2)  # Black line for the bar

    pygame.display.flip()

pygame.quit()
sys.exit()




"""
loop_check=0
        global loop_check
        if loop_check in range(1000):
            loop_check+=1
        else:
            loop_check = 0
        print(loop_check)
"""

'''

