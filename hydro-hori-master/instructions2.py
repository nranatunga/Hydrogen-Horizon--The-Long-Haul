import pygame
from constants2 import *
from utils2 import Button  # Assuming you have a Button class in utils.py

def draw_text_block(screen, text, font, color, x, y, line_spacing=10):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if line.strip():  # Only render non-empty lines
            text_surface = font.render(line.strip(), True, color)
            text_rect = text_surface.get_rect(x=x, y=y + (i * (font.get_height() + line_spacing)))
            screen.blit(text_surface, text_rect)

def show_instructions(screen):
    # Load and scale background
    background = pygame.image.load('hydro-hori-master/assets/highway_1.png').convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Create fonts
    title_font = pygame.font.Font('hydro-hori-master/assets/font.ttf', 36)
    instruction_font = pygame.font.Font('hydro-hori-master/assets/font.ttf', 15)
    
    # Create back button using Button class from utils, positioned at bottom right corner
    back_button = Button(SCREEN_WIDTH - 140, SCREEN_HEIGHT - 60, text="Back", font_size=24, padding_x=20, padding_y=10)
    
    # Instruction text - condensed version
    instructions = """
 Controls:
• LEFT/RIGHT - Move truck
• P - Pause Game
• Enter  - Select button

Gameplay:
• Collect Fuel Cells for energy
• Convert vehicles to hydrogen
• Avoid obstacles
• Use Fuel/Maintenance Stations

Scoring:
• Convert vehicle: +2 points
• Fuel cell: +2 energy
• Hit obstacle: -1 health
• Converting uses 1 fuel

Win/Lose:
• Goal: Convert max vehicles
• Game ends if:
  - Health = 0
  - No fuel/cells
  - Time expires"""
    
    running = True
    back_button_selected = True 
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if back_button.handle_event(event, back_button_selected):
                return True
        
        # Draw background with overlay
        screen.blit(background, (0, 0))
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)  # More opaque for better text readability
        screen.blit(overlay, (0, 0))
        
        # Draw title
        title_text = title_font.render("Game Instructions", True, WHITE)
        title_rect = title_text.get_rect(centerx=SCREEN_WIDTH // 2, y=30)
        screen.blit(title_text, title_rect)
        
        # Draw instructions
        draw_text_block(screen, instructions, instruction_font, WHITE, 50, 100)
        
        # Draw back button
        back_button.draw(screen, is_selected=False)
        
        pygame.display.flip()
    
    return False
