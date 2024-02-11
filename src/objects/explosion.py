import random

from src.engine.objects import BaseObject
from src.engine.config import *
from src.engine.utils import *


class Explosion(BaseObject):
    def __init__(self, x, y, scale=4):
        super().__init__(x, y, EXPLOSION_LAYER)
        self.sheet = LoopingSpriteSheet(get_path('images', 'explosion', 'explosion1.png'), 1, 12,
                                        alpha=False, scale=scale + 1, color_key='#061D29')

        self.sheet.callback = self.destroy
        self.spawned_timer = Timer(0.25, reset=False)
        self.scale = scale

    def update(self, events: list[pygame.event.Event], dt):
        return
        # if self.spawned_timer.tick:
        #     for i in range(self.scale):
        #         self.object_manager.add(
        #             Explosion(*(self.pos + [random.randint(-50, 50), random.randint(-50, 50)]), self.scale - 1)
        #         )

    def draw(self, surf: pygame.Surface, offset):
        self.sheet.draw(surf, *(self.pos + offset))


class PowerUpExplosion(BaseObject):
    def __init__(self, x, y):
        super().__init__(x, y, EXPLOSION_LAYER)
        self.sheet = LoopingSpriteSheet(get_path('images', 'explosion', 'powerup_explosion.png'), 5, 4,
                                        alpha=False, scale=2, color_key='#061D29', timer=0.02)

        self.sheet.callback = self.destroy

    def draw(self, surf: pygame.Surface, offset):
        self.sheet.draw(surf, *(self.pos + offset))
