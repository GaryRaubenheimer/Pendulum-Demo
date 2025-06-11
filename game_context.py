"""
Game Context Module

This module provides a centralized location for shared game resources and context,
eliminating circular import dependencies and providing proper pygame instance management.
"""

from typing import Optional
import pygame

# Initialize pygame once and make it available to all modules
pygame.init()


class GameContext:
    """
    Centralized game context that manages shared resources and state.
    This eliminates the need for circular imports and provides a clean interface.

    Attributes:
        pygame: The pygame module instance
        window: The main game display surface
        clock: The pygame clock for frame rate management
    """

    def __init__(self) -> None:
        """Initialize the game context with default values."""
        self.pygame = pygame
        self.window: Optional[pygame.Surface] = None
        self.clock: Optional[pygame.time.Clock] = None

    def initialize_display(
        self, width: int, height: int, caption: str = "Game"
    ) -> pygame.Surface:
        """
        Initialize the main game display.

        Args:
            width: Width of the display window in pixels
            height: Height of the display window in pixels
            caption: Window title caption (default: "Game")

        Returns:
            The initialized pygame Surface representing the main window
        """
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(
            (width, height), pygame.SCALED + pygame.RESIZABLE
        )
        return self.window

    def get_pygame(self) -> pygame:
        """
        Get the pygame module instance.

        Returns:
            The pygame module
        """
        return self.pygame

    def get_window(self) -> Optional[pygame.Surface]:
        """
        Get the main game window.

        Returns:
            The main game window Surface, or None if not initialized
        """
        return self.window

    def get_clock(self) -> Optional[pygame.time.Clock]:
        """
        Get the game clock.

        Returns:
            The pygame Clock instance, or None if not initialized
        """
        return self.clock


# Global game context instance
game_context: GameContext = GameContext()


def get_pygame() -> pygame:
    """
    Convenience function to get pygame instance.

    Returns:
        The pygame module instance
    """
    return game_context.get_pygame()


def get_game_context() -> GameContext:
    """
    Get the global game context.

    Returns:
        The global GameContext instance
    """
    return game_context
