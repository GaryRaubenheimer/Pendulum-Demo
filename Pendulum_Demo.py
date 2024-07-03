# -Import--------------------------------------------
import sys
import pygame

from colour import *
from constants import *
from Pendulum import *
from Render import *
from Event import *
from Input import *
from Widgets import *
from Widgets_Functions import *#change_speed,change_fps,button_click,radio_button_action


pygame.init()
pygame.display.set_caption('Pedulum Demo')
clock = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED + pygame.RESIZABLE)
gui_display = pygame.Surface((WIDTH/4, HEIGHT))
display = pygame.Surface((WIDTH/4*3, HEIGHT))
window.fill(GREEN)

speed_factor=1.0
fps_factor = GAME_FRAME_SPEED*1.0

# -Functions--------------------------------------------
def change_speed(slider_speed):
    global speed_factor
    speed_factor = slider_speed.get_real_value()

def change_fps(slider_fps):
    global fps_factor
    fps_factor = slider_fps.get_real_value()


# -Main--------------------------------------------
def main():
    print("Pedulum Demo")
    global window
    global display
    global speed_factor
    global fps_factor

    gui_widget_list=[]

    #(x, y, width, height, min_value, max_value, initial_value=, color):
    slider = Slider(50, HEIGHT // 2, WIDTH/4-100,10, 0.5,5,0.5,RED)
    slider_speed = Slider(50, (HEIGHT // 3)*2, WIDTH/4-100,10, 0.2,5,0.208333333,GREEN,action=change_speed)
    slider_fps = Slider(50, (HEIGHT // 4)*3, WIDTH/4-100,10, 1,GAME_FRAME_SPEED,1.016949,DARK_YELLOW,action=change_fps)

    #(x, y, width, height, color, hover_color, text='', font_size=20, text_color=(255, 255, 255), action=None):
    button = Button(50, HEIGHT // 9, 100, 50, BLUE, RED, "Button 1", action=button_click)

    #(x, y, radius, color, check_color, hover_color, action=None)
    radio_button = RadioButton(50, HEIGHT // 4, 20, LIGHT_GREY, BLACK, DARK_GREY, radio_button_action)

    gui_widget_list.append(slider)
    gui_widget_list.append(slider_speed)
    gui_widget_list.append(slider_fps)
    gui_widget_list.append(button)
    gui_widget_list.append(radio_button)

    M = Mouse()

    pen_array = []

    pendulum1 = Pendulum(DOUBLE,ORIGIN_POINT)
    pen_array.append(pendulum1)
    pendulum2 = Pendulum(SINGLE,[50,50])
    pen_array.append(pendulum2)
  
    draw_acc = 0
    physics_acc = 0
    running = True
    while running:
        #print("loop")
        
        # update time
        dt = clock.tick(GAME_FRAME_SPEED)
        physics_acc += dt
        draw_acc += dt

        # update events
        running ,event_array = pygame_event_buffer(running)
        handle_event_buffer(event_array, M, pen_array,gui_widget_list)
        update_pedulum_events(M,dt)

        # update input
        M.update(dt)

        # update physics at speed_factor speed
        n = 1
        while physics_acc>=GAME_PHYSICS_SPEED/speed_factor:
            for i in range(n):
                for pen in pen_array:
                    pen.update()
            physics_acc-=GAME_PHYSICS_SPEED/speed_factor

        #update gui widgets
        for widget in gui_widget_list:
            if isinstance(widget, Slider):
                widget.update()
                
        print(speed_factor)
        #draw gui widgets
        gui_display.fill(CYAN)
        for widget in gui_widget_list:
            widget.draw(gui_display)
        
        #draw pendulums at fps factor speed
        n=1
        while draw_acc>=1/fps_factor*1000:
            for i in range(n):
                display.fill(LIGHT_GREY)
                display, pen_array = draw_rods(display, pen_array)
                #border
                pygame.draw.rect(display, BLACK, (0, 0,WIDTH/4*3, HEIGHT), BORDER_THICKNESS)
            draw_acc-=1/fps_factor*1000
    
        #update display
        window.blit(gui_display,(0,0))
        window.blit(display,(WIDTH/4,0))
        pygame.display.flip()
        window.fill(GREEN)      # green if screen cant update

        #get fps
        fps = clock.get_fps()
        pygame.display.set_caption(f'Pendulum - {fps:.2f} FPS')

    pygame.quit()
    sys.exit()


if __name__=="__main__":
    main()
