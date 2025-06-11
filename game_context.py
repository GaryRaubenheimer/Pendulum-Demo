"""
Game Context Module

This module provides a centralized location for shared game resources and context,
eliminating circular import dependencies and providing proper pygame instance management.
"""

import pygame

# Initialize pygame once and make it available to all modules
pygame.init()

class GameContext:
    """
    Centralized game context that manages shared resources and state.
    This eliminates the need for circular imports and provides a clean interface.
    """
    
    def __init__(self):
        self.pygame = pygame
        self.window = None
        self.clock = None
        
    def initialize_display(self, width, height, caption="Game"):
        """Initialize the main game display"""
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((width, height), pygame.SCALED + pygame.RESIZABLE)
        return self.window
    
    def get_pygame(self):
        """Get the pygame module instance"""
        return self.pygame
    
    def get_window(self):
        """Get the main game window"""
        return self.window
    
    def get_clock(self):
        """Get the game clock"""
        return self.clock

# Global game context instance
game_context = GameContext()

def get_pygame():
    """Convenience function to get pygame instance"""
    return game_context.get_pygame()

def get_game_context():
    """Get the global game context"""
    return game_context 