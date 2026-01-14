import pygame
import random
import constants2
from sprite_entity_manager import *

# Define common colors
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0, 128)
SKY_BLUE = (135, 206, 235, 128)
DARK_SKY_BLUE = (70, 130, 180, 128)

class Button:
    def __init__(self, x, y, text, font_size=24, padding_x=30, padding_y=15, normal_color=SKY_BLUE, hover_color=DARK_SKY_BLUE, shape='rectangle'):
        self.text = text
        self.font = pygame.font.Font('hydro-hori-master/assets/font.ttf', font_size)
        
        # Calculate button size based on text
        text_surface = self.font.render(text, True, WHITE)
        self.width = text_surface.get_width() + (padding_x * 2)
        self.height = text_surface.get_height() + (padding_y * 2)
        
        # Center the button at the given x, y coordinates
        self.rect = pygame.Rect(x - self.width // 2, y - self.height // 2, self.width, self.height)
        
        # Button colors and shape
        self.normal_color = normal_color  # Customizable normal color
        self.hover_color = hover_color    # Customizable hover color
        self.text_color = WHITE           # White color
        self.shape = shape                # Button shape: 'rectangle' or 'ellipse'
        
    def draw(self, screen, is_selected=False):
        # Draw button background based on shape
        color = self.hover_color if is_selected else self.normal_color
        button_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        
        if self.shape == 'rectangle':
            pygame.draw.rect(button_surface, color, button_surface.get_rect(), border_radius=10)
        elif self.shape == 'ellipse':
            pygame.draw.ellipse(button_surface, color, button_surface.get_rect())
        
        screen.blit(button_surface, self.rect.topleft)
        
        # Draw border if selected
        if is_selected:
            if self.shape == 'rectangle':
                pygame.draw.rect(screen, self.text_color, self.rect, 2, border_radius=10)
            elif self.shape == 'ellipse':
                pygame.draw.ellipse(screen, self.text_color, self.rect, 2)
        
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event, is_selected=False):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                return self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and is_selected:
            if event.key == pygame.K_RETURN:  # Enter key
                return True
        return False
    


def draw_hud(screen, font, converted_trucks, fuel_cells_collected, truck_fuel, truck_health, timer, minimap):
    """
    Draws the HUD (Heads-Up Display) on the game screen.
    
    Parameters:
        screen (pygame.Surface): The surface on which the HUD is drawn.
        font (pygame.font.Font): The font used to render text in the HUD.
        converted_trucks (int): Number of trucks converted.
        fuel_cells_collected (int): Number of fuel cells collected.
        truck_fuel (int): The current fuel level of the player's truck.
        truck_health (int): The current health of the player's truck.
        timer (int): Remaining time in milliseconds.
        minimap (MiniMap): The minimap sprite instance to be drawn.
    """
    hud_height = 145  # Height of the HUD
    hud_background = pygame.Surface((constants2.SCREEN_WIDTH, hud_height))
    hud_background.fill((50, 50, 50))  # Gray background
    screen.blit(hud_background, (0, constants2.SCREEN_HEIGHT - hud_height))

    # Draw the light gray boundary around the HUD
    hud_boundary_color = (211, 211, 211)  # Light gray
    pygame.draw.rect(screen, hud_boundary_color, (0, constants2.SCREEN_HEIGHT - hud_height, constants2.SCREEN_WIDTH, hud_height), 2)  # Thickness of 2

    # Position the time stat at the top left
    time_text = f"Time: {timer // 60000:02}:{(timer % 60000) // 1000:02}"  # Format the timer
    draw_text(time_text, font, constants2.WHITE, screen, 10, constants2.SCREEN_HEIGHT - hud_height + 10)  # Top left position with padding

    # Create a list of stats
    stats = [
        f"Converted Trucks: {converted_trucks}",
        f"Fuel Cells: {fuel_cells_collected}",
        f"Health: {truck_health}",
        f"Fuel Level: {truck_fuel}"
    ]

    # Calculate spacing for the remaining stats
    spacing = (constants2.SCREEN_WIDTH - 20) // 2  # Space for each stat column

    # Starting y-position for the stats
    start_y = constants2.SCREEN_HEIGHT - hud_height + 30  # Padding from the top of the HUD for stats

    # Draw the first row (Converted Trucks and Fuel Cells)
    for i in range(2):
        screen_x = 10 + (i % 2) * spacing  # X position based on column
        screen_y = start_y  # Y position for the first row
        draw_text(stats[i], font, constants2.WHITE, screen, screen_x, screen_y)

    # Draw the second row (Health and Fuel Level) closer together
    for i in range(2, 4):
        screen_x = 10 + ((i - 2) % 2) * spacing  # X position based on column
        screen_y = start_y + 20  # Y position for the second row, adjusting for closeness
        draw_text(stats[i], font, constants2.WHITE, screen, screen_x, screen_y)

    # Draw the minimap on the left of the HUD
    minimap.rect.topleft = (635, constants2.SCREEN_HEIGHT - hud_height -47)  # Adjust minimap position
    minimap.draw(screen)


        
def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(topleft=(x, y))
    surface.blit(textobj, textrect)


def spawn_object(spawn_function, obj_list, *args):
    if random.randint(1, spawn_function[0]) == 1:
        obj_list.append(spawn_function[1](*args))


def draw_objects(screen, obj_list, image):
    for obj in obj_list:
        screen.blit(image, obj[:2])
