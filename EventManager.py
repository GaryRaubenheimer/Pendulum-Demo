from typing import List, Tuple
import pygame
import constants
from Event import (
    update_pendulum_events,
    handle_mouse_button_down,
    handle_mouse_button_up,
)


class EventManager:
    """
    Manages all event processing and dispatch.

    This class centralizes event handling, providing a clean interface
    for the rest of the application to receive and process events.
    """

    def __init__(self, pygame_instance):
        """Initialize the event manager."""
        self.pygame = pygame_instance

        # References to other managers (will be set by the application)
        self.state_manager = None
        self.ui_manager = None

    def set_state_manager(self, state_manager):
        """Set the state manager reference."""
        self.state_manager = state_manager

    def set_ui_manager(self, ui_manager):
        """Set the UI manager reference."""
        self.ui_manager = ui_manager

    def process_events(self, running: bool, mouse) -> Tuple[bool, List]:
        """
        Process all pending events.

        Args:
            running: Whether the application is running
            mouse: Mouse input handler

        Returns:
            Tuple of (running, event_list)
        """
        events = []

        # Process all pending events
        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT or (
                event.type == self.pygame.KEYDOWN and event.key == self.pygame.K_ESCAPE
            ):
                running = False
            elif event.type in (
                self.pygame.MOUSEBUTTONDOWN,
                self.pygame.MOUSEBUTTONUP,
                self.pygame.MOUSEMOTION,
            ):
                events.append(event)

        return running, events

    def handle_simulation_events(self, events: List, mouse, dt: float) -> None:
        """
        Handle events specific to the simulation state.

        Args:
            events: List of events to process
            mouse: Mouse input handler
            dt: Time delta since last frame
        """
        # Handle pendulum interaction events
        self.handle_pendulum_events(events, mouse)

        # Update pendulum events based on mouse input
        update_pendulum_events(mouse, dt)

        # Update mouse state
        mouse.update(dt)

        # Process UI events if we have a UI manager
        if self.ui_manager:
            current_ui = self.ui_manager.get_current_ui()
            if current_ui:
                # Handle events and get updated UI
                updated_ui = self.ui_manager.handle_events(events, mouse)

                # Process slider events
                if hasattr(current_ui, 'gui_widget_list'):
                    if isinstance(current_ui.gui_widget_list, dict):
                        for category, widgets in current_ui.gui_widget_list.items():
                            if category == 'sliders':
                                for name, widget in widgets.items():
                                    widget.handle_event(events[0] if events else None)
                                    widget.update()
                    elif isinstance(current_ui.gui_widget_list, list):
                        # Handle list case - no need to process sliders
                        pass

                # Check if UI state changed and update accordingly
                if updated_ui and updated_ui != current_ui:
                    if updated_ui.state == "MENU":
                        self.state_manager.change_state(self.state_manager.STARTMENU)
                    elif updated_ui.state == "SIDEBAR":
                        # Handle sidebar state changes
                        if hasattr(updated_ui, "sidebarState"):
                            # Force UI update by creating new UI
                            if updated_ui.sidebarState == "INFO":
                                self.ui_manager.change_sidebar(self.ui_manager.INFO)
                            elif updated_ui.sidebarState == "CREATE":
                                self.ui_manager.change_sidebar(self.ui_manager.CREATE)
                            elif updated_ui.sidebarState == "EDIT":
                                self.ui_manager.change_sidebar(self.ui_manager.EDIT)
                            
                            # Ensure the new UI is properly initialized
                            new_ui = self.ui_manager.get_current_ui()
                            if new_ui and hasattr(new_ui, "initialize_createPendulum"):
                                new_ui.initialize_createPendulum()
                            elif new_ui and hasattr(new_ui, "initialize_editGui"):
                                new_ui.initialize_editGui()
                            elif new_ui and hasattr(new_ui, "initialize_Sidebar"):
                                new_ui.initialize_Sidebar()

    def handle_pendulum_events(self, events: List, mouse) -> None:
        """
        Handle events specific to pendulum interaction.

        Args:
            events: List of events to process
            mouse: Mouse input handler
        """
        for event in events:
            # Handle mouse button down events
            if event.type == self.pygame.MOUSEBUTTONDOWN:
                handle_mouse_button_down(event, mouse, constants.pen_array)

                # Handle right-click to edit pendulum
                if event.button == 3 and mouse.collision_item:
                    if self.ui_manager:
                        self.ui_manager.change_sidebar("EDIT")
                        current_ui = self.ui_manager.get_current_ui()
                        if current_ui and hasattr(
                            current_ui, "change_guiEdit_widget_info"
                        ):
                            current_ui.change_guiEdit_widget_info(
                                mouse.collision_item[0]
                            )

            # Handle mouse button up events
            elif event.type == self.pygame.MOUSEBUTTONUP:
                if self.ui_manager:
                    current_ui = self.ui_manager.get_current_ui()
                    if current_ui:
                        handle_mouse_button_up(event, mouse, current_ui)

    def handle_menu_events(self, events: List, mouse, dt: float) -> None:
        """
        Handle events specific to the menu state.

        Args:
            events: List of events to process
            mouse: Mouse input handler
            dt: Time delta since last frame
        """
        # Update mouse state
        mouse.update(dt)

        # Process UI events if we have a UI manager
        if self.ui_manager:
            current_ui = self.ui_manager.get_current_ui()
            if current_ui:
                self.ui_manager.handle_events(events, mouse)

    def handle_about_events(self, events: List, mouse, dt: float) -> None:
        """
        Handle events specific to the about state.

        Args:
            events: List of events to process
            mouse: Mouse input handler
            dt: Time delta since last frame
        """
        # Update mouse state
        mouse.update(dt)

        # Process UI events if we have a UI manager
        if self.ui_manager:
            current_ui = self.ui_manager.get_current_ui()
            if current_ui:
                self.ui_manager.handle_events(events, mouse)
