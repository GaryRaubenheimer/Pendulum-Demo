import constants
import random
import colour

# Import specific classes instead of wildcard imports from correct modules
from Widgets import Label, Button, Slider, ToggleButton, RadioButton
from Pendulum import Pendulum
from game_context import get_pygame
from constants import WIDTH, HEIGHT, SINGLE, DOUBLE
from colour import (
    BLUE,
    RED,
    LIGHT_BLUE,
    LIGHT_CYAN,
    GREEN,
    LIGHT_GREY,
    BLACK,
    DARK_GREY,
    RAINBOW,
)

# Get pygame instance from game context
pygame = get_pygame()

slot_height = 40
x_offset = 20
y_offset = 5


class SidebarState:
    def __init__(self, sidebar):
        self.sidebar = sidebar
        self.gui_widget_list = {}
    
    def enter(self):
        """Called when entering this state"""
        self.initialize_widgets()
        
    def exit(self):
        """Called when exiting this state"""
        self.sidebar.kill_gui_widget_list()
        
    def initialize_widgets(self):
        """Initialize widgets for this state"""
        pass
        
    def handle_event(self, event):
        """Handle events for this state"""
        pass

class InfoState(SidebarState):
    def initialize_widgets(self):
        self.sidebar.gui_widget_list = {
            "labels": self.sidebar.create_Sidebar_label_dict(x_offset, y_offset, slot_height),
            "buttons": self.sidebar.create_Sidebar_button_dict(x_offset, y_offset, slot_height),
            "sliders": self.sidebar.create_Sidebar_slider_dict(x_offset, y_offset, slot_height),
        }

class CreateState(SidebarState):
    def initialize_widgets(self):
        self.sidebar.gui_widget_list = {
            "labels": self.create_createPendulum_label_dict(x_offset, y_offset, slot_height),
            "buttons": self.create_createPendulum_button_dict(x_offset, y_offset, slot_height),
            "sliders": self.create_createPendulum_slider_dict(x_offset, y_offset, slot_height),
        }

    def create_createPendulum_label_dict(self, x_offset, y_offset, slot_height):
        return {
            "label_createPendulum": Label(x_offset, y_offset, "Create Pendulum :", 37),
            "label_quickAddPendulum": Label(
                x_offset, y_offset + slot_height * 1, "Quick add new Pendulum:"
            ),
        }

    def create_createPendulum_button_dict(self, x_offset, y_offset, slot_height):
        return {
            "SinglePendulum_button": Button(
                x_offset,
                slot_height * 2,
                150,
                40,
                BLUE,
                LIGHT_BLUE,
                "Single Pendulum",
                action=self.create_newSinglePendulum,
            ),
            "DoublePendulum_button": Button(
                x_offset,
                slot_height * 3 + 10,
                150,
                40,
                BLUE,
                LIGHT_BLUE,
                "Double Pendulum",
                action=self.create_newDoublePendulum,
            ),
            "back_button": Button(
                x_offset,
                slot_height * 15,
                150,
                40,
                BLUE,
                RED,
                "Back",
                action=self.change_sidebarStateToInfo,
            ),
        }

    def create_createPendulum_slider_dict(self, x_offset, y_offset, slot_height):
        return {}

    def create_newSinglePendulum(self):
        randomColour = random.randint(0, 1)
        w = WIDTH / 4 * 3 / 2
        h = HEIGHT / 2
        random_xPosition = random.randint(int(w - (w / 1.2)), int(w + (w / 1.2)))
        random_yPosition = random.randint(
            int(h - (h / 1.2)) - 50, int(h + (h / 1.2)) - 50
        )
        if randomColour:
            constants.pen_array.extend(
                [
                    Pendulum(
                        SINGLE,
                        [random_xPosition, random_yPosition],
                        colour.get_RANDOM_COLOUR(),
                        isRainbow=False,
                    )
                ]
            )
        else:
            constants.pen_array.extend(
                [
                    Pendulum(
                        SINGLE,
                        [random_xPosition, random_yPosition],
                        RAINBOW,
                        isRainbow=True,
                    )
                ]
            )

    def create_newDoublePendulum(self):
        randomColour = random.randint(0, 1)
        w = WIDTH / 4 * 3 / 2
        h = HEIGHT / 2
        random_xPosition = random.randint(int(w - (w / 1.2)), int(w + (w / 1.2)))
        random_yPosition = random.randint(
            int(h - (h / 1.5)) - 50, int(h + (h / 1.5)) - 50
        )
        if randomColour:
            constants.pen_array.extend(
                [
                    Pendulum(
                        DOUBLE,
                        [random_xPosition, random_yPosition],
                        colour.get_RANDOM_COLOUR(),
                        isRainbow=False,
                    )
                ]
            )
        else:
            constants.pen_array.extend(
                [
                    Pendulum(
                        DOUBLE,
                        [random_xPosition, random_yPosition],
                        RAINBOW,
                        isRainbow=True,
                    )
                ]
            )

    def change_sidebarStateToInfo(self):
        self.sidebar.change_sidebar_state("INFO")

class EditState(SidebarState):
    def __init__(self, sidebar):
        super().__init__(sidebar)
        self.selected_pendulum = None
        self.selected_rod = None

    def initialize_widgets(self):
        self.sidebar.gui_widget_list = {
            "labels": self.create_guiEdit_label_dict(x_offset, y_offset, slot_height),
            "toggleButtons": self.create_guiEdit_toggleButton_dict(x_offset, y_offset, slot_height),
            "radioButtons": self.create_guiEdit_radioButton_dict(x_offset, y_offset, slot_height),
            "buttons": self.create_guiEdit_button_dict(x_offset, y_offset, slot_height),
            "sliders": self.create_guiEdit_slider_dict(x_offset, y_offset, slot_height),
        }

    def create_guiEdit_label_dict(self, x_offset, y_offset, slot_height):
        return {
            "label_Pendulum_Number": Label(x_offset, y_offset, "Pendulum Edit:", 37),
            "label_Rod_Number": Label(x_offset, y_offset + slot_height * 1, "Rod Selection:"),
            "label_Pin_Friction": Label(x_offset, y_offset + slot_height * 3, "Pin Friction:"),
            "label_Rod_Length": Label(x_offset, y_offset + slot_height * 5, "Rod Length:"),
            "label_Bob_Weight": Label(x_offset, y_offset + slot_height * 7, "Bob Weight:"),
            "label_Bob_Radius": Label(x_offset, y_offset + slot_height * 9, "Bob Radius:"),
            "label_Trace_Points": Label(x_offset, y_offset + slot_height * 11, "Trace Points On/Off:"),
            "label_TP_Off": Label(x_offset + 15, y_offset + slot_height * 12 - 10, "Off"),
            "label_TP_Dot": Label(x_offset + 75, y_offset + slot_height * 12 - 10, "Dot"),
            "label_TP_Line": Label(x_offset + 165, y_offset + slot_height * 12 - 10, "Line"),
        }

    def create_guiEdit_toggleButton_dict(self, x_offset, y_offset, slot_height):
        return {
            "toggle_button_rod1": ToggleButton(
                x_offset,
                slot_height * 2 - 10,
                100,
                35,
                "ROD 1",
                is_linked=True,
                is_active=True,
                action=self.change_rod_selection,
            ),
        }

    def create_guiEdit_radioButton_dict(self, x_offset, y_offset, slot_height):
        return {
            "radio_button_off": RadioButton(
                x_offset,
                y_offset + slot_height * 12,
                10,
                LIGHT_GREY,
                BLACK,
                DARK_GREY,
                is_checked=False,
                action=self.change_trace_points_off,
            ),
            "radio_button_points": RadioButton(
                x_offset + 60,
                y_offset + slot_height * 12,
                10,
                LIGHT_GREY,
                BLACK,
                DARK_GREY,
                is_checked=False,
                action=self.change_trace_points_dot,
            ),
            "radio_button_lines": RadioButton(
                x_offset + 150,
                y_offset + slot_height * 12,
                10,
                LIGHT_GREY,
                BLACK,
                DARK_GREY,
                is_checked=False,
                action=self.change_trace_points_line,
            ),
        }

    def create_guiEdit_button_dict(self, x_offset, y_offset, slot_height):
        return {
            "back_button": Button(
                x_offset,
                slot_height * 15,
                150,
                40,
                BLUE,
                RED,
                "Back",
                action=self.change_sidebarStateToInfo,
            )
        }

    def create_guiEdit_slider_dict(self, x_offset, y_offset, slot_height):
        return {
            "slider_pin_friction": Slider(
                x_offset + 5,
                slot_height * 4,
                250,
                10,
                0,
                0,
                1,
                action=self.change_friction,
            ),
            "slider_rod_length": Slider(
                x_offset + 5,
                slot_height * 6,
                250,
                10,
                25,
                25,
                250,
                action=self.change_length,
            ),
            "slider_bob_weight": Slider(
                x_offset + 5,
                slot_height * 8,
                250,
                10,
                1,
                1,
                50,
                action=self.change_weight,
            ),
            "slider_bob_radius": Slider(
                x_offset + 5,
                slot_height * 10,
                250,
                10,
                5,
                5,
                35,
                action=self.change_radius,
            ),
        }

    def change_sidebarStateToInfo(self):
        self.sidebar.change_sidebar_state("INFO")

    def get_pen_info(self, pen):
        rods_info = []
        pen_type = None
        if pen.isSelected:
            self.selected_pendulum = pen
            self.selected_rod = pen.rods[0]
            info_list = pen.get_info()
            pen_type = info_list[0]
            if len(info_list) == 2:
                t1 = info_list[1]
                rods_info.append(t1[:])
            else:
                t1 = info_list[1]
                t2 = info_list[2]
                rods_info.append(t1[:])
                rods_info.append(t2[:])
        return pen_type, rods_info

    def change_guiEdit_widget_info(self, pen):
        pen_type, rods_info = self.get_pen_info(pen)

        if pen_type == SINGLE:
            self.toggleButton_dict_remove_rod2()
        else:
            self.toggleButton_dict_add_rod2(x_offset, y_offset, slot_height)

        for category, widgets in self.sidebar.gui_widget_list.items():
            for name, widget in widgets.items():
                if name == "toggle_button_type":
                    if pen_type == SINGLE:
                        widget.change_value_to(True)
                    else:
                        widget.change_value_to(False)

                self.change_guiEdit_widget_slider_info(name, widget, rods_info[0])

                if name == "radio_button_off":
                    if rods_info[0][4]:
                        widget.change_value_to(False)
                    else:
                        widget.change_value_to(True)

                if name == "radio_buttons_lines":
                    if rods_info[0][5]:
                        widget.change_value_to(True)
                    else:
                        widget.change_value_to(False)

        self.check_trace_point_state()

    def change_guiEdit_widget_slider_info(self, name, widget, rod_info):
        if name == "slider_pin_friction":
            widget.change_value_to(rod_info[0])
        elif name == "slider_rod_length":
            widget.change_value_to(rod_info[1])
        elif name == "slider_bob_weight":
            widget.change_value_to(rod_info[2])
        elif name == "slider_bob_radius":
            widget.change_value_to(rod_info[3])
        return widget

    def toggleButton_dict_add_rod2(self, x_offset, y_offset, slot_height):
        for category, widgets in self.sidebar.gui_widget_list.items():
            if category == "toggleButtons":
                widgets.update({
                    "toggle_button_rod2": ToggleButton(
                        x_offset + 150,
                        slot_height * 2 - 10,
                        100,
                        35,
                        "ROD 2",
                        is_linked=True,
                        is_active=False,
                        action=self.change_rod_selection,
                    )
                })
        return self.sidebar.gui_widget_list

    def toggleButton_dict_remove_rod2(self):
        toggle_buttons = list(self.sidebar.gui_widget_list.get("toggleButtons", {}).keys())
        for key in toggle_buttons:
            if key == "toggle_button_rod2":
                self.sidebar.gui_widget_list["toggleButtons"].pop(key)
        return self.sidebar.gui_widget_list

    def change_rod_selection(self, rod_select_Button):
        if rod_select_Button.text == "ROD 1":
            if rod_select_Button.is_active == False:
                for category, widgets in self.sidebar.gui_widget_list.items():
                    if category == "toggleButtons":
                        for name, widget in widgets.items():
                            if name == "toggle_button_rod1":
                                widget.toggle()
                                self.selected_rod = self.selected_pendulum.rods[0]
                                rod_info = self.selected_rod.get_info()
                                for cat, wids in self.sidebar.gui_widget_list.items():
                                    if cat == "sliders":
                                        for name, widget in wids.items():
                                            self.change_guiEdit_widget_slider_info(name, widget, rod_info)
                            elif name == "toggle_button_rod2":
                                widget.toggle()
        elif rod_select_Button.text == "ROD 2":
            if rod_select_Button.is_active == False:
                for category, widgets in self.sidebar.gui_widget_list.items():
                    if category == "toggleButtons":
                        for name, widget in widgets.items():
                            if name == "toggle_button_rod1":
                                widget.toggle()
                            elif name == "toggle_button_rod2":
                                widget.toggle()
                                self.selected_rod = self.selected_pendulum.rods[1]
                                rod_info = self.selected_rod.get_info()
                                for cat, wids in self.sidebar.gui_widget_list.items():
                                    if cat == "sliders":
                                        for name, widget in wids.items():
                                            self.change_guiEdit_widget_slider_info(name, widget, rod_info)

    def change_length(self, slider_length):
        self.selected_rod.bar.change_length(slider_length.get_real_value())

    def change_friction(self, slider_friction):
        self.selected_rod.pin_1.change_friction(slider_friction.get_real_value())

    def change_weight(self, slider_weight):
        self.selected_rod.pin_2.change_weight(slider_weight.get_real_value())

    def change_radius(self, slider_radius):
        self.selected_rod.pin_2.change_radius(slider_radius.get_real_value())

    def check_trace_point_state(self):
        for rod in self.selected_pendulum.rods:
            if rod.pin_2.trace_points_isLine == False and rod.pin_2.trace_points_isOn == False:
                if self.sidebar.gui_widget_list:
                    for category, widgets in self.sidebar.gui_widget_list.items():
                        for name, widget in widgets.items():
                            if isinstance(widget, RadioButton):
                                if name == "radio_button_off":
                                    widget.change_value_to(True)
                                if name == "radio_button_points":
                                    widget.change_value_to(False)
                                if name == "radio_button_lines":
                                    widget.change_value_to(False)
            elif rod.pin_2.trace_points_isLine == True and rod.pin_2.trace_points_isOn == True:
                if self.sidebar.gui_widget_list:
                    for category, widgets in self.sidebar.gui_widget_list.items():
                        for name, widget in widgets.items():
                            if isinstance(widget, RadioButton):
                                if name == "radio_button_off":
                                    widget.change_value_to(False)
                                if name == "radio_button_points":
                                    widget.change_value_to(False)
                                if name == "radio_button_lines":
                                    widget.change_value_to(True)
            elif rod.pin_2.trace_points_isLine == False and rod.pin_2.trace_points_isOn == True:
                if self.sidebar.gui_widget_list:
                    for category, widgets in self.sidebar.gui_widget_list.items():
                        for name, widget in widgets.items():
                            if isinstance(widget, RadioButton):
                                if name == "radio_button_off":
                                    widget.change_value_to(False)
                                if name == "radio_button_points":
                                    widget.change_value_to(True)
                                if name == "radio_button_lines":
                                    widget.change_value_to(False)

    def change_trace_points_off(self, radioButton_trace_points):
        if radioButton_trace_points:
            for rod in self.selected_pendulum.rods:
                rod.pin_2.trace_points_isLine = False
                rod.pin_2.trace_points_isOn = False
        if self.sidebar.gui_widget_list:
            for category, widgets in self.sidebar.gui_widget_list.items():
                for name, widget in widgets.items():
                    if isinstance(widget, RadioButton):
                        if name == "radio_button_off":
                            widget.change_value_to(True)
                        if name == "radio_button_points":
                            widget.change_value_to(False)
                        if name == "radio_button_lines":
                            widget.change_value_to(False)

    def change_trace_points_dot(self, radioButton_trace_points):
        if radioButton_trace_points:
            for rod in self.selected_pendulum.rods:
                rod.pin_2.trace_points_isLine = False
                rod.pin_2.trace_points_isOn = True
        if self.sidebar.gui_widget_list:
            for category, widgets in self.sidebar.gui_widget_list.items():
                for name, widget in widgets.items():
                    if isinstance(widget, RadioButton):
                        if name == "radio_button_off":
                            widget.change_value_to(False)
                        if name == "radio_button_points":
                            widget.change_value_to(True)
                        if name == "radio_button_lines":
                            widget.change_value_to(False)

    def change_trace_points_line(self, radioButton_trace_points):
        if radioButton_trace_points:
            for rod in self.selected_pendulum.rods:
                rod.pin_2.trace_points_isLine = True
                rod.pin_2.trace_points_isOn = True
        if self.sidebar.gui_widget_list:
            for category, widgets in self.sidebar.gui_widget_list.items():
                for name, widget in widgets.items():
                    if isinstance(widget, RadioButton):
                        if name == "radio_button_off":
                            widget.change_value_to(False)
                        if name == "radio_button_points":
                            widget.change_value_to(False)
                        if name == "radio_button_lines":
                            widget.change_value_to(True)

class Gui:
    def __init__(self):
        self.gui_widget_list = []
        self.state = None
        self.inCreate = False
        self.was_inCreate = False

    def __del__(self):
        self.kill_gui_widget_list()

    def kill_gui_widget_list(self):
        self.gui_widget_list = []

class gui_Sidebar(Gui):
    def __init__(self):
        super().__init__()
        self.display = pygame.Surface((WIDTH / 4, HEIGHT))
        self.state = "SIDEBAR"
        self.sidebarState = "INFO"
        self.states = {
            "INFO": InfoState(self),
            "CREATE": CreateState(self),
            "EDIT": EditState(self)
        }
        self.current_state = self.states["INFO"]
        self.current_state.enter()
        self.state_manager = None
        self.inCreate = False

    def set_state_manager(self, state_manager):
        self.state_manager = state_manager

    def draw(self):
        self.display.fill(LIGHT_CYAN)
        if len(self.gui_widget_list) != 0:
            for _category, widgets in self.gui_widget_list.items():
                for _name, widget in widgets.items():
                    widget.draw(self.display)

    def change_sidebar_state(self, newState):
        if newState in self.states and newState != self.sidebarState:
            self.current_state.exit()
            self.sidebarState = newState
            self.current_state = self.states[newState]
            self.inCreate = (newState == "CREATE")
            self.current_state.enter()

    def change_sidebarStateToCreate(self):
        self.change_sidebar_state("CREATE")

    def change_sidebarStateToEdit(self, pendulum):
        self.change_sidebar_state("EDIT")
        if isinstance(self.current_state, EditState):
            self.current_state.change_guiEdit_widget_info(pendulum)

    def change_GuiToMenu(self):
        self.state = "MENU"
        self.kill_gui_widget_list()
        if self.state_manager:
            self.state_manager.change_state(self.state_manager.STARTMENU)

    def initialize_Sidebar(self):
        # Menu UI initialization
        self.gui_widget_list = self.create_Sidebar_widget_list()
        return self.gui_widget_list

    def create_Sidebar_widget_list(self):
        gui_widget_list = {
            "labels": self.create_Sidebar_label_dict(x_offset, y_offset, slot_height),
            "buttons": self.create_Sidebar_button_dict(x_offset, y_offset, slot_height),
            "sliders": self.create_Sidebar_slider_dict(x_offset, y_offset, slot_height),
        }
        return gui_widget_list

    def create_Sidebar_label_dict(self, x_offset, y_offset, slot_height):
        # (x, y, text, font_size=20, color=BLACK)
        label_dict = {
            "label_Sidebar": Label(x_offset, y_offset, "Side Bar:", 37),
            "label_simulationSpeed": Label(
                x_offset, y_offset + slot_height * 2 + 10, "Simulation Speed:"
            ),
            "label_simulationFPS": Label(
                x_offset, y_offset + slot_height * 4, "Simulation FPS:"
            ),
            "label_instructions": Label(
                x_offset, y_offset + slot_height * 6, "Instructions:", 30
            ),
            "label_instructionsLeftClick": Label(
                10, y_offset + slot_height * 6 + 25, "Left Click - To edit Pendulum"
            ),
            "label_instructionsMiddleClick": Label(
                10, y_offset + slot_height * 6 + 60, "Middle Click - To delete Pendulum"
            ),
            "label_instructionsRightClick_Grey1": Label(
                10, y_offset + slot_height * 6 + 95, "Right Click - On GREY node"
            ),
            "label_instructionsRightClick_Grey2": Label(
                20, y_offset + slot_height * 6 + 115, "move whole Pendulum"
            ),
            "label_instructionsRightClick_Red1": Label(
                10, y_offset + slot_height * 6 + 145, "Right Click - On RED node to "
            ),
            "label_instructionsRightClick_Red2": Label(
                20, y_offset + slot_height * 6 + 165, "move and swing the node"
            ),
        }
        return label_dict

    def create_Sidebar_button_dict(self, x_offset, y_offset, slot_height):
        # (x, y, width, height, color, hover_color, text='', font_size=20, text_color=(255, 255, 255), action=None)
        button_dict = {
            "create_button": Button(
                x_offset,
                slot_height * 1,
                150,
                40,
                BLUE,
                RED,
                "Create New Pendulum",
                action=self.change_sidebarStateToCreate,
            ),
            "back_button": Button(
                x_offset,
                slot_height * 15,
                150,
                40,
                BLUE,
                RED,
                "Back to Menu",
                action=self.change_GuiToMenu,
            ),
        }
        return button_dict

    def create_Sidebar_slider_dict(self, x_offset, y_offset, slot_height):
        # (self, x, y, width, height, min_value=0.0, real_value=0.5, max_value=1.0, color=BLUE, action=None)
        slider_dict = {
            "slider_simulated_frames": Slider(
                50,
                y_offset + slot_height * 5 - 10,
                WIDTH / 4 - 100,
                10,
                1,
                constants.fps_factor,
                60,
                RED,
                action=self.change_fps,
            ),
            "slider_simulation_speed": Slider(
                50,
                y_offset + slot_height * 3,
                WIDTH / 4 - 100,
                10,
                min_value=1,
                max_value=20,
                real_value=constants.speed_factor,
                color=GREEN,
                action=self.change_speed,
            ),
        }
        return slider_dict

    def change_speed(self, slider_speed):
        if slider_speed and hasattr(slider_speed, 'get_real_value'):
            speed = slider_speed.get_real_value()
            constants.speed_factor = speed
            print(f"Speed factor updated to: {speed}")

    def change_fps(self, slider_fps):
        if slider_fps and hasattr(slider_fps, 'get_real_value'):
            fps = slider_fps.get_real_value()
            constants.fps_factor = fps
            print(f"FPS factor updated to: {fps}")

    def setRed(self, redValue):
        pass

    def setBlue(self, blueValue):
        pass

    def setGreen(self, greenValue):
        pass

    def change_length(self, slider_length):
        pass

    def change_weight(self, slider_weight):
        pass

    def change_radius(self, slider_radius):
        pass


class gui_startMenu(Gui):
    def __init__(self, display):
        super().__init__()
        self.state = "MENU"
        self.display = display
        self.initialize_startMenuGui()
        self.state_manager = None

    def set_state_manager(self, state_manager):
        self.state_manager = state_manager

    def draw(self):
        if len(self.gui_widget_list) != 0:
            for category, widgets in self.gui_widget_list.items():
                for name, widget in widgets.items():
                    widget.draw(self.display)

    def initialize_startMenuGui(self):
        # Menu UI initialization
        self.gui_widget_list = self.create_startMenu_widget_list()
        return self.gui_widget_list

    def create_startMenu_widget_list(self):
        gui_widget_list = {
            "labels": self.create_guiEdit_label_dict(slot_height),
            "buttons": self.create_guiEdit_button_dict(slot_height),
        }
        return gui_widget_list

    def create_guiEdit_label_dict(self, slot_height):
        # (x, y, text, font_size=20, color=BLACK)
        label_dict = {
            "label_Title_PendulumDemo": Label(
                WIDTH / 2, slot_height * 4, "Pendulum Demo", 80
            )
        }
        return label_dict

    def create_guiEdit_button_dict(self, slot_height):
        # (x, y, width, height, color, hover_color, text='', font_size=20, text_color=(255, 255, 255), action=None)
        button_dict = {
            "start_button": Button(
                WIDTH / 2,
                slot_height * 8,
                150,
                40,
                LIGHT_BLUE,
                BLUE,
                "Start",
                action=self.select_start,
            ),
            "about_button": Button(
                WIDTH / 2,
                slot_height * 10,
                150,
                40,
                LIGHT_BLUE,
                BLUE,
                "About",
                action=self.select_about,
            ),
            "quit_button": Button(
                WIDTH / 2,
                slot_height * 12,
                150,
                40,
                LIGHT_BLUE,
                BLUE,
                "Quit",
                action=self.select_quit,
            ),
        }
        return button_dict

    def select_start(self):
        if self.state_manager:
            self.state_manager.change_state(self.state_manager.SIMULATION)

    def select_about(self):
        if self.state_manager:
            self.state_manager.change_state(self.state_manager.ABOUTMENU)

    def select_quit(self):
        if self.state_manager:
            self.state_manager.change_state(self.state_manager.QUIT)


class gui_aboutMenu(Gui):
    def __init__(self):
        super().__init__()
        self.state = "ABOUTMENU"
        self.display = pygame.Surface((WIDTH, HEIGHT))
        self.initialize_startAboutGui()
        self.state_manager = None

    def set_state_manager(self, state_manager):
        self.state_manager = state_manager

    def initialize_startAboutGui(self):
        # Menu UI initialization
        self.gui_widget_list = self.create_startMenu_widget_list()
        return self.gui_widget_list

    def draw(self):
        self.display.fill(LIGHT_CYAN)
        if len(self.gui_widget_list) != 0:
            for category, widgets in self.gui_widget_list.items():
                for name, widget in widgets.items():
                    widget.draw(self.display)

    def create_startMenu_widget_list(self):
        gui_widget_list = {
            "labels": self.create_guiEdit_label_dict(x_offset, y_offset, slot_height),
            "buttons": self.create_guiEdit_button_dict(x_offset, y_offset, slot_height),
        }
        return gui_widget_list

    def create_guiEdit_label_dict(self, x_offset, y_offset, slot_height):
        # (x, y, text, font_size=20, color=BLACK)
        label_dict = {
            "label_Title_PendulumDemo": Label(
                WIDTH / 8, slot_height * 1, "About Pendulum Demo", 40
            ),
            "label_Text1_1": Label(
                WIDTH / 10,
                slot_height * 3,
                "The Pendulum Demo project explores the motion of single and double pendulums.",
            ),
            "label_Text1_2": Label(
                WIDTH / 10,
                slot_height * 3 + 25,
                "While single pendulums exhibit predictable behavior, double pendulums showcase chaotic, sensitive motion and instability.",
            ),
            "label_Text2_1": Label(
                WIDTH / 10,
                slot_height * 6,
                "This project was created to learn Pygame, Visual Studio Code, and version control with Git and GitHub, ",
            ),
            "label_Text2_2": Label(
                WIDTH / 10,
                slot_height * 6 + 25,
                "while combining my interest in physics and programming. It demonstrates my ability to build interactive applications",
            ),
        }
        return label_dict

    def create_guiEdit_button_dict(self, x_offset, y_offset, slot_height):
        # (x, y, width, height, color, hover_color, text='', font_size=20, text_color=(255, 255, 255), action=None)
        button_dict = {
            "back_button": Button(
                x_offset,
                slot_height * 15,
                150,
                40,
                LIGHT_BLUE,
                BLUE,
                "Back",
                action=self.select_backToMenu,
            )
        }
        return button_dict

    def select_backToMenu(self):
        self.state = "MENU"
        self.kill_gui_widget_list()
        if self.state_manager:
            self.state_manager.change_state(self.state_manager.STARTMENU)
