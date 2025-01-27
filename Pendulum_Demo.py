import sys
import pygame

"""
todo:
clean up code and add comments

DONE move sidebar menu widgets up 
DONE add speed lables
DONE add instruction labels

DONE move edit menu widgets up 
DONE line tacepoint activate when activate edit again

DONE add about menu with details
DONE add start background

DONE make friction less harsh

"""

#  in python module  imports create seperate instances of global varialbles
import constants
import colour 
import Gui 

# _this below is bad practice_
# from constants import *
from Pendulum import *
from Render import *
from Event import *
from Input import *
from Widgets import *
# from Gui import *

# initiate pygame window and clock
pygame.init()
pygame.display.set_caption('Pendulum Demo')
clock = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED + pygame.RESIZABLE)

# create pygame surfaces - surfaces act as background
simulation_display = pygame.Surface((WIDTH/4*3, HEIGHT))
startMenu_display = pygame.Surface((WIDTH, HEIGHT))
startMenu_display.fill(RED)
#about_display = pygame.Surface((WIDTH, HEIGHT))
#about_display.fill(YELLOW)
#error_display = pygame.Surface((WIDTH, HEIGHT))
#error_display.fill(BLUE)

#window.blit(error_display, (0, 0))
window.fill(DARK_GREEN) # DARK_GREEN Screen means that display could not be displayed

draw_accuracy = 0 # simulated frames counter
physics_accuracy = 0 # speed of simulation counter

def draw_gradient(surface, color1, color2):
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))
    return surface

def draw_background_pattern(surface):
    center_x = WIDTH * 3 // 8  # Center in the first 3/4 of the width
    center_y = HEIGHT // 2
    max_radius = min(WIDTH, HEIGHT) // 3

    for i in range(10):
        radius = max_radius - (i * (max_radius // 10))
        color = (180 - i * 20, 220 - i * 20, 255 - i * 25)  # Light colors
        pygame.draw.circle(surface, color, (center_x, center_y), radius, width=3)
    return surface
    
def main():
    global window, startMenu_display, simulation_display, speed_factor, fps_factor, pen_array,draw_accuracy,physics_accuracy

    # Draw the gradient background
    light_color1 = (180, 220, 255)  # Very light blue
    light_color2 = (40, 100, 255)  # Slightly darker light blue
    startMenu_display = draw_gradient(startMenu_display, light_color1, light_color2)
    startMenu_display = draw_background_pattern(startMenu_display)

    # set initial simulation state
    constants.changeState("STARTMENU")
    ui= Gui.gui_startMenu(startMenu_display) # create start menu gui

    constants.pen_array.extend([Pendulum(SINGLE, [200,200],RANDOM_COLOUR),Pendulum(DOUBLE, ORIGIN_POINT,RAINBOW,isRainbow=True)]) #add initial pendulums

    M = Mouse() # create simulated mouse input

    initiate = True
    initiateAbout = True

    # game loop
    running = True
    while running:
        # update time
        dt = clock.tick(GAME_FRAME_SPEED)
        physics_accuracy += dt
        draw_accuracy += dt

        # check inputs and if running then get event array
        running, event_array = pygame_event_buffer(running) 

        # check ui state and initiate sidebar info
        # THIS IS BAD but it works
        if (constants.simulationState == "SIMULATION" and constants.prev_simulationState == "STARTMENU" and initiate == True):
            if ui.state != "SIDEBAR":
                ui = Gui.changeGui("INFO")
                initiate = False
                initiateAbout = True
        elif (constants.simulationState == "STARTMENU" and constants.prev_simulationState == "SIMULATION"):
            ui = Gui.changeGui("MENU",startMenu_display)
            initiate = True
            constants.pen_array = []
        elif (constants.simulationState == "SIMULATION"):
            if (ui.state == "SIDEBAR" and ui.sidebarState ==  "CREATE" and ui.inCreate):
                ui = Gui.changeGui("CREATE")
            elif (ui.state == "SIDEBAR" and ui.sidebarState ==  "INFO" and ui.was_inCreate):
                ui = Gui.changeGui("INFO")
        elif (constants.simulationState == "ABOUTMENU" and initiateAbout):
            ui = Gui.changeGui("ABOUT")
            initiateAbout = False
        elif (constants.simulationState == "STARTMENU" and constants.prev_simulationState == "ABOUTMENU" and initiateAbout == False):
            ui = Gui.changeGui("MENU",startMenu_display)
            initiateAbout = True
        
        # check which simulation state to run
        if constants.simulationState == "STARTMENU":
            ui = run_startMenuScreen(dt,M,event_array,ui)
        elif constants.simulationState == "ABOUTMENU":
            ui = run_aboutScreen(dt,M,event_array,ui)
        elif constants.simulationState == "SIMULATION":
            ui = run_simulationScreen(dt,M,event_array,ui)
        else:
            # stop running if no/incorrect state found
            running = False
            pygame.quit()
            sys.exit()

        # flip window display screen
        pygame.display.flip()
        window.fill(DARK_GREEN)

        # update window fps display
        fps = clock.get_fps()
        pygame.display.set_caption(f'Pendulum - {fps:.2f} FPS')

    pygame.quit()
    sys.exit()


def run_simulationScreen(dt,M,event_array,ui_Sidebar):
    global draw_accuracy,physics_accuracy,simulation_display

    # handle edit GUI widget events
    ui_Sidebar = handle_event_buffer(event_array, M, ui_Sidebar)

    # handle pendulem events
    update_pendulum_events(M, dt)

    # udate mouse movements and collistion detection
    M.update(dt) 

    # update pendulems with repect to the simulation speed
    while physics_accuracy >= GAME_PHYSICS_SPEED / constants.speed_factor:
        for pen in constants.pen_array:
            pen.update()
        physics_accuracy -= GAME_PHYSICS_SPEED / constants.speed_factor

    # update and draw edit Gui widgets
    if ui_Sidebar.gui_widget_list:
        for category, widgets in ui_Sidebar.gui_widget_list.items():
            for name, widget in widgets.items():
               if isinstance(widget, Slider):
                    widget.update()
    ui_Sidebar.draw()

    # draw the updated simulation with respect to the simulated frames
    while draw_accuracy >= 1 / constants.fps_factor * 1000:
        simulation_display.fill(LIGHT_GREY)
        simulation_display, constants.pen_array = draw_rods(simulation_display, constants.pen_array)
        pygame.draw.rect(simulation_display, BLACK, (0, 0, WIDTH/4*3, HEIGHT), BORDER_THICKNESS)
        draw_accuracy -= 1 / constants.fps_factor * 1000

    # draw the displays on the window and flip screen
    window.blit(ui_Sidebar.display, (0, 0))
    window.blit(simulation_display, (WIDTH/4, 0))

    return ui_Sidebar


def run_startMenuScreen(dt,M,event_array,ui_startMenu):
    global startMenu_display,draw_accuracy,physics_accuracy

    # handle edit GUI widget events
    ui_startMenu = handle_event_buffer(event_array, M, ui_startMenu)

    # udate mouse movements and collistion detection
    M.update(dt) 

    # update and reset physics_accuracy counter
    while physics_accuracy >= GAME_PHYSICS_SPEED / constants.speed_factor:
        physics_accuracy -= GAME_PHYSICS_SPEED / constants.speed_factor

    ui_startMenu.draw()

    # update and reset draw_accuracy counter
    while draw_accuracy >= 1 / constants.fps_factor * 1000:
        draw_accuracy -= 1 / constants.fps_factor * 1000

    # draw the displays on the window and flip screen
    
    window.blit(startMenu_display, (0, 0))
    window.blit(ui_startMenu.display, (0, 0))

    return ui_startMenu


def run_aboutScreen(dt,M,event_array,ui_aboutMenu):
    global startMenu_display,draw_accuracy,physics_accuracy

    # handle edit GUI widget events
    ui_aboutMenu = handle_event_buffer(event_array, M, ui_aboutMenu)

    # udate mouse movements and collistion detection
    M.update(dt) 

    # update and reset physics_accuracy counter
    while physics_accuracy >= GAME_PHYSICS_SPEED / constants.speed_factor:
        physics_accuracy -= GAME_PHYSICS_SPEED / constants.speed_factor

    # draw edit Gui widgets
    pygame.draw.rect(startMenu_display, BLACK, (0, 0, WIDTH, HEIGHT), BORDER_THICKNESS)
    ui_aboutMenu.draw()

    # update and reset draw_accuracy counter
    while draw_accuracy >= 1 / constants.fps_factor * 1000:
        draw_accuracy -= 1 / constants.fps_factor * 1000

    # draw the displays on the window and flip screen
    window.blit(startMenu_display, (0, 0))
    window.blit(ui_aboutMenu.display, (0, 0))

    return ui_aboutMenu


if __name__ == "__main__":
    main()
