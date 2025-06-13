import Gui
from constants import WIDTH, HEIGHT
from colour import LIGHT_GREY, BLACK
from Event import handle_event_buffer


class UIManager:
    """
    Manages all UI components and their interactions.

    This class centralizes UI creation, updates, and transitions,
    providing a clean interface for the rest of the application.
    """

    # Define UI types
    MENU = "MENU"
    SIMULATION = "SIMULATION"
    ABOUT = "ABOUT"

    # Define sidebar states
    INFO = "INFO"
    CREATE = "CREATE"
    EDIT = "EDIT"

    def __init__(self, pygame_instance, window):
        """Initialize the UI manager."""
        self.pygame = pygame_instance
        self.window = window

        # Create display surfaces
        self.simulation_display = self.pygame.Surface((WIDTH / 4 * 3, HEIGHT))
        self.menu_display = self.pygame.Surface((WIDTH, HEIGHT))

        # Current UI component
        self.current_ui = None
        self.current_ui_type = None

        # State manager reference (will be set by the application)
        self.state_manager = None

    def set_state_manager(self, state_manager):
        """Set the state manager reference."""
        self.state_manager = state_manager

    def create_start_menu(self):
        """Create and set the start menu UI."""
        self.current_ui = Gui.gui_startMenu(self.menu_display)
        if self.state_manager:
            self.current_ui.set_state_manager(self.state_manager)
        self.current_ui_type = self.MENU
        return self.current_ui

    def create_about_menu(self):
        """Create and set the about menu UI."""
        self.current_ui = Gui.gui_aboutMenu()
        if self.state_manager:
            self.current_ui.set_state_manager(self.state_manager)
        self.current_ui_type = self.ABOUT
        return self.current_ui

    def create_simulation_ui(self, sidebar_state=INFO):
        """
        Create and set the simulation UI with the specified sidebar.

        Args:
            sidebar_state: The sidebar state to use (INFO, CREATE, or EDIT)
        """
        # Create new UI instance
        self.current_ui = Gui.gui_Sidebar()

        # Set state manager if available
        if self.state_manager:
            self.current_ui.set_state_manager(self.state_manager)

        # Initialize UI and change to appropriate state
        self.current_ui.initialize_Sidebar()
        if sidebar_state != self.INFO:
            self.current_ui.change_sidebar_state(sidebar_state)

        self.current_ui_type = self.SIMULATION
        return self.current_ui

    def change_sidebar(self, sidebar_state):
        """
        Change the sidebar in the simulation UI.

        Args:
            sidebar_state: The sidebar state to use (INFO, CREATE, or EDIT)
        """
        if self.current_ui_type != self.SIMULATION:
            return None

        if not self.current_ui:
            self.current_ui = self.create_simulation_ui(sidebar_state)
        else:
            self.current_ui.change_sidebar_state(sidebar_state)
        
        return self.current_ui

    def update_edit_sidebar(self, pendulum):
        """
        Update the edit sidebar with the selected pendulum's information.

        Args:
            pendulum: The pendulum to edit
        """
        if self.current_ui_type == self.SIMULATION:
            self.current_ui.change_sidebarStateToEdit(pendulum)

    def draw(self):
        """Draw the current UI to the window."""
        if not self.current_ui:
            return

        # Draw UI based on type
        if self.current_ui_type == self.MENU:
            self.current_ui.draw()
            self.window.blit(self.menu_display, (0, 0))

        elif self.current_ui_type == self.ABOUT:
            self.current_ui.draw()
            self.window.blit(self.current_ui.display, (0, 0))

        elif self.current_ui_type == self.SIMULATION:
            # Draw sidebar
            self.current_ui.draw()

            # Blit to window - sidebar first, then simulation display
            self.window.blit(self.current_ui.display, (0, 0))
            self.window.blit(self.simulation_display, (WIDTH / 4, 0))

    def handle_events(self, events, mouse):
        """
        Handle UI events.

        Args:
            events: List of pygame events
            mouse: Mouse input handler

        Returns:
            Updated UI component
        """
        if not self.current_ui:
            return self.current_ui

        # Use the handle_event_buffer function from the Event module
        return handle_event_buffer(events, mouse, self.current_ui)

    def get_simulation_display(self):
        """Get the simulation display surface."""
        return self.simulation_display

    def get_menu_display(self):
        """Get the menu display surface."""
        return self.menu_display

    def get_current_ui(self):
        """Get the current UI component."""
        return self.current_ui
