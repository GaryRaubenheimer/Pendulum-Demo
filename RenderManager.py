import pygame
import constants
from Render import draw_rods
from colour import LIGHT_GREY, BLACK, DARK_GREEN


class RenderManager:
    """
    Manages all rendering operations.

    This class centralizes rendering logic, providing a clean interface
    for drawing the application state.
    """

    def __init__(self, pygame_instance, window):
        """Initialize the render manager."""
        self.pygame = pygame_instance
        self.window = window

        # Rendering timing variables
        self.draw_accuracy = 0
        self.physics_accuracy = 0

        # References to other managers (will be set by the application)
        self.state_manager = None
        self.ui_manager = None

        # Clock reference (will be set by set_clock)
        self.clock = None

    def set_state_manager(self, state_manager):
        """Set the state manager reference."""
        self.state_manager = state_manager

    def set_ui_manager(self, ui_manager):
        """Set the UI manager reference."""
        self.ui_manager = ui_manager

    def update_timing(self, dt):
        """
        Update rendering timing variables.

        Args:
            dt: Time delta since last frame
        """
        self.draw_accuracy += dt
        self.physics_accuracy += dt

    def update_physics(self):
        """Update physics simulation."""
        while (
            self.physics_accuracy
            >= constants.GAME_PHYSICS_SPEED / constants.speed_factor
        ):
            for pen in constants.pen_array:
                pen.update()
            self.physics_accuracy -= (
                constants.GAME_PHYSICS_SPEED / constants.speed_factor
            )

    def render_simulation(self):
        """Render the simulation state."""
        if not self.ui_manager:
            return

        # Get the simulation display surface
        simulation_display = self.ui_manager.get_simulation_display()

        # Update physics
        self.update_physics()

        # Draw the simulation at the appropriate frame rate
        while self.draw_accuracy >= 1 / constants.fps_factor * 1000:
            # Fill background
            simulation_display.fill(LIGHT_GREY)

            # Draw all pendulum rods
            simulation_display, constants.pen_array = draw_rods(
                simulation_display, constants.pen_array
            )

            # Draw border
            pygame.draw.rect(
                simulation_display,
                BLACK,
                (0, 0, constants.WIDTH / 4 * 3, constants.HEIGHT),
                constants.BORDER_THICKNESS,
            )

            self.draw_accuracy -= 1 / constants.fps_factor * 1000

        # Let the UI manager handle drawing the UI components
        self.ui_manager.draw()

    def render_menu(self):
        """Render the menu state."""
        if not self.ui_manager:
            return

        # Reset physics accuracy counter
        while (
            self.physics_accuracy
            >= constants.GAME_PHYSICS_SPEED / constants.speed_factor
        ):
            self.physics_accuracy -= (
                constants.GAME_PHYSICS_SPEED / constants.speed_factor
            )

        # Reset draw accuracy counter
        while self.draw_accuracy >= 1 / constants.fps_factor * 1000:
            self.draw_accuracy -= 1 / constants.fps_factor * 1000

        # Let the UI manager handle drawing the UI components
        self.ui_manager.draw()

    def render_about(self):
        """Render the about state."""
        if not self.ui_manager:
            return

        # Reset physics accuracy counter
        while (
            self.physics_accuracy
            >= constants.GAME_PHYSICS_SPEED / constants.speed_factor
        ):
            self.physics_accuracy -= (
                constants.GAME_PHYSICS_SPEED / constants.speed_factor
            )

        # Reset draw accuracy counter
        while self.draw_accuracy >= 1 / constants.fps_factor * 1000:
            self.draw_accuracy -= 1 / constants.fps_factor * 1000

        # Let the UI manager handle drawing the UI components
        self.ui_manager.draw()

    def render(self):
        """Render the current state."""
        if not self.state_manager:
            return

        # Clear the window
        self.window.fill(DARK_GREEN)

        # Render based on current state
        current_state = self.state_manager.get_current_state()

        if current_state == self.state_manager.SIMULATION:
            self.render_simulation()
        elif current_state == self.state_manager.STARTMENU:
            self.render_menu()
        elif current_state == self.state_manager.ABOUTMENU:
            self.render_about()

        # Update the display
        pygame.display.flip()

        # Update FPS display
        if self.clock:
            fps = self.clock.get_fps()
            pygame.display.set_caption(f"Pendulum - {fps:.2f} FPS")

    def set_clock(self, clock):
        """Set the pygame clock reference."""
        self.clock = clock
