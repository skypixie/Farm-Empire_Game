import pygame

from entity import Entity
from support import import_folder
from import_settings import *

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, create_death_particles):
        super().__init__(groups)
        self.sprite_type = 'enemy'

        self.import_images(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        self.name = monster_name
        stats = monster_data[monster_name]
        self.health = stats['health']
        self.speed = stats['speed']
        self.damage = stats['damage']
        self.attack_type = stats['attack_type']
        self.resistance = stats['resistance']
        self.attack_radius = stats['attack_radius']
        self.notice_radius = stats['notice_radius']

        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 1000
        self.damage_player = damage_player
        self.create_death_particles = create_death_particles

        self.unprotected = True
        self.hit_time = None
        self.protected_duration = 300

        self.death_sound = pygame.mixer.Sound('../audio/kill.wav')
        self.death_sound.set_volume(0.3)

    def import_images(self, name):
        self.animations = {'idle': [], 'attack': [], 'move': []}
        for folder_name in self.animations:
            self.animations[folder_name] = import_folder(f'../graphics/characters{graphics_ind}/monsters/{name}/{folder_name}')
    
    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations[self.status]):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0
        
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.unprotected:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
    
    def set_status(self, player):
        distance = self.get_player_distance_and_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'
    
    def get_player_distance_and_direction(self, player):
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)

        distance = (player_vector - enemy_vector).magnitude()
        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
        else:
            direction = pygame.math.Vector2()

        return distance, direction
    
    def actions(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.damage, self.attack_type)
        elif self.status == 'move':
            self.direction = self.get_player_distance_and_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()
    
    def get_hit(self, player, attack_sprite_type):
        if self.unprotected:
            self.direction = self.get_player_distance_and_direction(player)[1]
            if attack_sprite_type == 'weapon':
                self.health -= weapon_data[player.weapon]['damage']
            else:
                self.health -= magic_data[player.magic]['strength']
            self.hit_time = pygame.time.get_ticks()
            self.unprotected = False
    
    def check_death(self):
        if self.health <= 0:
            self.death_sound.play()
            self.create_death_particles(self.rect.center, self.name)
            self.kill()
    
    def hit_reaction(self):
        if not self.unprotected:
            self.direction *= -self.resistance
    
    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()
    
    def enemy_update(self, player):
        self.set_status(player)
        self.actions(player)
    
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        if not self.unprotected:
            if current_time - self.hit_time >= self.protected_duration:
                self.unprotected = True
