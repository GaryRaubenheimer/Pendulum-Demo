import sys
import pygame

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
about_display = pygame.Surface((WIDTH, HEIGHT))
about_display.fill(YELLOW)
#error_display = pygame.Surface((WIDTH, HEIGHT))
#error_display.fill(BLUE)

#window.blit(error_display, (0, 0))
window.fill(DARK_GREEN) # DARK_GREEN Screen means that display could not be displayed

draw_accuracy = 0 # simulated frames counter
physics_accuracy = 0 # speed of simulation counter


def main():
    global window, simulation_display, about_display, speed_factor, fps_factor, pen_array,draw_accuracy,physics_accuracy

    # set initial simulation state
    constants.changeState("STARTMENU")
    ui= Gui.gui_startMenu() # create start menu gui
    
    # ui_About = gui_aboutMenu() # create about gui 
    # ui_Sidebar = gui_Sidebar() # create side bar gui for editing and creating pendulums

    '''[Pendulum(DOUBLE, ORIGIN_POINT,RANDOM_COLOUR),'''
    constants.pen_array.extend([Pendulum(DOUBLE, ORIGIN_POINT,RANDOM_COLOUR),Pendulum(SINGLE, [50, 50],RAINBOW,isRainbow=True )]) #add pendulums

    M = Mouse() # create simulated mouse input

    initiate = True

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
        elif (constants.simulationState == "STARTMENU" and constants.prev_simulationState == "SIMULATION"):
            ui = Gui.changeGui("MENU")
            initiate = True
            constants.pen_array = []
        elif (constants.simulationState == "SIMULATION"):
            if (ui.state == "SIDEBAR" and ui.sidebarState ==  "CREATE" and ui.inCreate):
                ui = Gui.changeGui("CREATE")
        
        # check which simulation state to run
        if constants.simulationState == "STARTMENU":
            ui = run_startMenuScreen(dt,M,event_array,ui)
        elif constants.simulationState == "ABOUTMENU":
            run_aboutScreen()
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

# TO DO: something to create pendulem to start

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

    # update and draw edit Gui widgets
    if ui_startMenu.gui_widget_list:
        for category, widgets in ui_startMenu.gui_widget_list.items():
            for name, widget in widgets.items():
               if isinstance(widget, Slider):
                    widget.update()
    ui_startMenu.draw()

    # update and reset draw_accuracy counter
    while draw_accuracy >= 1 / constants.fps_factor * 1000:
        draw_accuracy -= 1 / constants.fps_factor * 1000

    # draw the displays on the window and flip screen
    startMenu_display.fill(LIGHT_GREY)
    pygame.draw.rect(simulation_display, BLACK, (0, 0, WIDTH, HEIGHT), BORDER_THICKNESS)
    window.blit(startMenu_display, (0, 0))
    window.blit(ui_startMenu.display, (0, 0))

    return ui_startMenu


def run_aboutScreen():
    pass

if __name__ == "__main__":
    main()
