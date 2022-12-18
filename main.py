import pygame

from settings import *
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        w = pygame.display.Info().current_w
        SIZE = WIDTH, HEIGHT = RESOLUION[0 if w < 1920 else (1 if w <= 3840 else 2)]
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()

        self.level = Level()
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.fill("black")
            self.level.run()
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()