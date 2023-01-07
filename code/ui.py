import pygame

from settings import *

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.health_rect = pygame.Rect(HP_POS[0], HP_POS[1], HP_WIDTH, HP_HEIGHT)
        self.mana_rect = pygame.Rect(MP_POS[0], MP_POS[1], MP_WIDTH, MP_HEIGHT)

    def show_bar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, STATS_BG_COLOR, bg_rect)

        # перевод количества в пиксели\
        current_width = current / max_amount * bg_rect.width

        current_bar = pygame.Rect(bg_rect.left, bg_rect.top,
                                  current_width, bg_rect.height)

        pygame.draw.rect(self.display_surface, color, current_bar)
        pygame.draw.rect(self.display_surface, STATS_BG_COLOR, current_bar, 3)

    def display(self, player):
        self.show_bar(player.current_health, player.stats['health'],
                      self.health_rect, HP_COLOR)
        self.show_bar(player.current_mana, player.stats['mana'],
                      self.mana_rect, MP_COLOR)
