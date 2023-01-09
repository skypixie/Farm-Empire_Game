import pygame

from settings import *

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.health_rect = pygame.Rect(HP_POS[0], HP_POS[1], HP_WIDTH, HP_HEIGHT)
        self.mana_rect = pygame.Rect(MP_POS[0], MP_POS[1], MP_WIDTH, MP_HEIGHT)

        self.weapon_paths = [weapon_dict['graphic'] for weapon_dict in weapon_data.values()]
        self.magic_paths = [magic_dict['graphic'] for magic_dict in magic_data.values()]

    def show_bar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, STATS_BG_COLOR, bg_rect)

        # перевод количества в пиксели\
        current_width = current / max_amount * bg_rect.width

        current_bar = pygame.Rect(bg_rect.left, bg_rect.top,
                                  current_width, bg_rect.height)

        pygame.draw.rect(self.display_surface, color, current_bar)
        pygame.draw.rect(self.display_surface, STATS_BG_COLOR, current_bar, 3)

    def show_item(self, item_path, x, y, width, height):
        # подложка для оружия
        bg_rect = pygame.Rect(x, y, width, height)
        bg_border = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.display_surface, ITEM_BOX_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, ITEM_BOX_BORDER_COLOR, bg_border, 3)

        # оружие
        weapon_img = pygame.image.load(item_path).convert_alpha()
        weapon_rect = weapon_img.get_rect(center=bg_rect.center)

        self.display_surface.blit(weapon_img, weapon_rect)

    def display(self, player):
        self.show_bar(player.current_health, player.stats['health'],
                      self.health_rect, HP_COLOR)
        self.show_bar(player.current_mana, player.stats['mana'],
                      self.mana_rect, MP_COLOR)

        self.show_item(self.weapon_paths[player.weapon_index], *WEAPON_BOX_POS, *WEAPON_BOX_SIZE)
        self.show_item(self.magic_paths[player.magic_index], *MAGIC_BOX_POS, *MAGIC_BOX_SIZE)
