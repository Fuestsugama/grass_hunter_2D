import pygame 
from support import import_folder
from random import choice
from settings import monster_data, ANIMATION_SPEED


class AnimationPlayer:
    def __init__(self):
        """Load every particle animation once."""
        leaf_frames = [import_folder(f'../assets/graphics/particles/leaf{number}') for number in range(1, 7)]

        self.frames = {
            # magic
            'flame': import_folder('../assets/graphics/particles/flame/frames'),
            'aura': import_folder('../assets/graphics/particles/aura'),
            'heal': import_folder('../assets/graphics/particles/heal/frames'),

            #attacks
            'claw': import_folder('../assets/graphics/particles/claw'),
            'slash': import_folder('../assets/graphics/particles/slash'),
            'sparkle': import_folder('../assets/graphics/particles/sparkle'),
            'leaf_attack': import_folder('../assets/graphics/particles/leaf_attack'),
            'thunder': import_folder('../assets/graphics/particles/thunder'),
            'fireball': import_folder('../assets/graphics/particles/fireball'),
            'bite': import_folder('../assets/graphics/particles/bite'),
            'dig': import_folder('../assets/graphics/particles/dig'),

            # monster deaths
            'squid_ink': import_folder('../assets/graphics/particles/squid_ink'),
            'raccoon_dash': import_folder('../assets/graphics/particles/raccoon_dash'),
            'spirit_explosion': import_folder('../assets/graphics/particles/spirit_explosion'),
            'slime3': import_folder('../assets/graphics/particles/squid_ink'),
            'flam': import_folder('../assets/graphics/particles/spirit_explosion'),
            'gold_racoon': import_folder('../assets/graphics/particles/raccoon_dash'),
            'trex': import_folder('../assets/graphics/particles/raccoon_dash'),
            'spider_yellow': import_folder('../assets/graphics/particles/squid_ink'),
            'mole': import_folder('../assets/graphics/particles/dig'),
            'snake3': import_folder('../assets/graphics/particles/raccoon_dash'),
            'tengu_blue': import_folder('../assets/graphics/particles/spirit_explosion'),

            # leaves: the 6 animations, plus the same 6 mirrored
            'leaf': tuple(leaf_frames + [self.reflect_images(frames) for frames in leaf_frames]),
        }

    def reflect_images(self, frames):
        new_frames = []
        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
        return new_frames 

    def create_grass_particles(self, pos, groups):
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos, animation_frames, groups)

    def create_particles(self, animation_type, pos,groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = ANIMATION_SPEED
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()