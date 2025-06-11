"""
Constants Module

This module contains all global constants and configuration values for the pendulum simulation.
It defines pendulum types, display settings, physics parameters, and simulation state management.

Constants:
    Pendulum Types: SINGLE, DOUBLE
    Display Settings: WIDTH, HEIGHT, ORIGIN_POINT, BORDER_THICKNESS
    Physics Settings: GRAVITY, SPEED_LIMIT, GAME_PHYSICS_SPEED
    Performance Settings: GAME_FRAME_SPEED, speed_factor, fps_factor
    State Management: simulation_state, previous_simulation_state
"""

from typing import List, Any

# Pendulum Type Constants
SINGLE: int = 1
DOUBLE: int = 2

# Display Configuration
WIDTH: int = 1200
HEIGHT: int = 650
ORIGIN_POINT: List[float] = [WIDTH / 2, HEIGHT / 2]
BORDER_THICKNESS: int = 5

# Performance and Frame Rate Settings
GAME_FRAME_SPEED: int = 60  # Target FPS for display updates
GAME_PHYSICS_SPEED: int = 20  # Physics update interval in milliseconds

# Physics Constants
GRAVITY: float = 0.3  # Simplified gravity constant (not real-world 9.81 m/s²)
SPEED_LIMIT: float = 0.5  # Maximum velocity limit for stability

# Simulation Speed Control
speed_factor: float = 1.0  # Global speed multiplier for simulation
fps_factor: float = GAME_FRAME_SPEED * 1.0  # Simulated frames calculation

# Simulation State Management
simulation_state: str = "startup"
previous_simulation_state: str = ""

# Valid simulation states:
# "STARTMENU", "ABOUTMENU", "SIMULATION", "QUIT"

# Global Pendulum Storage
pen_array: List[Any] = []  # Array storing all active pendulum objects


def change_state(new_state: str) -> None:
    """
    Change the current simulation state.

    Updates both the current state and preserves the previous state
    for potential rollback or state transition logic.

    Args:
        new_state: The new simulation state to transition to

    Valid states:
        - "STARTMENU": Main menu screen
        - "ABOUTMENU": About/help screen
        - "SIMULATION": Active pendulum simulation
        - "QUIT": Application shutdown
    """
    global simulation_state, previous_simulation_state
    previous_simulation_state = simulation_state
    simulation_state = new_state


def get_current_state() -> str:
    """
    Get the current simulation state.

    Returns:
        The current simulation state string
    """
    return simulation_state


def get_previous_state() -> str:
    """
    Get the previous simulation state.

    Returns:
        The previous simulation state string
    """
    return previous_simulation_state


def reset_pendulum_array() -> None:
    """
    Clear all pendulums from the simulation.

    Resets the global pendulum array to an empty state.
    """
    global pen_array
    pen_array = []


def add_pendulum(pendulum: Any) -> None:
    """
    Add a pendulum to the simulation.

    Args:
        pendulum: Pendulum object to add to the simulation
    """
    pen_array.append(pendulum)


def remove_pendulum(index: int) -> None:
    """
    Remove a pendulum from the simulation by index.

    Args:
        index: Index of the pendulum to remove

    Raises:
        IndexError: If index is out of range
    """
    if 0 <= index < len(pen_array):
        pen_array.pop(index)
    else:
        raise IndexError(f"Pendulum index {index} out of range")


def get_pendulum_count() -> int:
    """
    Get the number of pendulums currently in the simulation.

    Returns:
        Number of active pendulums
    """
    return len(pen_array)
