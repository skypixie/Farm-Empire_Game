import pygame

from level import Level
from settings import *


class Game:
    def __init__(self):
        pygame.init()

        self.WIDTH, self.HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h - 60

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

        self.level = Level()

        pygame.display.set_caption("Farm Empire")

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.fill((0, 0, 0))
            self.level.run()
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
