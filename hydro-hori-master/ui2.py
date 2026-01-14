import pygame
from constants2 import *
from utils2 import *
from sound_manager import *
from options2_pause import pause_options

# Initialize Pygame modules
pygame.init()

# Set up the screen before loading assets
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load and scale background images
pause_menu_background = pygame.image.load('hydro-hori-master/assets/B1_End_1.png').convert()
pause_menu_background = pygame.transform.scale(pause_menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

game_over_background = pygame.image.load('hydro-hori-master/assets/B1_End.png').convert()
game_over_background = pygame.transform.scale(game_over_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

get_player_background = pygame.image.load('hydro-hori-master/assets/B1_End.png').convert()
get_player_background = pygame.transform.scale(get_player_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
# Load fonts
large_font = pygame.font.Font('hydro-hori-master/assets/font.ttf', 32)
developer_font = pygame.font.Font('hydro-hori-master/assets/font.ttf', 10)  
import pygame

def get_player_name(screen, converted_trucks, fuel_cells, sound_manager):
    """Get player name input after game over"""
    
    # Draw the background image
    screen.blit(get_player_background, (0, 0))

    # Draw overlay for better visibility of text
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)
    screen.blit(overlay, (0, 0))

    input_box = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = True
    text = ''
    done = False

    # State management
    state = 'input'  # States: 'input', 'confirm', 'confirmed', 'return_to_menu'
    selected_button = 0  # 0 = Yes, 1 = No for confirmation; 0 = Back for final screen

    # Buffer to space out elements vertically
    buffer_y_spacing = 40
    background_padding = 10  # Padding around text for background rectangles

    def draw_text_with_background(text, font, text_color, screen, x, y):
        """Draws text with a transparent grey background for better visibility"""
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(x, y))

        # Create a background rectangle slightly larger than the text surface
        background_rect = text_rect.inflate(background_padding * 2, background_padding * 2)
        background_surface = pygame.Surface((background_rect.width, background_rect.height))
        background_surface.fill((50, 50, 50))  # Grey color
        background_surface.set_alpha(180)  # Transparency level

        # Draw the background and then the text
        screen.blit(background_surface, background_rect)
        screen.blit(text_surface, text_rect)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if state == 'input':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and text.strip():
                        state = 'confirm'
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        # Limit name length to 15 characters
                        if len(text) < 15:
                            text += event.unicode

            elif state == 'confirm':
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        selected_button = 1 - selected_button  # Toggle between Yes/No
                    elif event.key == pygame.K_RETURN:
                        if selected_button == 0:  # Yes selected
                            state = 'confirmed'
                        else:  # No selected
                            state = 'return_to_menu'
                            selected_button = 0  # Reset selection for the next menu

            elif state == 'confirmed':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        done = True
                        return text

            elif state == 'return_to_menu':
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        selected_button = 1 - selected_button  # Toggle between Yes/No
                    elif event.key == pygame.K_RETURN:
                        if selected_button == 0:  # Yes selected
                            return None
                        else:  # No selected
                            state = 'input'  # Go back to name input
                            text = ''  # Clear previous input
                            selected_button = 0  # Reset selection

        # Redraw the background and overlay in each iteration
        screen.blit(get_player_background, (0, 0))
        screen.blit(overlay, (0, 0))

        # Show final score, centered with grey background
        draw_text_with_background(f"Trucks Converted: {converted_trucks}", developer_font, WHITE, screen,
                                  SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)

        draw_text_with_background(f"Fuel Cells: {fuel_cells}", developer_font, WHITE, screen,
                                  SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + buffer_y_spacing)

        if state == 'input':
            # Render input box and centered input prompt
            draw_text_with_background("Enter your name:", developer_font, WHITE, screen,
                                      SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - buffer_y_spacing)

            txt_surface = developer_font.render(text, True, color_active if active else color_inactive)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            input_box.centerx = SCREEN_WIDTH // 2  # Center the input box horizontally
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(screen, color_active if active else color_inactive, input_box, 2)

            # Show instruction
            draw_text_with_background("Press Enter to confirm", developer_font, WHITE, screen,
                                      SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + buffer_y_spacing)

        elif state == 'confirm':
            # Show confirmation message, centered with grey background
            draw_text_with_background(f"Save score as '{text}'?", developer_font, WHITE, screen,
                                      SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - buffer_y_spacing)

            # Draw Yes/No buttons, centered and spaced
            yes_color = color_active if selected_button == 0 else color_inactive
            no_color = color_active if selected_button == 1 else color_inactive

            draw_text_with_background("Yes", developer_font, yes_color, screen,
                                      SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + buffer_y_spacing)
            draw_text_with_background("No", developer_font, no_color, screen,
                                      SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2 + buffer_y_spacing)

        elif state == 'confirmed':
            # Show score saved message, centered with grey background
            draw_text_with_background("Score saved successfully!", developer_font, WHITE, screen,
                                      SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - buffer_y_spacing)

            # Draw back button, centered with grey background
            draw_text_with_background("Back to Main Menu", developer_font, color_active, screen,
                                      SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + buffer_y_spacing)

            # Show instruction, centered with grey background
            draw_text_with_background("Press Enter to continue", developer_font, WHITE, screen,
                                      SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + buffer_y_spacing * 2)

        elif state == 'return_to_menu':
            # Draw "Return to Main Menu?" message, centered with grey background
            draw_text_with_background("Return to Main Menu?", developer_font, WHITE, screen,
                                      SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - buffer_y_spacing)

            # Draw Yes/No buttons, centered and spaced with grey background
            yes_color = color_active if selected_button == 0 else color_inactive
            no_color = color_active if selected_button == 1 else color_inactive

            draw_text_with_background("Yes", developer_font, yes_color, screen,
                                      SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + buffer_y_spacing)
            draw_text_with_background("No", developer_font, no_color, screen,
                                      SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2 + buffer_y_spacing)

            # Show instructions, centered with grey background
            draw_text_with_background("Use left/right arrows to select", developer_font, WHITE, screen,
                                      SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + buffer_y_spacing * 2)

        # Update the display
        pygame.display.flip()

    return text


def draw_pause_menu(screen, sound_manager):
    # Draw the background image
    screen.blit(pause_menu_background, (0, 0))

    # Draw overlay for better visibility of text
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)
    screen.blit(overlay, (0, 0))

    # Calculate center position for title and adjust spacing
    title_y = SCREEN_HEIGHT // 4  # Move title even higher
    button_start_y = title_y + 120  # Start buttons further below title
    button_y_spacing = 100  # Increase spacing between buttons significantly

    # Draw the pause menu text centered
    title_text = "Game Paused"
    title_surface = large_font.render(title_text, True, WHITE)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, title_y))
    screen.blit(title_surface, title_rect)
    
    # Create and draw buttons for Pause menu with more spacing
    resume_button = Button(SCREEN_WIDTH // 2, button_start_y, "Resume", font_size=24)
    options_button = Button(SCREEN_WIDTH // 2, button_start_y + button_y_spacing, "Options", font_size=24)
    quit_button = Button(SCREEN_WIDTH // 2, button_start_y + button_y_spacing * 2, "Quit Game", font_size=24)
    
    buttons = [resume_button, options_button, quit_button]
    selected_index = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(buttons)
                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(buttons)
                elif event.key == pygame.K_RETURN:
                    if selected_index == 0:  # Resume button
                        return True
                    elif selected_index == 1:  # Options button
                        result = pause_options(screen, sound_manager)
                        if result == 'resume_game':
                            return True
                        elif result == 'quit':
                            return False 
                    elif selected_index == 2:  # Quit button
                        return False
                elif event.key == pygame.K_p:  # Allow P key to resume as well
                    return True
        
        # Draw buttons
        for i, button in enumerate(buttons):
            button.draw(screen, i == selected_index)
        
        pygame.display.flip()

def draw_game_over_menu(screen):
    # Draw the background image
    screen.blit(game_over_background, (0, 0))

    # Draw overlay for better visibility of text
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)
    screen.blit(overlay, (0, 0))

    # Draw the game over text
    draw_text("Restart Game?", large_font, WHITE, screen, 
              SCREEN_WIDTH // 2 - large_font.size("Restart Game?")[0] // 2, 
              SCREEN_HEIGHT // 2 - 100)
    
    # Create and draw buttons for Game Over screen
    button_y_spacing = 60
    restart_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, "Play Again", font_size=24)
    quit_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + button_y_spacing, "Quit Game", font_size=24)
    
    buttons = [restart_button, quit_button]
    selected_index = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(buttons)
                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(buttons)
                elif event.key == pygame.K_RETURN:
                    if selected_index == 0:  # Play Again button
                        return True
                    elif selected_index == 1:  # Quit button
                        return False
        
        # Draw buttons
        for i, button in enumerate(buttons):
            button.draw(screen, i == selected_index)
        
        pygame.display.flip()