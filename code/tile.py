import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)

        tilesize = pygame.display.get_surface().get_height() // 15
        self.hitbox = self.rect.inflate(0, -tilesize // 4)
