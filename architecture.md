# Pendulum Demo Architecture

This document describes the architecture of the Pendulum Demo application, which has been refactored to use a manager-based design pattern.

## Overview

The application has been restructured to use separate manager classes that handle specific aspects of the application:

1. **StateManager**: Handles application state transitions and state-specific logic
2. **UIManager**: Manages UI components and their rendering
3. **EventManager**: Processes and dispatches events
4. **RenderManager**: Handles all rendering operations

This separation of concerns makes the code more maintainable, easier to understand, and more extensible.

## State Flow

The application follows this state flow:

1. **STARTUP**: Initial state that initializes everything and transitions to STARTMENU
2. **STARTMENU**: Main menu with options to start simulation, view about page, or quit
3. **SIMULATION**: Active simulation state with pendulums and sidebar UI
4. **ABOUTMENU**: Information about the application
5. **QUIT**: Exit state

## Manager Classes

### StateManager

The StateManager is responsible for:
- Tracking the current and previous application states
- Handling state transitions with proper setup/teardown
- Initializing pendulums when entering the simulation state
- Coordinating with other managers during state changes

### UIManager

The UIManager is responsible for:
- Creating and managing UI components for each state
- Handling sidebar states in the simulation (INFO, CREATE, EDIT)
- Drawing UI components to the screen
- Providing interfaces for other managers to interact with UI

### EventManager

The EventManager is responsible for:
- Processing pygame events
- Dispatching events to appropriate handlers based on the current state
- Handling pendulum interaction events
- Coordinating with other managers for event responses

### RenderManager

The RenderManager is responsible for:
- Managing rendering timing and physics updates
- Rendering the simulation, menu, and about screens
- Coordinating with the UIManager for UI rendering
- Handling frame rate and display updates

## Sidebar States in Simulation

The simulation state has three sidebar states:

1. **INFO**: Displays instructions and simulation controls
2. **CREATE**: Provides options to create new pendulums
3. **EDIT**: Allows editing of selected pendulums

## Benefits of the New Architecture

1. **Separation of Concerns**: Each manager handles a specific aspect of the application
2. **Reduced Complexity**: State transitions and UI management are centralized
3. **Improved Maintainability**: Changes to one aspect don't affect others
4. **Better Extensibility**: New states or features can be added more easily
5. **Clearer Code Flow**: The application flow is more explicit and easier to follow

## Implementation Details

The managers are connected through references to each other, allowing them to coordinate their actions. The main application creates and connects these managers, then starts the application in the STARTUP state.

The state transitions are handled by the StateManager, which calls appropriate methods on other managers to update the application state. The UI is created and managed by the UIManager, events are processed by the EventManager, and rendering is handled by the RenderManager.

This architecture provides a solid foundation for further development and enhancement of the Pendulum Demo application. 