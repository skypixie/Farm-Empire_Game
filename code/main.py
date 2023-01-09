import pygame

from level import Level
from settings import *
from support import get_screen_size


class Game:
    def __init__(self):
        pygame.init()

        self.WIDTH, self.HEIGHT = get_screen_size()

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
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
            self.screen.fill((0, 0, 0))
            self.level.run()
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
