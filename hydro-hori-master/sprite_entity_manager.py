import pygame
import random
import constants2

class SpriteSheet:
    def __init__(self, sprite_sheet_image, num_columns, num_rows):
        """
        Initialize the sprite sheet.
        :param sprite_sheet_image: The Pygame surface containing the sprite sheet.
        :param num_columns: The number of columns of frames in the sprite sheet.
        :param num_rows: The number of rows of frames in the sprite sheet.
        """
        self.sprite_sheet = sprite_sheet_image
        self.num_columns = num_columns
        self.num_rows = num_rows
        self.sheet_width, self.sheet_height = self.sprite_sheet.get_size()
        self.frame_width = self.sheet_width // self.num_columns
        self.frame_height = self.sheet_height // self.num_rows

    def get_frame(self, column, row):
        """
        Get a specific frame from the sprite sheet.
        :param column: The column of the frame (starting from 0).
        :param row: The row of the frame (starting from 0).
        :return: The surface with the frame image.
        """
        frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
        frame.blit(self.sprite_sheet, (0, 0), 
                  (column * self.frame_width, row * self.frame_height, 
                   self.frame_width, self.frame_height))
        return frame

class EntitySprite(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_sheet, num_columns, num_rows, animation_speed):
        """
        Base class for all animated entities
        """
        super().__init__()
        self.sprite_sheet = sprite_sheet
        self.num_columns = num_columns
        self.num_rows = num_rows
        self.frame_index = 0
        self.animation_speed = animation_speed
        self.current_row = 0
        
        # Set initial frame
        self.image = self.sprite_sheet.get_frame(0, 0)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_y = random.uniform(2, 5)
        self.last_update = pygame.time.get_ticks()          ###
        self.animation_cooldown = 100  # Time between frame updates in milliseconds         ###

    def update_animation(self):
        """Update the current animation frame"""
        ##self.frame_index += self.animation_speed
        ##if self.frame_index >= self.num_columns:
        ##    self.frame_index = 0
        ##self.image = self.sprite_sheet.get_frame(int(self.frame_index), self.current_row)
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.frame_index = (self.frame_index + 1) % self.num_columns
            self.image = self.sprite_sheet.get_frame(int(self.frame_index), self.current_row)
            self.last_update = current_time

    def update(self):
        """Update entity position and animation"""
        self.update_animation()
        self.rect.y += self.speed_y
        if self.rect.y > constants2.SCREEN_HEIGHT:
            self.kill()

class PlayerSprite(EntitySprite):
    def __init__(self, x, y, sprite_sheet):
        super().__init__(x, y, sprite_sheet, num_columns=5, num_rows=1, animation_speed=0.2)
        self.speed = 0
        self.rect.y = y  # Fixed vertical position

    def update(self):
        """Update player position and animation"""
        # self.update_animation()
        if self.speed != 0:
            # Update frame index
            self.frame_index = (self.frame_index + self.animation_speed) % 5
            # Get new frame
            self.image = self.sprite_sheet.get_frame(int(self.frame_index), 0)
        
        self.rect.x += self.speed
        # Keep player within screen bounds
        self.rect.x = max(0, min(constants2.SCREEN_WIDTH - self.rect.width, self.rect.x))

    def set_speed(self, speed):
        """Set player horizontal speed"""
        self.speed = speed

class FuelCell(EntitySprite):
    def __init__(self, sprite_sheet):
        x = random.randint(constants2.GAME_LEFT_BOUNDARY, 
                          constants2.GAME_RIGHT_BOUNDARY - constants2.FUEL_CELL_SIZE)
        y = random.randint(-100, -40)
        super().__init__(x, y, sprite_sheet, num_columns=2, num_rows=1, animation_speed=0.2)

class Obstacle(EntitySprite):
    def __init__(self, sprite_sheet):
        x = random.randint(constants2.GAME_LEFT_BOUNDARY, 
                          constants2.GAME_RIGHT_BOUNDARY - constants2.OBSTACLE_SIZE)
        y = random.randint(-100, -40)
        super().__init__(x, y, sprite_sheet, num_columns=8, num_rows=1, animation_speed=0.1)  #.15
        

class Vehicle(EntitySprite):
    def __init__(self, sprite_sheet):
        x = random.randint(constants2.GAME_LEFT_BOUNDARY, 
                          constants2.GAME_RIGHT_BOUNDARY - constants2.VEHICLE_WIDTH)
        y = random.randint(-100, -40)
        super().__init__(x, y, sprite_sheet, num_columns=1, num_rows=1, animation_speed=0.1)

class FuelStationSprite(EntitySprite):
    def __init__(self, image, sprite_sheet=None, column=None, row=None):
        x = constants2.SCREEN_WIDTH - constants2.FUEL_STATION_WIDTH - 30
        y = random.randint(-100, -40)
        
        if sprite_sheet:
            super().__init__(x, y, sprite_sheet, num_columns=2, num_rows=1, animation_speed=0.1)
        else:
            # Fallback to non-animated version if no sprite sheet provided
            super().__init__(x, y, SpriteSheet(image, 1, 1), 
                           num_columns=1, num_rows=1, animation_speed=0)
            
        self.speed_y = 2  # Consistent speed for stations

class MaintenanceStation(EntitySprite):
    def __init__(self, sprite_sheet):
        x = 10
        y = random.randint(-100, -40)
        super().__init__(x, y, sprite_sheet, num_columns=1, num_rows=1, animation_speed=0.1)

class MiniMap(EntitySprite):
    def __init__(self, x, y, sprite_sheet):
        super().__init__(x, y, sprite_sheet, num_columns=2, num_rows=1, animation_speed=0.1)
        self.rect.topleft = (10, 10)  # Fixed position for minimap

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def update(self):
        """Update only animation, no movement"""
        self.update_animation()

# Spawning functions
def spawn_fuel_cell(sprite_sheet):
    return FuelCell(sprite_sheet)

def spawn_obstacle(sprite_sheet):
    return Obstacle(sprite_sheet)

def spawn_vehicle(sprite_sheet):
    return Vehicle(sprite_sheet)

def spawn_fuel_station(sprite_sheet):
    return FuelStationSprite(None, sprite_sheet)

def spawn_maintenance_station(sprite_sheet):
    return MaintenanceStation(sprite_sheet)
