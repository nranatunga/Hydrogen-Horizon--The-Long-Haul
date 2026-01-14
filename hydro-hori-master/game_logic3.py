import pygame
from constants2 import *
from utils2 import draw_text
from sound_manager import SoundManager

def update_game_objects(sprite_groups):
    """Update all sprite groups"""
    for group in sprite_groups.values():
        group.update()

def handle_collisions(player_sprite, sprite_groups, game_state, screen, font, sound_manager):
    """Handle collisions between player and other sprites"""
    game_over = False
    
    # Fuel Cell collisions
    fuel_cell_hits = pygame.sprite.spritecollide(player_sprite, sprite_groups['fuel_cells'], True)
    for _ in fuel_cell_hits:
        sound_manager.play_sound('fuel_collect')
        game_state['fuel_cells_collected'] += 2
    
    # Obstacle collisions
    obstacle_hits = pygame.sprite.spritecollide(player_sprite, sprite_groups['obstacles'], False)
    for obstacle in obstacle_hits:
        
        game_state['truck_health'] -= 1
        game_state['truck_health'] = max(0, game_state['truck_health'])
        obstacle.kill()
        
        if game_state['truck_health'] <= 0:
            game_over = True
            display_game_over(screen, font, "The truck's health has hit zero!", 
                            game_state['converted_trucks'], game_state['fuel_cells_collected'])
    
    # Vehicle collisions
    vehicle_hits = pygame.sprite.spritecollide(player_sprite, sprite_groups['vehicles'], True)
    for _ in vehicle_hits:
        sound_manager.play_sound('truck_collision')
        fuel_cost = 1
        
        if game_state['truck_fuel'] >= fuel_cost:
            game_state['truck_fuel'] -= fuel_cost
            game_state['converted_trucks'] += 2
        elif game_state['truck_fuel'] == 0 and game_state['fuel_cells_collected'] >= fuel_cost:
            game_state['fuel_cells_collected'] -= fuel_cost
            game_state['converted_trucks'] += 2
        else:
            game_over = True
            display_game_over(screen, font, "Out of fuel and fuel cells!", 
                            game_state['converted_trucks'], game_state['fuel_cells_collected'])
    
    return game_over

def handle_stations(player_sprite, sprite_groups, game_state, sound_manager):
    """Handle fuel and maintenance station interactions"""
    # Handle fuel station collisions
    if game_state['in_fuel_station']:
        if pygame.time.get_ticks() - game_state['fuel_station_timer'] > 50:
            game_state['in_fuel_station'] = False
            game_state['truck_fuel'] += 2
    else:
        fuel_station_collisions = pygame.sprite.spritecollide(player_sprite, 
                                                            sprite_groups['fuel_stations'], False)
        if fuel_station_collisions:
            sound_manager.play_sound('fuel_station')
            game_state['in_fuel_station'] = True
            game_state['fuel_station_timer'] = pygame.time.get_ticks()
            game_state['truck_fuel'] += 2

    # Handle maintenance station collisions
    if game_state['in_maintenance_station']:
        if pygame.time.get_ticks() - game_state['maintenance_station_timer'] > 50:
            game_state['in_maintenance_station'] = False
            game_state['truck_health'] = 100
    else:
        maintenance_collisions = pygame.sprite.spritecollide(player_sprite, 
                                                           sprite_groups['maintenance'], False)
        if maintenance_collisions:
            sound_manager.play_sound('health_station')
            game_state['in_maintenance_station'] = True
            game_state['maintenance_station_timer'] = pygame.time.get_ticks()
            game_state['truck_health'] = 100

def display_game_over(screen, font, message, converted_trucks, fuel_cells_collected):
    """Display game over screen with final scores"""
    screen.fill(WHITE)
    stats_y = SCREEN_HEIGHT // 2 - 30
    
    draw_text(message, font, RED, screen, 
             SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100)
    
    draw_text(f"Trucks Converted: {converted_trucks}", font, BLACK, screen,
             SCREEN_WIDTH // 2 - 100, stats_y + 30)
    draw_text(f"Fuel Cells Collected: {fuel_cells_collected}", font, BLACK, screen,
             SCREEN_WIDTH // 2 - 100, stats_y + 60)
    draw_text("Press Q to Quit", font, BLACK, screen,
             SCREEN_WIDTH // 2 - 100, stats_y + 100)
    
    pygame.display.flip()
    pygame.time.wait(10000)