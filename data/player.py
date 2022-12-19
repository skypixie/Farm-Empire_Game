import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load("data/character.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
