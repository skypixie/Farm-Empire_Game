import pygame

from level import Level
from import_settings import FPS
from support import get_screen_size
import sys
import sqlite3


class Game:
    def __init__(self):
        pygame.init()

        self.WIDTH, self.HEIGHT = get_screen_size()

        self.define_graphics_index()

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

        self.start_sound = pygame.mixer.Sound('../audio/start_game.wav')
        self.start_sound.set_volume(0.3)

        self.game_over_sound = pygame.mixer.Sound('../audio/game_over.wav')
        self.game_over_sound.set_volume(0.3)

        pygame.display.set_caption("Farm Empire")

    def run(self, show_start_screen):
        if show_start_screen:
            if not self.show_start_screen():
                return
        
        self.level = Level(self.graphics_ind, self.show_game_over_screen)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.show_game_over_screen(False)
                if event.type == pygame.KEYDOWN and\
                        event.key == pygame.K_ESCAPE:
                    self.level.toggle_menu()
            
            if self.level.running:
                self.screen.fill((0, 0, 0))
                self.level.run()
                pygame.display.flip()
                self.clock.tick(FPS)
            else:
                self.show_game_over_screen(True)
        pygame.quit()
        sys.exit()
    
    def show_start_screen(self):
        self.screen.fill((0, 0, 0))
        start_image = pygame.image.load(f'../graphics/start_screen{self.graphics_ind}.png').convert_alpha()
        img_rect = start_image.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        self.screen.blit(start_image, img_rect)
        pygame.display.flip()
        self.start_sound.play()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.show_game_over_screen(False)
                    else:
                        return True
    
    def show_game_over_screen(self, restart_game):
        self.game_over_sound.play()
        
        if restart_game:
            self.clear_progress()

            self.show_start_screen()

            running = True
            start_ticks=pygame.time.get_ticks()
            while running:
                seconds=(pygame.time.get_ticks() - start_ticks) / 1000
                if seconds > 2:
                    self.run(False)
        else:
            self.screen.fill((0, 0, 0))
            img = pygame.image.load(f'../graphics/game_over{self.graphics_ind}_exit.png')
            rect = img.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
            self.screen.blit(img, rect)
            pygame.display.flip()

            start_ticks = pygame.time.get_ticks()
            while True:
                seconds = (pygame.time.get_ticks() - start_ticks) / 1000
                if seconds > 2:
                    break
            sys.exit()


    def define_graphics_index(self):
        if self.WIDTH <= 1920:
            self.graphics_ind = 1
        else:
            self.graphics_ind = 2
    
    def clear_progress(self):
        # очистить базу данны с прогрессом
        con = sqlite3.connect('database/progress_db.sqlite3')
        cur = con.cursor()
        cur.execute("delete from fields")
        cur.execute("delete from sqlite_sequence where name='fields'")
        for i in range(4):
            cur.execute("INSERT INTO fields(passed) VALUES(0)")
        con.commit()


if __name__ == '__main__':
    game = Game()
    game.run(True)
