import sys
import pygame

from colour import *
from constants import *
from Pendulum import *
from Render import *
from Event import *
from Input import *
from Widgets import *
from Gui import *

pygame.init()
pygame.display.set_caption('Pendulum Demo')
clock = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED + pygame.RESIZABLE)
display = pygame.Surface((WIDTH/4*3, HEIGHT))
window.fill(GREEN)

speed_factor = 1.0
fps_factor = GAME_FRAME_SPEED * 1.0

def main():
    global window, display, speed_factor, fps_factor, pen_array
    
    M = Mouse()
    ui_Edit = gui_Edit()

    pen_array.extend([Pendulum(DOUBLE, ORIGIN_POINT), Pendulum(SINGLE, [50, 50])])

    draw_acc = 0
    physics_acc = 0

    running = True
    while running:
        dt = clock.tick(GAME_FRAME_SPEED)
        physics_acc += dt
        draw_acc += dt
    
        running, event_array = pygame_event_buffer(running)
        handle_event_buffer(event_array, M, pen_array,ui_Edit)
        update_pendulum_events(M, dt)

        M.update(dt)

        while physics_acc >= GAME_PHYSICS_SPEED / speed_factor:
            for pen in pen_array:
                pen.update()
            physics_acc -= GAME_PHYSICS_SPEED / speed_factor

        if ui_Edit.gui_widget_list:
            for category, widgets in ui_Edit.gui_widget_list.items():
                for name, widget in widgets.items():
                   if isinstance(widget, Slider):
                        widget.update()

        ui_Edit.draw()

        while draw_acc >= 1 / fps_factor * 1000:
            display.fill(LIGHT_GREY)
            display, pen_array = draw_rods(display, pen_array)
            pygame.draw.rect(display, BLACK, (0, 0, WIDTH/4*3, HEIGHT), BORDER_THICKNESS)
            draw_acc -= 1 / fps_factor * 1000

        window.blit(ui_Edit.display, (0, 0))
        window.blit(display, (WIDTH/4, 0))
        pygame.display.flip()
        window.fill(GREEN)

        fps = clock.get_fps()
        pygame.display.set_caption(f'Pendulum - {fps:.2f} FPS')

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
