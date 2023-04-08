import pygame

from entity import Entity
from support import *
from import_settings import *


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic, player_in_field, start_battle):
        super().__init__(groups)
        self.sprite_type = 'player'
        self.image = pygame.image.load(f'../graphics/characters{graphics_ind}/hero/down/down_0.png')
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -TILESIZE // 3)

        self.import_player_assets()
        self.status = 'down'

        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        # оружие
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # магия
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        self.stats = {'health': 100, 'mana': 100, 'speed': PLAYER_SPEED}
        self.current_health = self.stats['health']
        self.current_mana = self.stats['mana']

        self.obstacle_sprites = obstacle_sprites

        # бой
        self.battle_started = False
        self.player_in_field = player_in_field
        self.start_battle = start_battle

        self.unprotected = True
        self.hit_time = None
        self.protected_duration = 500

        # звук
        self.sound = pygame.mixer.Sound('../audio/hit.wav')
        self.sound.set_volume(0.2)

    def import_player_assets(self):
        character_path = f'../graphics/characters{graphics_ind}/hero'
        self.animations = {
            'up': [],
            'down': [],
            'left': [],
            'right': [],
            'right_idle': [],
            'left_idle': [],
            'up_idle': [],
            'down_idle': [],
            'right_attack': [],
            'left_attack': [],
            'up_attack': [],
            'down_attack': []
        }

        for animation in self.animations:
            self.animations[animation] = import_folder(character_path + '/' + animation)

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            # движение
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # начать бой
            if keys[pygame.K_g]:
                if not self.battle_started:
                    in_field, field_center = self.player_in_field()
                    if in_field:
                        self.start_battle(field_center)

            # атака
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.sound.play()

            # магия
            if keys[pygame.K_e]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()

                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength']
                cost = list(magic_data.values())[self.magic_index]['cost']

                self.create_magic(style, strength, cost)

            if keys[pygame.K_TAB] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()

                if self.weapon_index < len(weapon_data.keys()) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0

                self.weapon = list(weapon_data.keys())[self.weapon_index]

            if keys[pygame.K_CAPSLOCK] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()

                if self.magic_index < len(magic_data.keys()) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0

                self.magic = list(magic_data.keys())[self.magic_index]

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if 'idle' not in self.status and 'attack' not in self.status:
                self.status += '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if 'attack' not in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status += '_attack'
        else:
            if '_attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.unprotected:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.stats['speed'])
        self.mana_recovery()

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True
        
        if not self.unprotected:
            if current_time - self.hit_time >= self.protected_duration:
                self.unprotected = True
    
    def mana_recovery(self):
        if self.current_mana < self.stats['mana']:
            self.current_mana += 0.03
        else:
            self.current_mana = self.stats['mana']
