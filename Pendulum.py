"""
Pendulum Physics Module

This module contains the core pendulum simulation classes including Pendulum, Rod, Bar, and Pin.
It provides the physical representation and behavior of single and double pendulums with
support for trace visualization, rainbow effects, and physics integration.

Classes:
    Pendulum: Main pendulum system that can be single or double type
    Rod: Individual rod component with pins and bars
    Bar: Rigid bar connecting pins in a pendulum rod
    Pin: Mass point in the pendulum system with position and physics properties
"""

import math
from typing import List, Tuple, Optional, Any, Union
import colour

from game_context import get_pygame
from constants import SINGLE, DOUBLE
from Physics import update_rods

# Get pygame instance from game context
pygame = get_pygame()

# Physical Constants for Pendulum Simulation
PIN2_WEIGHT_SINGLE: float = 5.0
PIN2_RADIUS_SINGLE: int = 15
BAR_LENGTH_SINGLE: int = 100
BAR_WIDTH: int = 3
BAR_COLOUR: Tuple[int, int, int] = colour.BLACK
ANGULAR_POSITION_SINGLE: float = math.pi / 3

PIN2_WEIGHT_DOUBLE: float = 1.0
ANGULAR_POSITION_DOUBLE: float = math.pi

TRACE_POINTS_LENGTH: int = 50

# Type aliases for better code clarity
Position = List[float]
Color = Tuple[int, int, int]
RodInfo = List[Any]


class Pendulum:
    """
    Main pendulum system that can simulate single or double pendulums.

    A pendulum consists of one or more rods, each with pins and bars. The pendulum
    can be split into independent single pendulums or combined as a coupled system.

    Attributes:
        type (int): Pendulum type (SINGLE or DOUBLE)
        origin_pos (Position): Origin position [x, y] of the pendulum
        trace_points_colour (Color): Color of the trace points
        isRainbow (bool): Whether to use rainbow color cycling
        rods (List[Rod]): List of rod components
        isSplit (bool): Whether the pendulum is split into independent parts
        isSelected (bool): Whether the pendulum is currently selected
    """

    def __init__(
        self,
        pendulum_type: int,
        origin_pos: Position,
        trace_colour: Color,
        isRainbow: bool = False,
    ) -> None:
        """
        Initialize a new pendulum system.

        Args:
            pendulum_type: Type of pendulum (SINGLE or DOUBLE)
            origin_pos: Origin position [x, y] in screen coordinates
            trace_colour: RGB color tuple for trace points
            isRainbow: Whether to enable rainbow color cycling
        """
        self.type = pendulum_type
        self.origin_pos = origin_pos
        self.trace_points_colour = trace_colour
        self.isRainbow = isRainbow
        rods_info = self.create_rod_info()
        self.rods = self.create_rod_array(rods_info, self.trace_points_colour)
        self.isSplit = False
        self.isSelected = False

    def get_info(self) -> List[Any]:
        """
        Get comprehensive information about the pendulum system.

        Returns:
            List containing pendulum type and rod information
        """
        info_list = [self.type]
        for rod in self.rods:
            info_list.append(rod.get_info())
        return info_list

    def create_rod_info(self) -> List[RodInfo]:
        """
        Create configuration information for all rods in the pendulum.

        Returns:
            List of rod configuration data
        """
        rods_info = []
        friction = 0.0

        if self.type == SINGLE:
            rods_info.append(self._create_single_rod_info(friction))
        elif self.type == DOUBLE:
            rods_info.append(self._create_single_rod_info(friction))
            rods_info.append(self._create_double_rod_info(friction, rods_info[0]))

        return rods_info

    def _create_single_rod_info(self, friction_coefficient: float) -> RodInfo:
        """
        Create configuration for a single rod (used as first rod in any pendulum).

        Args:
            friction_coefficient: Friction coefficient for the rod

        Returns:
            Configuration data for the rod [pins_info, bar_info, angular_position]
        """
        pins_info = [
            PIN2_WEIGHT_SINGLE,
            PIN2_RADIUS_SINGLE,
            [colour.GREY, colour.RED],
            friction_coefficient,
            self.origin_pos,
        ]
        bar_info = [0, BAR_LENGTH_SINGLE, BAR_WIDTH, BAR_COLOUR]
        return [pins_info, bar_info, ANGULAR_POSITION_SINGLE]

    def _create_double_rod_info(
        self, friction_coefficient: float, first_rod_info: RodInfo
    ) -> RodInfo:
        """
        Create configuration for the second rod in a double pendulum.

        Args:
            friction_coefficient: Friction coefficient for the rod
            first_rod_info: Configuration of the first rod to calculate attachment point

        Returns:
            Configuration data for the second rod
        """
        pins_info = [
            PIN2_WEIGHT_DOUBLE,
            PIN2_RADIUS_SINGLE,
            [colour.GREY, colour.RED],
            friction_coefficient,
            self._calculate_pin_position(first_rod_info),
        ]
        bar_info = [0, BAR_LENGTH_SINGLE, BAR_WIDTH, BAR_COLOUR]
        return [pins_info, bar_info, ANGULAR_POSITION_DOUBLE]

    def _calculate_pin_position(self, rod_info: RodInfo) -> Position:
        """
        Calculate the position of a pin based on rod configuration.

        Args:
            rod_info: Configuration data of the rod

        Returns:
            [x, y] position of the pin
        """
        pin_position = [0.0, 0.0]
        pin_position[0] = rod_info[0][4][0] + rod_info[1][1] * math.sin(rod_info[2])
        pin_position[1] = rod_info[0][4][1] + rod_info[1][1] * math.cos(rod_info[2])
        return pin_position

    def create_rod_array(
        self, rods_info: List[RodInfo], trace_points_colour: Color
    ) -> List["Rod"]:
        """
        Create Rod objects from configuration data.

        Args:
            rods_info: List of rod configuration data
            trace_points_colour: Color for trace points

        Returns:
            List of initialized Rod objects
        """
        rods = []
        for rod_id, rod_info in enumerate(rods_info, start=1):
            rods.append(
                Rod(rod_id, self.isRainbow, self.type, trace_points_colour, *rod_info)
            )
        return rods

    def split(self) -> None:
        """
        Split the pendulum into independent single pendulums.

        This converts a double pendulum into two independent single pendulums
        for simulation purposes.
        """
        for rod in self.rods:
            rod.type = SINGLE
        self.isSplit = True

    def unsplit(self) -> None:
        """
        Recombine split pendulum into a coupled system.

        This converts independent single pendulums back into a coupled
        double pendulum system.
        """
        for rod in self.rods:
            rod.type = DOUBLE
        self.isSplit = False

    def update(self) -> None:
        """
        Update the pendulum physics simulation.

        Calls the physics engine to update all rod positions and velocities.
        """
        self.rods = update_rods(self.rods, self.isSplit, self.type)


class Rod:
    """
    Individual rod component of a pendulum system.

    A rod consists of two pins connected by a bar, with angular position and velocity.
    The rod handles the physical properties and updates of its components.

    Attributes:
        angular_position (float): Current angle in radians
        angular_velocity (float): Current angular velocity
        rod_id (int): Unique identifier for this rod
        type (int): Pendulum type this rod belongs to
        pin_1 (Pin): First pin (usually the pivot/attachment point)
        pin_2 (Pin): Second pin (the mass point)
        bar (Bar): The rigid bar connecting the pins
    """

    def __init__(
        self,
        rod_id: int,
        isRainbow: bool,
        pendulum_type: int,
        trace_points_colour: Color,
        pins_info: List[Any],
        bar_info: List[Any],
        angular_position: float,
    ) -> None:
        """
        Initialize a rod with its pins and bar.

        Args:
            rod_id: Unique identifier for this rod
            isRainbow: Whether to enable rainbow color effects
            pendulum_type: Type of pendulum system this rod belongs to
            trace_points_colour: Color for trace visualization
            pins_info: Configuration data for the pins
            bar_info: Configuration data for the bar
            angular_position: Initial angular position in radians
        """
        self.angular_position = angular_position
        self.angular_velocity = 0.0
        self.rod_id = rod_id
        self.type = pendulum_type
        self.pin_1 = Pin(
            1,
            rod_id,
            isRainbow,
            pins_info[4],
            0,
            5,
            pins_info[2][0],
            trace_points_colour,
            pins_info[3],
        )
        self.pin_2 = Pin(
            2,
            rod_id,
            isRainbow,
            self._create_pin2_position(pins_info[4], bar_info[1]),
            pins_info[0],
            pins_info[1],
            pins_info[2][1],
            trace_points_colour,
            pin_friction=0,
        )
        self.bar = Bar(*bar_info)

    def get_info(self) -> List[Union[float, int, bool]]:
        """
        Get information about this rod's configuration.

        Returns:
            List containing friction, length, weight, radius, and trace settings
        """
        return [
            self.pin_1.friction,
            self.bar.length,
            self.pin_2.weight,
            self.pin_2.radius,
            self.pin_2.trace_points_isOn,
            self.pin_2.trace_points_isLine,
        ]

    def _create_pin2_position(
        self, pin1_position: Position, bar_length: float
    ) -> Position:
        """
        Calculate the position of pin 2 based on pin 1 and bar length.

        Args:
            pin1_position: Position of the first pin
            bar_length: Length of the connecting bar

        Returns:
            [x, y] position of the second pin
        """
        return [
            pin1_position[0] + bar_length * math.sin(self.angular_position),
            pin1_position[1] + bar_length * math.cos(self.angular_position),
        ]

    def update(self) -> None:
        """
        Update the rod's pin positions based on current angular position.
        """
        p2_position = self._create_pin2_position(self.pin_1.position, self.bar.length)
        self.pin_2.update_pos(p2_position)


class Bar:
    """
    Rigid bar component connecting two pins in a pendulum rod.

    The bar provides the rigid connection between pins and carries physical
    properties like length, weight, and visual appearance.

    Attributes:
        length (float): Length of the bar
        weight (float): Mass of the bar
        width (int): Visual width for rendering
        colour (Color): RGB color of the bar
    """

    def __init__(self, weight: float, length: float, width: int, colour: Color) -> None:
        """
        Initialize a bar with physical and visual properties.

        Args:
            weight: Mass of the bar
            length: Length of the bar
            width: Visual width for rendering
            colour: RGB color tuple
        """
        self.length = length
        self.weight = weight
        self.width = width
        self.colour = colour

    def update(self) -> None:
        """
        Update the bar state.

        Currently a placeholder for future bar-specific updates.
        """
        pass

    def change_length(self, length: float) -> None:
        """
        Change the length of the bar.

        Args:
            length: New length value
        """
        self.length = length


class Pin:
    """
    Mass point in the pendulum system with position and physics properties.

    A pin represents a point mass that can have weight, friction, and visual
    properties. Pin 2 in each rod typically has trace visualization.

    Attributes:
        pin_vector (pygame.math.Vector2): Position vector for efficient calculations
        x, y (float): Individual coordinate components
        position (Position): [x, y] position list
        pin_id (int): Pin identifier (1 or 2)
        rod_id (int): ID of the rod this pin belongs to
        weight (float): Mass of the pin
        radius (int): Visual radius for rendering
        colour (Color): RGB color of the pin
        friction (Optional[float]): Friction coefficient
        trace_points (List[Position]): History of positions for trace visualization
        trace_points_length (int): Maximum number of trace points to keep
        trace_points_colour (Optional[Color]): Color of trace points
        trace_points_isLine (bool): Whether to draw trace as lines
        trace_points_isOn (bool): Whether trace visualization is enabled
        isRainbow (bool): Whether to use rainbow color effects
        RAINBOW_step_direction (int): Direction for rainbow color cycling
    """

    def __init__(
        self,
        pin_id: int,
        rod_id: int,
        isRainbow: bool,
        position: Position,
        weight: float,
        radius: int,
        colour: Color,
        trace_pcolour: Optional[Color] = None,
        pin_friction: Optional[float] = None,
    ) -> None:
        """
        Initialize a pin with position and physical properties.

        Args:
            pin_id: Pin identifier (1 or 2)
            rod_id: ID of the rod this pin belongs to
            isRainbow: Whether to enable rainbow color effects
            position: Initial [x, y] position
            weight: Mass of the pin
            radius: Visual radius for rendering
            colour: RGB color of the pin
            trace_pcolour: Color for trace points (optional)
            pin_friction: Friction coefficient (optional)
        """
        self.pin_vector = pygame.math.Vector2(position)
        self.x = self.pin_vector.x
        self.y = self.pin_vector.y
        self.position = [self.x, self.y]
        self.pin_id = pin_id
        self.rod_id = rod_id
        self.weight = weight
        self.radius = radius
        self.colour = colour
        self.friction = pin_friction
        self.trace_points: List[Position] = []
        self.trace_points_length = TRACE_POINTS_LENGTH
        self.trace_points_colour = trace_pcolour
        self.trace_points_isLine = True
        self.trace_points_isOn = True
        self.isRainbow = isRainbow
        self.RAINBOW_step_direction = 0

    def update_pos(self, new_pos: Position) -> None:
        """
        Update the pin's position and handle trace point generation.

        Args:
            new_pos: New [x, y] position
        """
        self.pin_vector.update(new_pos[0], new_pos[1])
        self.x = self.pin_vector.x
        self.y = self.pin_vector.y
        self.position = [self.x, self.y]
        if self.pin_id == 2:
            self.calc_trace_points()
            if self.isRainbow:
                newColour, self.RAINBOW_step_direction = colour.changeRAINBOW(
                    self.trace_points_colour, self.RAINBOW_step_direction
                )
                self.trace_points_colour = newColour

    def calc_trace_points(self) -> None:
        """
        Calculate and store trace points for visualization.

        Maintains a rolling buffer of position history for drawing traces.
        """
        if len(self.trace_points) < self.trace_points_length:
            self.trace_points.append(self.position[:])
        else:
            self.trace_points.pop(0)
            self.trace_points.append(self.position[:])

    def change_friction(self, friction: float) -> None:
        """
        Change the friction coefficient of the pin.

        Args:
            friction: New friction coefficient
        """
        self.friction = friction

    def change_weight(self, weight: float) -> None:
        """
        Change the mass of the pin.

        Args:
            weight: New weight/mass value
        """
        self.weight = weight

    def change_radius(self, radius: int) -> None:
        """
        Change the visual radius of the pin.

        Args:
            radius: New radius for rendering
        """
        self.radius = radius

    def change_trace_points(self) -> None:
        """
        Placeholder method for trace point modifications.

        Currently unused but available for future trace customization.
        """
        pass
