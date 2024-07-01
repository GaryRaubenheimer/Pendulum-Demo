# -Import--------------------------------------------
import sys
import pygame
import math

from colour import *
from constants import *
from Pendulum import *
from Render import *
from Event import *
from Input import *
from Widgets import *


pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED + pygame.RESIZABLE)
pygame.display.set_caption('Pedulum Demo')
# pygame.mouse.set_visible(False)
gui_display = pygame.Surface((WIDTH/4, HEIGHT))
display = pygame.Surface((WIDTH/4*3, HEIGHT))
#gui_display.set_colorkey(RED)    
# Set the current color key for the Surface. When blitting this Surface onto a destination, any pixels that have the same color as the colorkey will be transparent.
window.fill(GREEN)
display.fill(LIGHT_GREY)
gui_display.fill(CYAN)

# -Functions--------------------------------------------

# Function to be called when button is clicked
def button_click():
    print("Button clicked!")

# -Main--------------------------------------------
def main():
    print("Pedulum Demo")
    global window
    global display

    #(x, y, width, height, min_value, max_value, initial_value=, color):
    slider = Slider(50, HEIGHT // 2, WIDTH/4-100,10, 0.5,5,0.5,RED)

    #(x, y, width, height, color, hover_color, text='', font_size=20, text_color=(255, 255, 255), action=None):
    button = Button(50, HEIGHT // 4, 100, 50, BLUE, RED, "Button 1", action=button_click)


    M = Mouse()

    pen_array = []

    pendulum1 = Pendulum(DOUBLE,ORIGIN_POINT)
    pen_array.append(pendulum1)
    pendulum2 = Pendulum(SINGLE,[50,50])
    pen_array.append(pendulum2)

    physics_acc = 0
    running = True
    while running:
        #print("loop")
        
        # update time
        dt = clock.tick(GAME_FRAME_SPEED)
        physics_acc += dt

        # update events
        running ,event_array = pygame_event_buffer(running)
        handle_event_buffer(event_array, M, pen_array,slider,button)
        update_events(M,dt)

        # update input
        M.update(dt)

        # udate physics
        n = 1
        while physics_acc>=GAME_PHYSICS_SPEED:
            for i in range(n):
                for pen in pen_array:
                    pen.update()
            physics_acc-=GAME_PHYSICS_SPEED


        # Update slider
        slider.update()
        # Draw slider
        slider.draw(gui_display)
        button.draw(gui_display)

        
        #update screen
        display, pen_array = draw_rods(display, pen_array, input)
        window.blit(gui_display,(0,0))
        window.blit(display,(WIDTH/4,0))
        pygame.display.flip()
        window.fill(GREEN)
        display.fill(LIGHT_GREY)
        gui_display.fill(CYAN)
        # print(clock.get_fps())

    pygame.quit()
    sys.exit()


if __name__=="__main__":
    main()
