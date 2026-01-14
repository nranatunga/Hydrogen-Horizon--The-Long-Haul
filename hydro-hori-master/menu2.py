import pygame
from constants2 import *
from utils2 import Button  # Assuming you have a Button class in utils.py
from instructions2 import show_instructions
from leaderboards2 import show_leaderboards
from sound_manager import SoundManager
from options2 import show_options

def draw_text_block(screen, text, font, color, x, y, line_spacing=10):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if line.strip():  # Only render non-empty lines
            text_surface = font.render(line.strip(), True, color)
            text_rect = text_surface.get_rect(x=x, y=y + (i * (font.get_height() + line_spacing)))
            screen.blit(text_surface, text_rect)

def show_main_menu(screen, sound_manager):

    # Load and scale background image
    background = pygame.image.load('assets/B1_Title.png').convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Create fonts
    title_font = pygame.font.Font('assets/font.ttf', 38)
    subtitle_font = pygame.font.Font('assets/font.ttf', 14)
    developer_font = pygame.font.Font('assets/font.ttf', 10)
    
    # Create buttons
    button_y_spacing = 80  # Increased space between buttons to avoid overlap
    start_y = SCREEN_HEIGHT // 2 - 150
    buttons = [
        Button(SCREEN_WIDTH // 2, start_y, "Start Game", font_size=24),
        Button(SCREEN_WIDTH // 2, start_y + button_y_spacing, "Instructions", font_size=24),
        Button(SCREEN_WIDTH // 2, start_y + button_y_spacing * 2, "Leaderboards", font_size=24),
        Button(SCREEN_WIDTH // 2, start_y + button_y_spacing * 3, "Exit Game", font_size=24),
        Button(SCREEN_WIDTH - 90, SCREEN_HEIGHT - 50, "Options", font_size=10)  # Options button at bottom right
    ]
    
    # Menu state
    selected_index = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(buttons)
                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(buttons)
                elif event.key == pygame.K_RETURN:
                    if buttons[selected_index].text == "Start Game":
                        return True
                    elif buttons[selected_index].text == "Instructions":
                        # Show instructions screen
                        result = show_instructions(screen)
                        if result == 'main_menu':
                            continue  # Go back to main menu
                    elif buttons[selected_index].text == "Leaderboards":
                        # Show leaderboards screen
                        result = show_leaderboards(screen)
                        if result == 'main_menu':
                            continue  # Go back to main menu
                    elif buttons[selected_index].text == "Exit Game":
                        pygame.quit()
                        exit()
                    elif buttons[selected_index].text == "Options":
                        result = show_options(screen, sound_manager)
                        if result == 'main_menu':
                            continue
        
        # Draw background
        screen.blit(background, (0, 0))
        
        # Draw overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))
        
        # Draw title
        title_text = title_font.render("The Long Haul:", True, WHITE)
        subtitle_text = subtitle_font.render("Hydrogen Horizons", True, WHITE)
        
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 8))
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, title_rect.bottom + 30))
        
        screen.blit(title_text, title_rect)
        screen.blit(subtitle_text, subtitle_rect)
        
        # Draw buttons
        for i, button in enumerate(buttons):
            button.draw(screen, i == selected_index)
        
        # Draw developer names
        developer_text = developer_font.render("Developed by: C. Moraleja, N. Ranatunga, R. Rabusa", True, WHITE)
        developer_rect = developer_text.get_rect(topleft=(20, SCREEN_HEIGHT - 30))
        screen.blit(developer_text, developer_rect)
        
        pygame.display.flip()
    
    return False

