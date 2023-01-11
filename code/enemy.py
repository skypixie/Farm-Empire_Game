import pygame

from entity import Entity
from support import import_folder
from settings import *

class Enemy(Entity):
    def __init__(self, groups, name, pos, ):
        super().__init__(groups)
        self.set_images(name)

    def set_images(self, name):
        self.animations = {'idle': [], 'attack': [], 'move': []}
        for folder_name in self.animations:
            self.animations[folder_name] = import_folder(f'../graphics/characters/monsters/{name}/{folder_name}')
