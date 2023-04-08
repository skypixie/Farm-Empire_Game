import pygame
from support import import_folder
from random import choice
from import_settings import graphics_ind


class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # магия
            'flame': import_folder(f'../graphics/particles{graphics_ind}/flame/frames'),
            'heal': import_folder(f'../graphics/particles{graphics_ind}/heal/frames'),
            'spark': import_folder(f'../graphics/particles{graphics_ind}/spark/frames'),
            'aura': import_folder(f'../graphics/particles{graphics_ind}/aura'),

            # атаки
            'slash': import_folder(f'../graphics/particles{graphics_ind}/slash'),
            'claw': import_folder(f'../graphics/particles{graphics_ind}/claw'),
            'thunder': import_folder(f'../graphics/particles{graphics_ind}/thunder'),

            # смерть противника
            'reptile': import_folder(f'../graphics/particles{graphics_ind}/smoke'),
            'dragon': import_folder(f'../graphics/particles{graphics_ind}/bamboo'),
            'mole': import_folder(f'../graphics/particles{graphics_ind}/nova'),
            'leaf': (import_folder(f'../graphics/particles{graphics_ind}/leaf'),
                     self.reverse_frames(import_folder(f'../graphics/particles{graphics_ind}/leaf2')))
        }
    
    def reverse_frames(self, frames):
        result = []
        for img in frames:
            result.append(pygame.transform.flip(img, False, True))
        
        return result
    
    def create_grass_particles(self, pos, groups):
        frames = choice(self.frames['leaf'])
        ParticleEffect(pos, frames, groups)
    
    def create_particles(self, attack_type, pos, groups):
        frames = self.frames[attack_type]
        ParticleEffect(pos, frames, groups)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = 0.30
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
    
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]
    
    def update(self):
        self.animate()
