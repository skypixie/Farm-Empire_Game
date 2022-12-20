import pygame
import sys

from level import Level
from settings import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((pygame.display.Info().current_w,
                                              pygame.display.Info().current_h - 60))
        pygame.display.set_caption("Farm Empire")
        self.clock = pygame.time.Clock()

        self.level = Level()
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill('black')
            self.level.run()
            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
