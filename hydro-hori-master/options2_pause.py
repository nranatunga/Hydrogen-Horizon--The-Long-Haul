import pygame
from constants2 import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from utils2 import Button, draw_text

def pause_options(screen, sound_manager):
    """Display options screen during pause, without the main menu return option"""
    font = pygame.font.Font('assets/font.ttf', 24)
    small_font = pygame.font.Font('assets/font.ttf', 20)
    
    # Create buttons
    button_y_start = SCREEN_HEIGHT // 3
    button_spacing = 80
    music_button = Button(SCREEN_WIDTH // 2, button_y_start, 
                         "Music: ON" if sound_manager.music_volume > 0 else "Music: OFF")
    sound_button = Button(SCREEN_WIDTH // 2, button_y_start + button_spacing, 
                         "Sound Effects: ON" if sound_manager.sfx_volume > 0 else "Sound Effects: OFF")
    resume_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, "Resume Game")  # Changed text to just "Back"
    
    buttons = [music_button, sound_button, resume_button]
    selected_index = 0
    
    running = True
    while running:
        screen.fill(BLACK)
        # Draw background
        background = pygame.image.load('assets/highway_1.png').convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(background, (0, 0))

        # Add overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))
        
        # Draw title
        title_text = "Options"
        title_surface = font.render(title_text, True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_surface, title_rect)
        
        # Update button text based on current state
        buttons[0].text = "Music: ON" if sound_manager.music_volume > 0 else "Music: OFF"
        buttons[1].text = "Sound Effects: ON" if sound_manager.sfx_volume > 0 else "Sound Effects: OFF"
        
        # Draw buttons
        for i, button in enumerate(buttons):
            button.draw(screen, i == selected_index)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'resume_game'
                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(buttons)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(buttons)
                elif event.key == pygame.K_RETURN:
                    if selected_index == 0:  # Music toggle
                        if sound_manager.music_volume > 0:
                            sound_manager.set_music_volume(0)
                            pygame.mixer.music.pause()
                        else:
                            sound_manager.set_music_volume(0.3)
                            pygame.mixer.music.unpause()
                    elif selected_index == 1:  # Sound effects toggle
                        if sound_manager.sfx_volume > 0:
                            sound_manager.set_sfx_volume(0)
                        else:
                            sound_manager.set_sfx_volume(0.5)
                    elif selected_index == 2:  # Resume button
                        return 'resume_game'  # Resume game
        
        pygame.display.flip()
    
    return 'resume_game'  # Default to resuming game if loop exits