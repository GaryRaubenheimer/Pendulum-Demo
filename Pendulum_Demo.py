import sys

# Import game context instead of pygame directly
from game_context import get_game_context, get_pygame

# Import managers
from StateManager import StateManager
from UIManager import UIManager
from EventManager import EventManager
from RenderManager import RenderManager

# Import constants and color definitions
from constants import WIDTH, HEIGHT, GAME_FRAME_SPEED
from colour import DARK_GREEN

# Import mouse input handler
from Input import Mouse

# Import validation tests
from test_game_validation import run_validation

# Initialize game context and get pygame instance
game_context = get_game_context()
pygame = get_pygame()

# Initialize the display using game context
window = game_context.initialize_display(WIDTH, HEIGHT, "Pendulum Demo")
clock = game_context.get_clock()


def draw_gradient(surface, color1, color2):
    """Draw a vertical gradient on the given surface."""
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))
    return surface


def draw_background_pattern(surface):
    """Draw a circular pattern on the given surface."""
    center_x = WIDTH * 3 // 8  # Center in the first 3/4 of the width
    center_y = HEIGHT // 2
    max_radius = min(WIDTH, HEIGHT) // 3

    for i in range(10):
        radius = max_radius - (i * (max_radius // 10))
        color = (180 - i * 20, 220 - i * 20, 255 - i * 25)  # Light colors
        pygame.draw.circle(surface, color, (center_x, center_y), radius, width=3)
    return surface


def main():
    """Main application entry point."""
    # Run initial validation
    validation_results = run_validation()
    print("\nInitial Validation Results:")
    for result in validation_results:
        print(result)

    # Create managers
    state_manager = StateManager()
    ui_manager = UIManager(pygame, window)
    event_manager = EventManager(pygame)
    render_manager = RenderManager(pygame, window)

    # Connect managers
    state_manager.set_ui_manager(ui_manager)
    ui_manager.set_state_manager(state_manager)
    event_manager.set_state_manager(state_manager)
    event_manager.set_ui_manager(ui_manager)
    render_manager.set_state_manager(state_manager)
    render_manager.set_ui_manager(ui_manager)
    render_manager.set_clock(clock)

    # Initialize menu display with gradient background
    menu_display = ui_manager.get_menu_display()
    light_color1 = (180, 220, 255)  # Very light blue
    light_color2 = (40, 100, 255)  # Slightly darker light blue
    menu_display = draw_gradient(menu_display, light_color1, light_color2)
    menu_display = draw_background_pattern(menu_display)

    # Create mouse input handler
    mouse = Mouse()

    # Start the application in the STARTUP state
    state_manager.change_state(StateManager.STARTUP)

    # Main game loop
    running = True
    while running:
        # Update time
        dt = clock.tick(GAME_FRAME_SPEED)
        render_manager.update_timing(dt)

        # Process events
        running, events = event_manager.process_events(running, mouse)

        # Handle events based on current state
        current_state = state_manager.get_current_state()
        if current_state == StateManager.SIMULATION:
            event_manager.handle_simulation_events(events, mouse, dt)
        elif current_state == StateManager.STARTMENU:
            event_manager.handle_menu_events(events, mouse, dt)
        elif current_state == StateManager.ABOUTMENU:
            event_manager.handle_about_events(events, mouse, dt)
        elif current_state == StateManager.QUIT:
            running = False

        # Render the current state
        render_manager.render()

    # Clean up and exit
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
