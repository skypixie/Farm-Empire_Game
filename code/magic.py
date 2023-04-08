import pygame
from import_settings import *
from random import randint


class Magic:
    def __init__(self, animation_player):
        self.animation_player = animation_player
        self.sounds = {
            'heal': pygame.mixer.Sound('../audio/heal.wav'),
            'flame': pygame.mixer.Sound('../audio/flame.wav'),
            'spark': pygame.mixer.Sound('../audio/spark.wav')
        }
        for key in self.sounds:
            self.sounds[key].set_volume(0.3)
    
    def heal(self, player, strength, cost, groups):
        # игрок может увеличивать здоровье до 1000 единиц - не баг, а фича!
        if player.current_mana >= cost and player.current_health <= 1000:
            player.current_health += strength
            player.current_mana -= cost

            self.sounds['heal'].play()
            self.animation_player.create_particles('heal', player.rect.center + pygame.math.Vector2(0, -TILESIZE),
                                                   groups)
            self.animation_player.create_particles('aura', player.rect.center, groups)

    def long_spell(self, player, cost, magic_name, groups):
        if player.current_mana >= cost:
            player.current_mana -= cost
            status = player.status.split('_')[0]

            if status == 'right':
                direction = pygame.math.Vector2(1, 0)
            elif status == 'left':
                direction = pygame.math.Vector2(-1, 0)
            elif status == 'up':
                direction = pygame.math.Vector2(0, -1)
            elif status == 'down':
                direction = pygame.math.Vector2(0, 1)
            
            self.sounds[magic_name].play()
            for i in range(1, 6):
                if direction.x:
                    offset_x = direction.x * i * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles(magic_name,
                                                           (x, y),
                                                           groups)
                else:
                    offset_y = direction.y * i * TILESIZE
                    x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles(magic_name,
                                                           (x, y),
                                                           groups)
