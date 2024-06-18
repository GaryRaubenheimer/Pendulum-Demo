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