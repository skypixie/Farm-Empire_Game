import pygame
import sqlite3

from random import choice
from player import Player
from enemy import Enemy
from tile import Tile
from weapon import Weapon
from ui import UI
from game_menu import Menu
from particles import AnimationPlayer
from magic import Magic
from support import *
from import_settings import *



class Level:
    def __init__(self, graphics_index, exit_from_game):
        self.display_surface = pygame.display.get_surface()
        self.graphics_index = graphics_index

        self.running = True

        self.obstacle_sprites = pygame.sprite.Group()
        self.visible_sprites = YSortCameraGroup(self.graphics_index)
        self.attack_sprites = pygame.sprite.Group()
        self.attackale_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.fields = {}

        self.passed_fields = set()

        # attack sprites
        self.current_attack = None

        # sql
        self.con = sqlite3.connect('database/progress_db.sqlite3')
        self.cur = self.con.cursor()

        self.create_map()

        self.ui = UI()
        self.game_menu = Menu(exit_from_game)

        self.animation_player = AnimationPlayer()
        self.magic_player = Magic(self.animation_player)

        self.game_paused = False

        self.field_passed_sound = pygame.mixer.Sound('../audio/success.wav')
        self.field_passed_sound.set_volume(0.4)

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('../graphics/map/map_floor_blocks.csv'),
            'grass': import_csv_layout('../graphics/map/map_grass.csv'),
            'trees': import_csv_layout('../graphics/map/map_trees.csv'),
            'field_id': import_csv_layout('../graphics/map/map_field_id.csv'),
            'entities': import_csv_layout('../graphics/map/map_entities.csv')
        }

        graphics = {
            'grass': import_folder(f'../graphics/grass{self.graphics_index}'),
            'trees': import_folder(f'../graphics/trees{self.graphics_index}'),
        }

        player_pos = ()
        for row_index, row in enumerate(import_csv_layout('../graphics/map/map_player.csv')):
            for col_index, col in enumerate(row):
                if col != '-1':
                    x, y = col_index * TILESIZE, row_index * TILESIZE
                    player_pos = (x, y)

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        
                        elif style == 'grass':
                            grass_image = choice(graphics['grass'])
                            Tile((x, y),
                                 [self.visible_sprites, self.obstacle_sprites, self.attackale_sprites],
                                 'grass', grass_image)
                        
                        elif style == 'trees':
                            surf = graphics['trees'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)
                        
                        elif style == 'field_id':
                            self.fields[FIELDS_IDS[int(col)]] = (x, y)
                            if self.cur.execute(f"SELECT * FROM fields WHERE id = {FIELDS_IDS[int(col)]}").fetchall()[0][1]:
                                self.passed_fields.add(FIELDS_IDS[int(col)])
                                Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object',
                                     pygame.image.load(f'../graphics/food_tree/{graphics_ind}.png'))
                        
                        elif style == 'entities':
                            self.player = Player(player_pos, [self.visible_sprites], self.obstacle_sprites, 
                                                 self.create_attack, self.destroy_attack,
                                                 self.create_magic, self.player_in_field,
                                                 self.start_battle)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])
        elif style in ('flame', 'spark'):
            self.magic_player.long_spell(self.player, cost, style, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_in_field(self):
        for field_center in list(self.fields.values()):
            if self.player.rect.colliderect(field_center[0] - TILESIZE, field_center[1] - TILESIZE,
                                            TILESIZE * 3, TILESIZE * 3):
                return True, field_center
        return (None, None)
    
    def get_field_id(self):
        for field_id in self.fields:
            field_center = self.fields[field_id]
            if self.player.rect.colliderect(field_center[0] - TILESIZE, field_center[1] - TILESIZE,
                                            TILESIZE * 3, TILESIZE * 3):
                return field_id

    def start_battle(self, field_center):
        self.player.battle_started = True

        # вычислить номер поля, с которым взаимодействовал игрок
        for key in self.fields:
            if self.fields[key] == field_center:
                field = key
                break
        
        self.player.battle_field = field
        field_passed = self.cur.execute(f'SELECT * FROM fields WHERE id = {field}').fetchall()[0][1]
        if not field_passed:
            # создать врагов на нужном поле
            self.create_enemies(field)

    def create_enemies(self, level):
        for row_index, row in enumerate(import_csv_layout(f'../graphics/map/map_level_{level}_entities.csv')):
            for col_index, col in enumerate(row):
                if col != '-1':
                    x = TILESIZE * col_index
                    y = TILESIZE * row_index
                    monster_name = choice(list(monster_data.keys()))
                    Enemy(monster_name, (x, y),
                    [self.visible_sprites, self.attackale_sprites, self.enemies], self.obstacle_sprites,
                    self.damage_player, self.create_death_particles)

    def battle_is_over(self):
        if not self.enemies:
            self.log_progress()
            self.spawn_apple_tree()
            self.player.battle_started = False
            self.field_passed_sound.play()
            
            if len(self.passed_fields) == 4:
                self.show_congrats_screen()
            else:
                self.show_field_passed_screen()
    
    def spawn_apple_tree(self):
        for row_index, row in enumerate(import_csv_layout('../graphics/map/map_field_id.csv')):
            for col_index, col in enumerate(row):
                if col != '-1':
                    x = TILESIZE * col_index
                    y = TILESIZE * row_index
                    if col == str(reversed_dict(FIELDS_IDS)[self.player.battle_field]):
                        Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object',
                             pygame.image.load(f'../graphics/food_tree/{graphics_ind}.png'))
    
    def log_progress(self):
        con = sqlite3.connect('database/progress_db.sqlite3')
        cur = con.cursor()
        cur.execute(f"UPDATE fields SET passed = 1 WHERE id = {self.player.battle_field}")
        con.commit()

        self.passed_fields.add(self.player.battle_field)
    
        # проверка, пройдены ли все поля и показывалось ли уведомление прежде
        fields = cur.execute("SELECT * FROM fields").fetchall()
        all_passed = True
        for field in fields:
            if not field[1]:
                all_passed = False
        
        with open('congrats.txt') as file:
            if file.read().strip() == 'NO':
                player_was_not_congrat = True
            else:
                player_was_not_congrat = False

        if all_passed and player_was_not_congrat:
            self.show_congrats_screen()
            with open('congrats.txt', 'w') as file:
                file.write('YES')
        
        con.close()

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                attacked_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackale_sprites, False)
                if attacked_sprites:
                    for target_sprite in attacked_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            for i in range(2):
                                self.animation_player.create_grass_particles(pos, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_hit(self.player, attack_sprite.sprite_type)
    
    def create_death_particles(self, pos, type):
        self.animation_player.create_particles(type, pos, [self.visible_sprites])

    def damage_player(self, damage, attack_type):
        if self.player.unprotected and self.player.current_health - damage > 0:
            self.player.current_health -= damage
            self.player.unprotected = False
            self.player.hit_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type,
                                                          self.player.rect.center,
                                                          [self.visible_sprites])
        elif self.player.current_health - damage <= 0:
            # Игрок умер
            self.running = False

    def run(self):
        self.visible_sprites.custom_draw(self.player)

        if self.game_paused:
            self.game_menu.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()

            if self.player_in_field()[0] and not self.player.battle_started and\
                    not self.get_field_id() in self.passed_fields:
                self.ui.display_start_battle()

            if self.player.battle_started:
                self.battle_is_over()
            
            self.ui.display(self.player)

    def show_congrats_screen(self):
        image = pygame.image.load(f'../graphics/congrats{self.graphics_index}.png')
        rect = image.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        self.display_surface.blit(image, rect)
        pygame.display.flip()

        start_ticks = pygame.time.get_ticks()
        while True:
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            if seconds > 4:
                break
        self.toggle_menu()
    
    def show_field_passed_screen(self):
        image = pygame.image.load(f'../graphics/hud/field_passed{graphics_ind}.png')
        rect = image.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        self.display_surface.blit(image, rect)
        pygame.display.flip()

        start_ticks = pygame.time.get_ticks()
        while True:
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000
            if seconds > 3:
                break


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self, graphics_index):
        super().__init__()
        self.graphics_ind = graphics_index

        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.image.load(f'../graphics/map{self.graphics_ind}.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda x: x.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
    
    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
