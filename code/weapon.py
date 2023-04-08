import pygame
from import_settings import TILESIZE, graphics_ind


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        direction = player.status.split('_')[0]

        full_path = f'../graphics/weapons{graphics_ind}/{player.weapon}/{direction}.png'

        self.image = pygame.image.load(full_path).convert_alpha()

        y_offset = pygame.math.Vector2(0, TILESIZE // 4)
        x_offset = pygame.math.Vector2(-TILESIZE // 4, 0)
        if direction == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright + y_offset)
        elif direction == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft + y_offset)
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + x_offset)
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + x_offset)
