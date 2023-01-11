import pygame

from random import choice
from player import Player
from tile import Tile
from weapon import Weapon
from ui import UI
from support import *
from settings import *


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.obstacle_sprites = pygame.sprite.Group()
        self.visible_sprites = YSortCameraGroup()
        self.fields = {}

        # attack sprites
        self.current_attack = None

        self.create_map()

        self.ui = UI()

        self.fighting_enemies = pygame.sprite.Group()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('../graphics/map/map_floor_blocks.csv'),
            'grass': import_csv_layout('../graphics/map/map_grass.csv'),
            'trees': import_csv_layout('../graphics/map/map_trees.csv'),
            'field_id': import_csv_layout('../graphics/map/map_field_id.csv')
        }

        graphics = {
            'grass': import_folder('../graphics/grass'),
            'trees': import_folder('../graphics/trees'),
            '?': import_folder('../graphics/question_mark')
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
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'grass', grass_image)
                        elif style == 'trees':
                            surf = graphics['trees'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)
                        elif style == 'field_id':
                            self.fields[FIELDS_IDS[int(col)]] = (x, y)

        self.player = Player(player_pos, [self.visible_sprites], self.obstacle_sprites,
                             self.create_attack, self.destroy_attack, self.create_magic, self.player_in_field)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    def create_magic(self, style, strength, cost):
        pass

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_in_field(self):
        for field_center in list(self.fields.values()):
            if self.player.rect.colliderect(field_center[0] - TILESIZE, field_center[1] - TILESIZE,
                                            TILESIZE * 3, TILESIZE * 3):
                if not self.player.battle_started:
                    self.start_battle(field_center)

    def start_battle(self, field_center):
        self.player.battle_started = True
        # вычислить номер поля, с которым взаимодействовал игрок
        field = None
        for key in self.fields:
            if self.fields[key] == field_center:
                field = key
                break
        # создать врагов на нужном поле
        self.create_enemies(field)

    def create_enemies(self, level):
        for row_index, row in enumerate(import_csv_layout(f'../graphics/map/map_level_{level}_entities.csv')):
            for col_index, col in enumerate(row):
                pass

    def battle_is_over(self):
        pass

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.image.load('../graphics/map.png').convert()
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
