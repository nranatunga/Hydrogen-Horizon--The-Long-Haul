import pygame
import constants2
from utils2 import draw_text, draw_hud 
from sprite_entity_manager import (PlayerSprite, FuelCell, Obstacle, Vehicle, 
                                 FuelStationSprite, MaintenanceStation, SpriteSheet, MiniMap)
from game_logic3 import update_game_objects, handle_collisions, handle_stations
from menu2 import show_main_menu
from ui2 import *
from leaderboards2 import Leaderboard
from sound_manager import SoundManager
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Initialize sound manager
sound_manager = SoundManager()
# Start playing menu music
sound_manager.play_music('main_menu')

# Initialize screen
screen = pygame.display.set_mode((constants2.SCREEN_WIDTH, constants2.SCREEN_HEIGHT))
pygame.display.set_caption("The Long Haul: Hydrogen Horizons")
leaderboard = Leaderboard()

# Show main menu
if not show_main_menu(screen, sound_manager):
    pygame.quit()
    exit()


# Create scrolling background class
class ScrollingBackground:
    def __init__(self, image, speed):
        self.image = image
        self.rect1 = self.image.get_rect()
        self.rect2 = self.image.get_rect()
        self.rect2.y = -self.rect1.height
        self.speed = speed

    def update(self):
        self.rect1.y += self.speed
        self.rect2.y += self.speed

        if self.rect1.y >= constants2.SCREEN_HEIGHT:
            self.rect1.y = self.rect2.y - self.rect1.height
        if self.rect2.y >= constants2.SCREEN_HEIGHT:
            self.rect2.y = self.rect1.y - self.rect2.height

    def draw(self, screen):
        screen.blit(self.image, self.rect1)
        screen.blit(self.image, self.rect2)


# Load background and create scrolling instance
background_main = pygame.image.load('hydro-hori-master/assets/highway_main.png').convert()
background_main = pygame.transform.scale(background_main, (constants2.SCREEN_WIDTH, constants2.SCREEN_HEIGHT))
scrolling_background = ScrollingBackground(background_main, speed=2)

# Load and initialize sprite sheets with correct animation frames
sprite_sheets = {
    'player': SpriteSheet(pygame.image.load("hydro-hori-master/assets/pickup_b_n_ss.png").convert_alpha(), 5, 1),
    'fuel_cell': SpriteSheet(pygame.image.load("hydro-hori-master/assets/fuel_cell_H_ss.png").convert_alpha(), 2, 1),
    'obstacle': SpriteSheet(pygame.image.load("hydro-hori-master/assets/obs_deer_2_ss.png").convert_alpha(), 8, 1),
    'vehicle': SpriteSheet(pygame.image.load("hydro-hori-master/assets/truck_b_s.png").convert_alpha(), 1, 1),
    'fuel_station': SpriteSheet(pygame.image.load("hydro-hori-master/assets/fuel_station_H_ss.png").convert_alpha(), 2, 1),
    'maintenance': SpriteSheet(pygame.image.load("hydro-hori-master/assets/maintenance.png").convert_alpha(), 1, 1),
    'minimap': SpriteSheet(pygame.image.load("hydro-hori-master/assets/Hyw_2_ss.png").convert_alpha(), 2, 1)
}

# Initialize sprite groups
def init_sprite_groups():
    """Initialize and return all sprite groups"""
    return {
        'player': pygame.sprite.GroupSingle(),
        'fuel_cells': pygame.sprite.Group(),
        'obstacles': pygame.sprite.Group(),
        'vehicles': pygame.sprite.Group(),
        'fuel_stations': pygame.sprite.Group(),
        'maintenance': pygame.sprite.Group()
    }

def spawn_entities(sprite_groups, sprite_sheets):
    """Handle entity spawning with proper probabilities"""
    if random.randint(1, 50) == 1:  # 5% chance each frame
        sprite_groups['fuel_cells'].add(FuelCell(sprite_sheets['fuel_cell']))
        
    if random.randint(1, 50) == 1:
        sprite_groups['vehicles'].add(Vehicle(sprite_sheets['vehicle']))
        
    if random.randint(1, 50) == 1:  # 2% chance each frame #50
        sprite_groups['obstacles'].add(Obstacle(sprite_sheets['obstacle']))
        
    if random.randint(1, 500) == 1:  # 0.2% chance each frame
        sprite_groups['fuel_stations'].add(FuelStationSprite(None, sprite_sheets['fuel_station']))
        
    if random.randint(1, 800) == 1:  # 0.125% chance each frame
        sprite_groups['maintenance'].add(MaintenanceStation(sprite_sheets['maintenance']))


# Load fonts
custom_font_path = 'hydro-hori-master/assets/font.ttf'
font = pygame.font.Font(custom_font_path, 9)
large_font = pygame.font.Font(custom_font_path, 32)

def init_game_state():
    """Initialize and return game state dictionary"""
    return {
        'converted_trucks': 0,
        'fuel_cells_collected': 0,
        'truck_health': 100,
        'truck_fuel': 100,
        'in_fuel_station': False,
        'in_maintenance_station': False,
        'fuel_station_timer': 0,
        'maintenance_station_timer': 0
    }

# Initialize game components
sprite_groups = init_sprite_groups()
player_sprite = PlayerSprite(
    constants2.SCREEN_WIDTH // 2,
    constants2.SCREEN_HEIGHT - constants2.TRUCK_HEIGHT - 120,
    sprite_sheets['player']
)
sprite_groups['player'].add(player_sprite)

# Initialize minimap
minimap = MiniMap(10, 10, sprite_sheets['minimap'])

# Game state initialization
game_state = init_game_state()

# Game control variables
clock = pygame.time.Clock()
running = True
game_over = False
paused = False
timer = 5 * 60 * 1000  # 5 minutes in milliseconds

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_over = True
            elif event.key == pygame.K_p:
                paused = not paused
            elif event.key == pygame.K_q and (game_over or paused):
                running = False

    if not game_over and not paused:
        # Handle player movement
        keys = pygame.key.get_pressed()
        speed = 0
        if keys[pygame.K_LEFT]:
            speed = -7
        elif keys[pygame.K_RIGHT]:
            speed = 7
        player_sprite.set_speed(speed)
        
        # Update and draw scrolling background
        scrolling_background.update()
        scrolling_background.draw(screen)

        # Spawn new entities
        spawn_entities(sprite_groups, sprite_sheets)
        
        # Update game objects and handle collisions
        update_game_objects(sprite_groups)
        game_over = handle_collisions(player_sprite, sprite_groups, game_state, screen, font, sound_manager)
        handle_stations(player_sprite, sprite_groups, game_state, sound_manager)

        # Draw everything
        for group in sprite_groups.values():
            group.draw(screen)
            
        # Update and draw minimap
        minimap.update()
        screen.blit(minimap.image, minimap.rect)
      

            
        # Draw HUD
        draw_hud(screen, font, game_state['converted_trucks'], 
                game_state['fuel_cells_collected'], game_state['truck_fuel'], 
                game_state['truck_health'], timer,minimap)

        # Update timer
        timer -= clock.get_time()
        if timer <= 0:
            game_over = True

    elif paused:
        pause_result = draw_pause_menu(screen, sound_manager)
        if pause_result is True:
            paused = False
        elif pause_result is False:
            running = False

    elif game_over:
        player_name = get_player_name(screen,game_state['converted_trucks'], 
                                    game_state['fuel_cells_collected'], sound_manager)
        if player_name is not None:
            leaderboard.add_score(player_name, game_state['converted_trucks'], 
                                game_state['fuel_cells_collected'])
        # Reset game
        game_over = False
        game_state = init_game_state()
        timer = 1 * 60 * 1000
        sprite_groups = init_sprite_groups()
        player_sprite = PlayerSprite(
                constants2.SCREEN_WIDTH // 2,
                constants2.SCREEN_HEIGHT - constants2.TRUCK_HEIGHT - 120,
                sprite_sheets['player']

            )
        sprite_groups['player'].add(player_sprite)
        if not show_main_menu(screen, sound_manager):
            running = False

    pygame.display.flip()
    clock.tick(25)

pygame.quit()