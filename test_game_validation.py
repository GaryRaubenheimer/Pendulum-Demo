#!/usr/bin/env python3

import unittest
import pygame
import sys
from game_context import get_game_context, get_pygame
from StateManager import StateManager
from UIManager import UIManager
from EventManager import EventManager
from RenderManager import RenderManager
from constants import WIDTH, HEIGHT, GAME_FRAME_SPEED
from Input import Mouse

class GameValidationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment before running tests."""
        pygame.init()
        cls.game_context = get_game_context()
        cls.pygame = get_pygame()
        cls.window = cls.game_context.initialize_display(WIDTH, HEIGHT, "Test Window")
        cls.clock = cls.game_context.get_clock()
        
        # Initialize managers
        cls.state_manager = StateManager()
        cls.ui_manager = UIManager(cls.pygame, cls.window)
        cls.event_manager = EventManager(cls.pygame)
        cls.render_manager = RenderManager(cls.pygame, cls.window)
        
        # Connect managers
        cls.state_manager.set_ui_manager(cls.ui_manager)
        cls.ui_manager.set_state_manager(cls.state_manager)
        cls.event_manager.set_state_manager(cls.state_manager)
        cls.event_manager.set_ui_manager(cls.ui_manager)
        cls.render_manager.set_state_manager(cls.state_manager)
        cls.render_manager.set_ui_manager(cls.ui_manager)
        cls.render_manager.set_clock(cls.clock)
        
        cls.mouse = Mouse()

    def test_initial_state(self):
        """Test initial state is STARTUP -> STARTMENU."""
        self.state_manager.change_state(StateManager.STARTUP)
        # The state manager transitions to STARTMENU after STARTUP
        self.assertEqual(self.state_manager.get_current_state(), StateManager.STARTMENU)

    def test_state_transitions(self):
        """Test all state transitions."""
        # STARTUP -> STARTMENU
        self.state_manager.change_state(StateManager.STARTUP)
        self.assertEqual(self.state_manager.get_current_state(), StateManager.STARTMENU)
        
        # STARTMENU -> SIMULATION
        self.state_manager.change_state(StateManager.SIMULATION)
        self.assertEqual(self.state_manager.get_current_state(), StateManager.SIMULATION)
        
        # SIMULATION -> STARTMENU
        self.state_manager.change_state(StateManager.STARTMENU)
        self.assertEqual(self.state_manager.get_current_state(), StateManager.STARTMENU)
        
        # STARTMENU -> ABOUTMENU
        self.state_manager.change_state(StateManager.ABOUTMENU)
        self.assertEqual(self.state_manager.get_current_state(), StateManager.ABOUTMENU)
        
        # ABOUTMENU -> STARTMENU
        self.state_manager.change_state(StateManager.STARTMENU)
        self.assertEqual(self.state_manager.get_current_state(), StateManager.STARTMENU)
        
        # STARTMENU -> QUIT
        self.state_manager.change_state(StateManager.QUIT)
        self.assertEqual(self.state_manager.get_current_state(), StateManager.QUIT)

    def test_ui_components(self):
        """Test UI components in different states."""
        # Test STARTMENU components
        self.state_manager.change_state(StateManager.STARTMENU)
        self.assertTrue(hasattr(self.ui_manager, 'menu_display'))
        
        # Test SIMULATION components
        self.state_manager.change_state(StateManager.SIMULATION)
        self.assertTrue(hasattr(self.ui_manager, 'simulation_display'))
        
        # Test ABOUTMENU components
        self.state_manager.change_state(StateManager.ABOUTMENU)
        self.ui_manager.create_about_menu()
        self.assertEqual(self.ui_manager.current_ui_type, self.ui_manager.ABOUT)
        self.assertIsNotNone(self.ui_manager.current_ui)

    def test_simulation_initialization(self):
        """Test simulation initialization."""
        self.state_manager.change_state(StateManager.SIMULATION)
        # Check if simulation display is created
        self.assertTrue(hasattr(self.ui_manager, 'simulation_display'))
        
        # Test going back to menu and returning
        self.state_manager.change_state(StateManager.STARTMENU)
        self.state_manager.change_state(StateManager.SIMULATION)
        self.assertTrue(hasattr(self.ui_manager, 'simulation_display'))

    def test_render_surfaces(self):
        """Test rendering surfaces in different states."""
        # Test STARTMENU rendering
        self.state_manager.change_state(StateManager.STARTMENU)
        self.assertTrue(hasattr(self.ui_manager, 'menu_display'))
        
        # Test SIMULATION rendering
        self.state_manager.change_state(StateManager.SIMULATION)
        self.assertTrue(hasattr(self.ui_manager, 'simulation_display'))

    def test_event_handling(self):
        """Test event handling in different states."""
        # Create test events
        mouse_pos = (WIDTH // 2, HEIGHT // 2)
        mouse_click = pygame.event.Event(pygame.MOUSEBUTTONDOWN, 
                                       {'pos': mouse_pos, 'button': 1})
        
        # Test menu events
        self.state_manager.change_state(StateManager.STARTMENU)
        events = [mouse_click]
        running = True
        running, _ = self.event_manager.process_events(running, self.mouse)
        self.event_manager.handle_menu_events(events, self.mouse, 16)
        
        # Test simulation events
        self.state_manager.change_state(StateManager.SIMULATION)
        self.event_manager.handle_simulation_events(events, self.mouse, 16)
        
        # Test about events
        self.state_manager.change_state(StateManager.ABOUTMENU)
        self.event_manager.handle_about_events(events, self.mouse, 16)

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests."""
        pygame.quit()

def run_validation():
    """Run validation tests during program execution."""
    test_suite = GameValidationTest()
    test_suite.setUpClass()
    
    # Run all test methods
    test_methods = [method for method in dir(GameValidationTest) 
                   if method.startswith('test_')]
    
    results = []
    for method in test_methods:
        try:
            getattr(test_suite, method)()
            results.append(f"✓ {method} passed")
        except AssertionError as e:
            results.append(f"✗ {method} failed: {str(e)}")
        except Exception as e:
            results.append(f"✗ {method} error: {str(e)}")
    
    return results

if __name__ == '__main__':
    unittest.main() 