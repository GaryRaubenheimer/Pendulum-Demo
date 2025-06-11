import math
import Gui
import constants

from game_context import get_pygame

# Get pygame instance from game context
pygame = get_pygame()

#---
# get all events from pygame
def pygame_event_buffer(running):
    events = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            events.append(event)
    return running, events

#---

def handle_event_buffer(events, M,ui):
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_button_down(event, M, constants.pen_array)
        elif event.type == pygame.MOUSEBUTTONUP:
            ui = handle_mouse_button_up(event, M,ui)
        # Handle GUI widget events
        if ui.gui_widget_list:
            for category, widgets in ui.gui_widget_list.items():
                for name, widget in widgets.items():
                    widget.handle_event(event)
    return ui

# handle mouse down input events in simulation
def handle_mouse_button_down(event, M, pen_array):
    if event.button == 1:  # Left mouse button pressed
        M.left_held = True
        for pen in pen_array:
            M.collision_pen_check(pen)
            pen.isSelected = False
    elif event.button == 2:  # Middle mouse button pressed
        for pen in pen_array:
            for pen in pen_array:
                M.collision_pen_check(pen)
                if M.collision_item and M.collision_item[0] != pen:
                    pen.isSelected = False
        if M.collision_item:
            M.collision_item[0].isSelected = True
    elif event.button == 3:  # Right mouse button pressed
        M.right_held = True
        for pen in pen_array:
            M.collision_pen_check(pen)
            if M.collision_item and M.collision_item[0] != pen:
                pen.isSelected = False
        if M.collision_item:
            M.collision_item[0].isSelected = True

# handle mouse up input events in simulation
def handle_mouse_button_up(event, M,ui):
    if event.button == 1:
        M.prev_state = M.left_held
        M.left_held = False
    elif event.button == 3:
        M.right_held = False
        if M.collision_item and M.left_held == False:
            ui = Gui.changeGui("EDIT")
            #ui.change_sidebar_state("EDIT")
            if ui.sidebarState == "EDIT":
                ui.change_guiEdit_widget_info(M.collision_item[0])
            M.collision_item = None
        else:
            #ui.kill_gui_widget_list()
            ui = Gui.changeGui("INFO")
            #ui.change_sidebar_state("INFO")
    elif event.button == 2:         #middle mouse button and remove pendulum
        if M.collision_item and M.left_held == False and M.right_held == False:
            constants.pen_array.remove(M.collision_item[0])
            M.collision_item = None
    return ui

#---

def update_pendulum_events(M, dt):
    mo = M.get_position()
    pos = [mo[0] - constants.WIDTH / 4, mo[1]]

    if M.left_held:
        update_held_pendulum(M, pos)
    elif not M.left_held and M.prev_state:
        release_held_pendulum(M, dt)

def update_held_pendulum(M, pos):
    if M.collision_item:
        held_pendulum, held_pin = M.collision_item
        if held_pin == held_pendulum.rods[0].pin_1:
            update_first_pin(pos, held_pendulum)
        elif held_pin == held_pendulum.rods[0].pin_2 and held_pendulum.type == constants.DOUBLE:
            update_split_pendulum(pos, held_pendulum)
        elif held_pin == held_pendulum.rods[held_pendulum.type - 1].pin_2:
            update_last_pin(pos, held_pendulum)

def update_first_pin(pos, held_pendulum):
    temp_pos = pos.copy()
    temp_pos[0] = max(constants.BORDER_THICKNESS + 2.5, min(pos[0], constants.WIDTH / 4 * 3 - constants.BORDER_THICKNESS - 2.5))
    temp_pos[1] = max(constants.BORDER_THICKNESS + 2.5, min(pos[1], constants.HEIGHT - constants.BORDER_THICKNESS - 2.5))

    held_pendulum.rods[0].pin_1.update_pos(temp_pos)
    held_pendulum.rods[0].update()
    if held_pendulum.type == constants.DOUBLE:
        held_pendulum.rods[1].pin_1.update_pos(held_pendulum.rods[0].pin_2.position)
        held_pendulum.rods[1].update()

def update_split_pendulum(pos, held_pendulum):
    held_pendulum.split()
    rod1, rod2 = held_pendulum.rods
    dx, dy = pos[0] - rod1.pin_1.x, pos[1] - rod1.pin_1.y
    angle_with_vertical = math.atan2(dx, dy)
    rod1.angular_velocity = 0
    rod1.angular_position = angle_with_vertical
    rod1.update()
    rod2.pin_1.update_pos(rod1.pin_2.position)
    rod2.update()

def update_last_pin(pos, held_pendulum):
    rod = held_pendulum.rods[held_pendulum.type - 1]
    dx, dy = pos[0] - rod.pin_1.x, pos[1] - rod.pin_1.y
    angle_with_vertical = math.atan2(dx, dy)
    rod.angular_velocity = 0
    rod.angular_position = angle_with_vertical
    rod.update()

def release_held_pendulum(M, dt):
    if M.collision_item:
        held_pendulum, held_pin = M.collision_item
        if held_pin == held_pendulum.rods[0].pin_1:
            M.collision_item = None
        elif held_pin == held_pendulum.rods[0].pin_2 and held_pendulum.type == constants.DOUBLE:
            release_split_pendulum(M, dt, held_pendulum)
        elif held_pin == held_pendulum.rods[held_pendulum.type - 1].pin_2:
            release_last_pin(M, dt, held_pendulum)
        M.collision_item = None
    M.prev_state = False

def release_split_pendulum(M, dt, held_pendulum):
    held_pendulum.unsplit()
    rod = held_pendulum.rods[0]
    apply_mouse_velocity_to_rod(M, dt, rod)

def release_last_pin(M, dt, held_pendulum):
    rod = held_pendulum.rods[held_pendulum.type - 1]
    apply_mouse_velocity_to_rod(M, dt, rod)

def apply_mouse_velocity_to_rod(M, dt, rod):
    mouse_velocity = M.get_velocity(dt)
    mouse_velocity_angle = M.direction_angle_from_vertical()
    if mouse_velocity_angle != 0:
        beta = (mouse_velocity_angle - ((3 * math.pi - rod.angular_position) % (2 * math.pi)))
        mouse_mag = (mouse_velocity[0] ** 2 + mouse_velocity[1] ** 2) ** 0.5
        new_angular_velocity = mouse_mag * math.sin(beta) * rod.bar.length * 0.0003
        rod.angular_velocity = -new_angular_velocity
    else:
        rod.angular_velocity = 0
