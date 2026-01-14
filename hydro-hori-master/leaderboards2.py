import pygame
import json
from os import path
from utils2 import Button, draw_text
from constants2 import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from sound_manager import SoundManager

class Leaderboard:
    def __init__(self):
        self.scores = []
        self.filename = 'leaderboard.json'
        self.load_scores()
        
    def load_scores(self):
        try:
            if path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    self.scores = json.load(f)
                    # Sort scores by converted trucks (primary) and fuel cells (secondary)
                    self.scores.sort(key=lambda x: (x['converted_trucks'], x['fuel_cells']), reverse=True)
                    # Keep only top 10 scores
                    self.scores = self.scores[:10]
        except:
            self.scores = []
    
    def save_scores(self):
        with open(self.filename, 'w') as f:
            json.dump(self.scores, f)
    
    def add_score(self, name, converted_trucks, fuel_cells):
        score = {
            'name': name,
            'converted_trucks': converted_trucks,
            'fuel_cells': fuel_cells
        }
        self.scores.append(score)
        # Sort and trim scores
        self.scores.sort(key=lambda x: (x['converted_trucks'], x['fuel_cells']), reverse=True)
        self.scores = self.scores[:10]
        self.save_scores()


def draw_centered_text(text, font, color, screen, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


def show_leaderboards(screen):
    """Display leaderboards screen"""
    leaderboard = Leaderboard()
    font = pygame.font.Font('hydro-hori-master/assets/font.ttf', 24)
    small_font = pygame.font.Font('hydro-hori-master/assets/font.ttf', 20)

    back_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, "Back to Main Menu")
    # Track if back button is selected
    back_button_selected = True
    
    # Define column positions
    rank_x = SCREEN_WIDTH // 5
    name_x = SCREEN_WIDTH * 2 // 5
    trucks_x = SCREEN_WIDTH * 3 // 5
    cells_x = SCREEN_WIDTH * 4 // 5

    running = True
    while running:
        screen.fill(BLACK)
        background = pygame.image.load('hydro-hori-master/assets/highway_1.png').convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(background, (0, 0))

        # Add a semi-transparent overlay to make text more readable
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)  # Adjust transparency (0-255)
        screen.blit(overlay, (0, 0))
        
        # Draw centered title
        draw_centered_text("Leaderboards", font, WHITE, screen, SCREEN_WIDTH // 2, 50)

        
        # Draw centered column headers
        draw_centered_text("Rank", small_font, WHITE, screen, rank_x, 100)
        draw_centered_text("Name", small_font, WHITE, screen, name_x, 100)
        draw_centered_text("Trucks", small_font, WHITE, screen, trucks_x, 100)
        draw_centered_text("Cells", small_font, WHITE, screen, cells_x, 100)
        
        # Draw scores with center alignment
        for i, score in enumerate(leaderboard.scores):
            y = 150 + (i * 30)
            draw_centered_text(f"#{i+1}", small_font, WHITE, screen, rank_x, y)
            draw_centered_text(score['name'], small_font, WHITE, screen, name_x, y)
            draw_centered_text(str(score['converted_trucks']), small_font, WHITE, screen, trucks_x, y)
            draw_centered_text(str(score['fuel_cells']), small_font, WHITE, screen, cells_x, y)
        
        # Draw back button with selection highlight
        back_button.draw(screen, back_button_selected)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'main_menu'
                elif event.key == pygame.K_RETURN and back_button_selected:
                    return 'main_menu'
                # up and down keys will select the back button
                elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                    back_button_selected = True
        
        pygame.display.flip()
    
    return 'main_menu'