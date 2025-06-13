from typing import Dict, Callable
import constants
from Pendulum import Pendulum
from colour import get_RANDOM_COLOUR, RAINBOW
from constants import SINGLE, DOUBLE, ORIGIN_POINT


class StateManager:
    """
    Manages application states and transitions between them.

    This class centralizes all state management logic, providing a clean interface
    for state transitions and ensuring proper setup/teardown between states.
    """

    # Define valid states
    INIT = "INIT"  # Special initial state
    STARTUP = "STARTUP"
    STARTMENU = "STARTMENU"
    SIMULATION = "SIMULATION"
    ABOUTMENU = "ABOUTMENU"
    QUIT = "QUIT"

    def __init__(self):
        """Initialize the state manager with default state."""
        self.current_state = self.INIT  # Start in INIT state
        self.previous_state = ""
        self.state_enter_handlers: Dict[str, Callable] = {
            self.STARTUP: self._enter_startup,
            self.STARTMENU: self._enter_startmenu,
            self.SIMULATION: self._enter_simulation,
            self.ABOUTMENU: self._enter_aboutmenu,
            self.QUIT: self._enter_quit,
        }
        self.state_exit_handlers: Dict[str, Callable] = {
            self.STARTUP: self._exit_startup,
            self.STARTMENU: self._exit_startmenu,
            self.SIMULATION: self._exit_simulation,
            self.ABOUTMENU: self._exit_aboutmenu,
            self.QUIT: self._exit_quit,
        }

        # Track if we've initialized pendulums in simulation
        self.pendulums_initialized = False

        # UI reference (will be set by UIManager)
        self.ui_manager = None

    def set_ui_manager(self, ui_manager):
        """Set the UI manager reference."""
        self.ui_manager = ui_manager

    def change_state(self, new_state: str) -> None:
        """
        Change the current state to a new state.

        This method handles the proper exit of the current state
        and entry into the new state.

        Args:
            new_state: The state to transition to
        """
        if new_state not in self.state_enter_handlers and new_state != self.INIT:
            raise ValueError(f"Invalid state: {new_state}")

        # Don't change if it's the same state, unless we're in INIT state
        if new_state == self.current_state and self.current_state != self.INIT:
            return

        # Exit current state
        if self.current_state in self.state_exit_handlers:
            self.state_exit_handlers[self.current_state]()

        # Update state tracking
        self.previous_state = self.current_state
        self.current_state = new_state

        # Update constants module state (for backward compatibility)
        constants.change_state(new_state)

        # Enter new state
        if new_state in self.state_enter_handlers:
            self.state_enter_handlers[new_state]()

    def get_current_state(self) -> str:
        """Get the current state."""
        return self.current_state

    def get_previous_state(self) -> str:
        """Get the previous state."""
        return self.previous_state

    # State entry handlers
    def _enter_startup(self) -> None:
        """Initialize the application on startup."""
        # This state is transient and should immediately transition to STARTMENU
        self.change_state(self.STARTMENU)

    def _enter_startmenu(self) -> None:
        """Enter the start menu state."""
        if self.ui_manager:
            self.ui_manager.create_start_menu()

    def _enter_simulation(self) -> None:
        """Enter the simulation state."""
        # Always initialize pendulums when entering simulation
        self._initialize_pendulums()

        if self.ui_manager:
            self.ui_manager.create_simulation_ui()

    def _enter_aboutmenu(self) -> None:
        """Enter the about menu state."""
        if self.ui_manager:
            self.ui_manager.create_about_menu()

    def _enter_quit(self) -> None:
        """Enter the quit state."""
        # Nothing specific needed here as the main loop will handle actual quitting

    # State exit handlers
    def _exit_startup(self) -> None:
        """Exit the startup state."""

    def _exit_startmenu(self) -> None:
        """Exit the start menu state."""

    def _exit_simulation(self) -> None:
        """Exit the simulation state."""
        # We don't clear pendulums here to preserve them between simulation sessions

    def _exit_aboutmenu(self) -> None:
        """Exit the about menu state."""

    def _exit_quit(self) -> None:
        """Exit the quit state."""

    def _initialize_pendulums(self) -> None:
        """Initialize default pendulums for the simulation."""
        # Clear any existing pendulums
        constants.pen_array = []

        # Add initial pendulums
        constants.pen_array.extend(
            [
                Pendulum(SINGLE, [200, 200], get_RANDOM_COLOUR()),
                Pendulum(DOUBLE, ORIGIN_POINT, RAINBOW, isRainbow=True),
            ]
        )

        # Validate pendulum initialization
        if len(constants.pen_array) != 2:
            raise RuntimeError(f"Failed to initialize pendulums. Expected 2, got {len(constants.pen_array)}")

        self.pendulums_initialized = True

    def reset_pendulums(self) -> None:
        """Reset all pendulums."""
        constants.pen_array = []
        self.pendulums_initialized = False

    def validate_pendulums(self) -> bool:
        """Validate that pendulums are properly initialized."""
        return len(constants.pen_array) > 0 and self.pendulums_initialized
