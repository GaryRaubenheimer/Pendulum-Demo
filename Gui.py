import constants 

from Widgets import *

slot_height = 40
x_offset = 20
y_offset = 5

class Gui:   
    def __init__(self):
        self.gui_widget_list = []

#---
class gui_Edit(Gui):
    def __init__(self):
        super().__init__()
        self.display = pygame.Surface((WIDTH/4, HEIGHT))
        self.selected_pendulum = None
        self.selected_rod = None

    def draw(self):
        self.display.fill(LIGHT_CYAN)
        if len(self.gui_widget_list) !=0:
            for category, widgets in self.gui_widget_list.items():
                for name, widget in widgets.items():
                    widget.draw(self.display)

    #-- create edit gui widgets

    def initialize_editGui(self):
        # UI initialization
        self.gui_widget_list = self.create_pen_edit_widget_list()
        return self.gui_widget_list
    
    def kill_pen_edit_widget_list(self):
        self.gui_widget_list =[]
    
    def create_pen_edit_widget_list(self):
        gui_widget_list = {
        "labels"         :self.create_guiEdit_lable_dict(x_offset,y_offset,slot_height),
        "toggleButtons"  :self.create_guiEdit_toggleButton_dict(x_offset,y_offset,slot_height),
        "radioButtons"   :self.create_guiEdit_radioButton_dict(x_offset,y_offset,slot_height),
        "buttons"        :self.create_guiEdit_button_dict(x_offset,y_offset,slot_height),
        "sliders"        :self.create_guiEdit_slider_dict(x_offset,y_offset,slot_height)
        }
        return gui_widget_list

    def create_guiEdit_lable_dict(self,x_offset,y_offset,slot_height):
        #(x, y, text, font_size=20, color=BLACK)
        lable_dict = {
        "label_Pendulum_Number": Label(x_offset, y_offset,                 "Pendulum Edit:", 37),
        "label_Pendulum_Type"  : Label(x_offset, y_offset + slot_height*1, "Pendulum Type:"),
        "label_Rod_Number"     : Label(x_offset, y_offset + slot_height*3, "Rod Selection:"),
        "label_Pin_Friction"   : Label(x_offset, y_offset + slot_height*5, "Pin Friction:"),
        "label_Rod_Length"     : Label(x_offset, y_offset + slot_height*7, "Rod Length:"),
        "label_Bob_Weight"     : Label(x_offset, y_offset + slot_height*9, "Bob Weight:"),
        "label_Bob_Radius"     : Label(x_offset, y_offset + slot_height*11,"Bob Radius:"),
        "label_Trace_Points"   : Label(x_offset, y_offset + slot_height*13,"Trace Points On/Off:"),
        "label_TP_Off"         : Label(x_offset+15, y_offset + slot_height*14-10,"Off"),
        "label_TP_Dot"         : Label(x_offset+75, y_offset + slot_height*14-10,"Dot"),
        "label_TP_Line"        : Label(x_offset+165, y_offset + slot_height*14-10,"Line")
        }
        return lable_dict

    def create_guiEdit_toggleButton_dict(self,x_offset,y_offset,slot_height):
        #(x, y, width, height, text, default=True, action=None)
        toggleButton_dict = {
        "toggle_button_type" : ToggleButton(((WIDTH/4)/2)-50, slot_height*2-10, 100, 35, "SINGLE","DOUBLE" ,is_active=True),
        "toggle_button_rod1" : ToggleButton(x_offset, slot_height*4-10, 100, 35, "ROD 1",is_linked = True, is_active=True,action = self.change_rod_selection),
        "toggle_button_rod2" : ToggleButton(x_offset+150, slot_height*4-10, 100, 35, "ROD 2", is_linked = True, is_active = False, action = self.change_rod_selection)
        }
        return toggleButton_dict

    def create_guiEdit_radioButton_dict(self,x_offset,y_offset,slot_height):
        #(x, y, radius, color, check_color, hover_color, action=None)
        radioButton_dict = {
        "radio_button_off"     : RadioButton(x_offset, y_offset + slot_height*14, 10, LIGHT_GREY, BLACK, DARK_GREY, is_checked=True),
        "radio_buttons_points"    : RadioButton(x_offset+60, y_offset + slot_height*14, 10, LIGHT_GREY, BLACK, DARK_GREY,is_checked=False),
        "radio_buttons_lines"    : RadioButton(x_offset+150, y_offset + slot_height*14, 10, LIGHT_GREY, BLACK, DARK_GREY,is_checked=False)
        }
        return radioButton_dict

    def create_guiEdit_button_dict(self,x_offset,y_offset,slot_height):
        #(x, y, width, height, color, hover_color, text='', font_size=20, text_color=(255, 255, 255), action=None)
        button_dict = {
        "confirm_button" : Button(x_offset, slot_height*15, 150, 40, BLUE, RED, "Confirm")
        }
        return button_dict

    def create_guiEdit_slider_dict(self,x_offset,y_offset,slot_height):
        #(x, y, width, height, min_value=0.0, max_value=1.0, initial_value=0.5, color=BLUE, action=None)
        slider_dict = {
        "slider_pin_friction" : Slider(x_offset+5, slot_height*6,  250, 10, 0, 0, 1, action=self.change_friction),
        "slider_rod_length"   : Slider(x_offset+5, slot_height*8,  250, 10, 25, 25, 250, action=self.change_length),
        "slider_bob_weight"   : Slider(x_offset+5, slot_height*10,  250, 10, 1, 1, 50, action=self.change_weight),
        "slider_bob_radius"   : Slider(x_offset+5, slot_height*12,  250, 10, 5, 5, 35, action=self.change_radius)
        }
        return slider_dict
    
    #-- Call function for edit gui

    def get_pen_info(self,pen):
        rods_info = []
        pen_type = None
        if pen.isSelected:
            self.selected_pendulum = pen
            self.selected_rod = pen.rods[0]
            info_list = pen.get_info()
            pen_type = info_list[0]
            if len(info_list)==2:
                t1 = info_list[1]
                rods_info.append(t1[:])
            else:
                t1 = info_list[1]
                t2 = info_list[2]
                rods_info.append(t1[:])
                rods_info.append(t2[:])
        return pen_type,rods_info
    

    def change_guiEdit_widget_info(self,pen):
        pen_type, rods_info = self.get_pen_info(pen)

        if pen_type == SINGLE:
            self.toggleButton_dict_remove_rod2()
        else:
            self.toggleButton_dict_add_rod2(x_offset,y_offset,slot_height)

        for category, widgets in self.gui_widget_list.items():
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

                if name == "radio_buttons_points":
                    if rods_info[0][5]:
                        widget.change_value_to(False)
                    else:
                        widget.change_value_to(True)

    def change_guiEdit_widget_slider_info(self,name,widget,rod_info):
        if name == "slider_pin_friction":
            widget.change_value_to(rod_info[0])
        elif name == "slider_rod_length":
            widget.change_value_to(rod_info[1])
        elif name == "slider_bob_weight":
            widget.change_value_to(rod_info[2])
        elif name == "slider_bob_radius":
            widget.change_value_to(rod_info[3])
        return widget
    
    def toggleButton_dict_add_rod2(self,x_offset,y_offset,slot_height):
        for category, widgets in self.gui_widget_list.items():
            if category == "toggleButtons":
                widgets.update({"toggle_button_rod2" : ToggleButton(x_offset+150, slot_height*4-10, 100, 35, "ROD 2", is_linked = True, is_active = False, action = self.change_rod_selection)})
        return self.gui_widget_list
    
    def toggleButton_dict_remove_rod2(self):
        # Create a copy of the list of keys to iterate over
        toggle_buttons = list(self.gui_widget_list.get("toggleButtons", {}).keys())

        # Iterate over the keys
        for key in toggle_buttons:
            if key == "toggle_button_rod2":
                # Remove the key from the original dictionary
                self.gui_widget_list["toggleButtons"].pop(key)

        return self.gui_widget_list


    #--
    # toggle and change which rod of selected pendulem is selected
    def change_rod_selection(self,rod_select_Button):
        if rod_select_Button.text == "ROD 1":
            if rod_select_Button.is_active == False:
                for category, widgets in self.gui_widget_list.items():
                    if category == "toggleButtons":
                        for name, widget in widgets.items():
                            if name == "toggle_button_rod1":
                                widget.toggle()
                                self.selected_rod = self.selected_pendulum.rods[0]
                                rod_info = self.selected_rod.get_info()
                                for cat, wids in self.gui_widget_list.items():
                                    if cat == "sliders":
                                        for name, widget in wids.items():
                                            self.change_guiEdit_widget_slider_info(name,widget,rod_info)
                            elif name == "toggle_button_rod2":
                                widget.toggle()
        elif rod_select_Button.text == "ROD 2":
            if rod_select_Button.is_active == False:
                for category, widgets in self.gui_widget_list.items():
                    if category == "toggleButtons":
                        for name, widget in widgets.items():
                            if name == "toggle_button_rod1":
                                widget.toggle()
                            elif name == "toggle_button_rod2":
                                widget.toggle()
                                self.selected_rod = self.selected_pendulum.rods[1]
                                rod_info = self.selected_rod.get_info()
                                for cat, wids in self.gui_widget_list.items():
                                    if cat == "sliders":
                                        for name, widget in wids.items():
                                            self.change_guiEdit_widget_slider_info(name,widget,rod_info)

    def change_length(self,silder_lenght):
        self.selected_rod.bar.change_length(silder_lenght.get_real_value())

    def change_friction(self,silder_friction):
        self.selected_rod.pin_1.change_friction(silder_friction.get_real_value())

    def change_weight(self,silder_weight):
        self.selected_rod.pin_2.change_weight(silder_weight.get_real_value())

    def change_radius(self,silder_radius):
        self.selected_rod.pin_2.change_radius(silder_radius.get_real_value())

    def change_trace_points_off(self,radioButton_trace_points):
        pass

    def change_trace_points_dot(self,radioButton_trace_points):
        pass

    def change_trace_points_line(self,radioButton_trace_points):
        pass

    #---


class gui_startMenu(Gui):
    def __init__(self):
        super().__init__()
        global simulationState
        self.display = pygame.Surface((WIDTH, HEIGHT))
        self.initialize_startMenuGui()

    def draw(self):
        self.display.fill(DARK_YELLOW)
        if len(self.gui_widget_list) !=0:
            for category, widgets in self.gui_widget_list.items():
                for name, widget in widgets.items():
                    widget.draw(self.display)

    def initialize_startMenuGui(self):
        # Menu UI initialization
        self.gui_widget_list = self.create_startMenu_widget_list()
        return self.gui_widget_list

    def kill_startMenu_widget_list(self):
        self.gui_widget_list =[]
    
    def create_startMenu_widget_list(self):
        gui_widget_list = {
        "labels"         :self.create_guiEdit_lable_dict(slot_height),
        "buttons"        :self.create_guiEdit_button_dict(slot_height)
        }
        return gui_widget_list
    
    def create_guiEdit_lable_dict(self,slot_height):
        #(x, y, text, font_size=20, color=BLACK)
        lable_dict = {
        "label_Title_PendulumDemo": Label(WIDTH/2, slot_height*4,"Pendulum Demo", 80)
        }
        return lable_dict

    def create_guiEdit_button_dict(self,slot_height):
        #(x, y, width, height, color, hover_color, text='', font_size=20, text_color=(255, 255, 255), action=None)
        button_dict = {
        "start_button" : Button(WIDTH/2, slot_height*8, 150, 40, LIGHT_BLUE, BLUE, "Start",action=self.select_start),
        "about_button" : Button(WIDTH/2, slot_height*10, 150, 40, LIGHT_BLUE, BLUE, "About",action=self.select_about),
        "quit_button" : Button(WIDTH/2, slot_height*12, 150, 40, LIGHT_BLUE, BLUE, "Quit", action=self.select_quit)
        }
        return button_dict
    
    def select_start(self):
        constants.changeState("SIMULATION")
        #print("--" + simulationState)

    def select_about(self):
        constants.changeState("ABOUTMENU")

    def select_quit(self):
        constants.changeState("QUIT")
    
'''
class gui_aboutMenu(Gui):
    def __init__(self):
        super().__init__()
        self.display = pygame.Surface((WIDTH, HEIGHT))

    def draw(self):
        self.display.fill(LIGHT_CYAN)
        if len(self.gui_widget_list) !=0:
            for category, widgets in self.gui_widget_list.items():
                for name, widget in widgets.items():
                    widget.draw(self.display)

    def kill_startMenu_widget_list(self):
        self.gui_widget_list =[]
    
    def create_startMenu_widget_list(self):
        gui_widget_list = {
        "labels"         :self.create_guiEdit_lable_dict(x_offset,y_offset,slot_height),
        "buttons"        :self.create_guiEdit_button_dict(x_offset,y_offset,slot_height)
        }
        return gui_widget_list
    
    def create_guiEdit_lable_dict(self,x_offset,y_offset,slot_height):
        #(x, y, text, font_size=20, color=BLACK)
        pass

    def create_guiEdit_button_dict(self,x_offset,y_offset,slot_height):
        #(x, y, width, height, color, hover_color, text='', font_size=20, text_color=(255, 255, 255), action=None)
        pass
    '''

#---







    # slider = Slider(50, HEIGHT // 2, WIDTH/4-100, 10, 0.5, 5, 0.5, RED)
    # slider_speed = Slider(50, (HEIGHT // 3)*2, WIDTH/4-100, 10, 0.2, 5, 0.208333333, GREEN, action=change_speed)
    # slider_fps = Slider(50, (HEIGHT // 4)*3, WIDTH/4-100, 10, 1, GAME_FRAME_SPEED, 1.016949, DARK_YELLOW, action=change_fps)
    # button = Button(50, HEIGHT // 9, 100, 50, BLUE, RED, "Button 1", action=button_click)
    # radio_button = RadioButton(50, HEIGHT // 4, 20, LIGHT_GREY, BLACK, DARK_GREY, radio_button_action)

    # gui_widget_list.extend([slider, slider_speed, slider_fps, button, radio_button])

# def change_speed(slider_speed):
#     global speed_factor
#     speed_factor = slider_speed.get_real_value()

# def change_fps(slider_fps):
#     global fps_factor
#     fps_factor = slider_fps.get_real_value()
