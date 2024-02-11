import random

import pygame

from src.engine.objects import BaseObject
from src.engine.config import *
from src.engine.utils import *
from src.objects.player import Player, PlayerBullet
from src.objects.explosion import Explosion
from src.engine.sounds import *


class Planet(BaseObject):
    def __init__(self, x, y):
        super().__init__(x, y, PLANET_LAYER)
        planet_index = random.randint(1, 5)
        self.size = random.randint(1, 3)
        self.sheet = LoopingSpriteSheet(get_path('images', 'background', f'planet{planet_index}.png'), 10, 20,
                                        timer=0.08, scale=self.size)
        self.alpha = 0
        self.overlay = self.sheet.image.copy()
        mask = pygame.mask.from_surface(self.overlay)
        self.overlay = mask.to_surface()
        # self.overlay.fill('red')
        self.overlay.fill('white', special_flags=pygame.BLEND_RGBA_MULT)
        self.overlay.set_colorkey('black')
        self.hit_count = self.size * 4

    @property
    def rect(self) -> pygame.Rect:
        return self.sheet.image.get_rect(center=self.pos).scale_by(0.8, 0.8)

    def destroy(self):
        super().destroy()
        self.object_manager.add(
            Explosion(*self.pos, self.size)
        )
        GAMESTATS.PLANET_SPAWN_TIMER -= 0.05
        if GAMESTATS.PLANET_SPAWN_TIMER <= 2:
            GAMESTATS.PLANET_SPAWN_TIMER = 2

    def update(self, events: list[pygame.event.Event], dt):
        self.y += GAMESTATS.OBJECTS_SPEED * dt
        self.alpha = lerp(self.alpha, 0, 0.1 * dt)
        if self.hit_count < 0:
            GAMESTATS.SCORE += self.size * 150
            SoundManager.play('explosion', volume=100)
            SoundManager.play('explosion1', volume=100)
            self.destroy()
        if self.y - self.sheet.size[1] > Config.HEIGHT:
            self.destroy()

    def interact_with(self, objects: list['BaseObject']):
        for i in objects:
            if isinstance(i, PlayerBullet):
                if self.rect.colliderect(i.rect):
                    self.alpha = 250
                    self.post_event(BULLET_HIT, bullet=i)
                    self.hit_count -= i.strength
                    SoundManager.play('planet_hit', volume=25)
                    i.destroy()
            elif isinstance(i, Player):
                if not i.blinking and self.rect.colliderect(i.rect):
                    i.get_hit()
                    self.post_event(CAMERA_SHAKE, intensity=20)

    def draw(self, surf: pygame.Surface, offset):
        self.sheet.draw(surf, *(self.pos + offset))
        if self.alpha > 1:
            self.overlay.set_alpha(self.alpha)
            surf.blit(self.overlay, self.overlay.get_rect(center=(self.pos + offset)))
