import pygame
from support import get_screen_size

pygame.init()
WIDTH, HEIGHT = get_screen_size()
pygame.quit()

if WIDTH <= 1920:
    from settings.settings1 import *
    graphics_ind = 1
else:
    from settings.settings2 import *
    graphics_ind = 2
