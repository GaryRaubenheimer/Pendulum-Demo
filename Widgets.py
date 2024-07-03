from Pendulum_Demo import pygame
from colour import *


class RadioButton:
    def __init__(self, x, y, radius, color, check_color, hover_color, action=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.check_color = check_color
        self.hover_color = hover_color
        self.action = action
        self.is_checked = False
        self.is_hovered = False

    def draw(self, screen):
        # Change color based on hover state
        color = self.hover_color if self.is_hovered else self.color

        # Draw radio button circle
        pygame.draw.circle(screen, color, (self.x, self.y), self.radius)

        # Draw check mark if checked
        if self.is_checked:
            pygame.draw.circle(screen, self.check_color, (self.x, self.y), self.radius // 2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_checked = not self.is_checked
                if self.action:
                    self.action(self.is_checked)

    @property
    def rect(self):
        # Create a rect for collision detection
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)


class Button:
    def __init__(self, x, y, width, height, color, hover_color, text='', font_size=20, text_color=(255, 255, 255), action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.text_color = text_color
        self.action = action
        self.is_hovered = False

    def draw(self, screen):
        # Change color based on hover state
        color = self.hover_color if self.is_hovered else self.color

        # Draw button rectangle
        pygame.draw.rect(screen, color, self.rect)

        # Draw button text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and self.action:
                self.action()


class Slider:
    def __init__(self, x, y, width, height, min_value=0.0, max_value=1.0, initial_value=0.5, color=BLUE,action=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.real_value = (self.max_value-self.min_value)*self.value #+ self.min_value
        self.color = color
        self.dragging = False
        self.slider_button_radius = 10
        self.action = action

    def draw(self, screen):
        # Draw slider background
        pygame.draw.rect(screen, LIGHT_GREY, (self.x, self.y - self.height // 2, self.width, self.height))
        
        # Draw slider button
        slider_button_x = int(self.x + self.width * self.value)
        pygame.draw.circle(screen, self.color, (slider_button_x, self.y), self.slider_button_radius)
        
        # Draw slider value text
        font = pygame.font.Font(None, 36)
        text = font.render(f'{self.real_value:.2f}', True, (0, 0, 0))
        screen.blit(text, (slider_button_x - text.get_width() // 2, self.y + 20))

    def update(self):
        if self.dragging:
            mouse_x, _ = pygame.mouse.get_pos()
            self.value = max(0, (min((mouse_x-self.x) ,self.width)))/self.width 
            self.real_value = (self.max_value-self.min_value)*self.value + self.min_value
            if self.action != None:
                self.action(self)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            slider_button_x = int(self.x + self.width * self.value)
            if slider_button_x - self.slider_button_radius <= mouse_x <= slider_button_x + self.slider_button_radius and self.y - self.slider_button_radius <= mouse_y <= self.y + self.slider_button_radius:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

    def get_value(self):
        return self.value
    
    def get_real_value(self):
        return self.real_value

