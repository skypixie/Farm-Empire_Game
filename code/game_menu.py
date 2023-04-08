import pygame
from import_settings import graphics_ind, WIDTH, HEIGHT


class Menu:
    def __init__(self, exit_game):
        self.display_surface = pygame.display.get_surface()
        self.exit_game = exit_game
    
    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_new_game_image_rect.collidepoint(event.pos):
                    self.exit_game(True)
                elif self.exit_game_image_rect.collidepoint(event.pos):
                    self.exit_game(False)
    
    def display(self):
        self.start_new_game_image = pygame.image.load(f'../graphics/hud/start_new_game{graphics_ind}.png')
        self.start_new_game_image_rect = self.start_new_game_image.get_rect(center=(WIDTH // 4, HEIGHT // 2))

        self.exit_game_image = pygame.image.load(f'../graphics/hud/exit_game{graphics_ind}.png')
        self.exit_game_image_rect = self.exit_game_image.get_rect(center=(WIDTH - WIDTH // 4, HEIGHT // 2))

        self.display_surface.blit(self.start_new_game_image, self.start_new_game_image_rect)
        self.display_surface.blit(self.exit_game_image, self.exit_game_image_rect)
        self.input()
