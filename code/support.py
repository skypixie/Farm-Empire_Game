from csv import reader
from os import walk

import pygame


def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_folder(path):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


def get_screen_size():
    w, h = pygame.display.Info().current_w, pygame.display.Info().current_h
    return w, h

def reversed_dict(d):
    res = dict()
    keys = list(d.keys())
    values = list(d.values())
    for i in range(len(values)):
        res[values[i]] = keys[i]
    return res
