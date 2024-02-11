from src.engine.objects import BaseObject
from src.engine.config import *
from src.engine.utils import *
from src.objects.player import Player, PlayerBullet
from src.objects.explosion import PowerUpExplosion


class PowerUp(BaseObject):
    def __init__(self, x, y):
        super().__init__(x, y, POWERUP_LAYER)
        self.sheet = LoopingSpriteSheet(**self.sprite_sheet_kwargs())

    @property
    def rect(self) -> pygame.Rect:
        return self.sheet.image.get_rect(center=self.pos).scale_by(0.8, 0.8)

    def destroy(self):
        super().destroy()
        self.object_manager.add(
            PowerUpExplosion(*self.pos)
        )

    def on_activate(self):
        raise NotImplementedError

    def on_deactivate(self):
        raise NotImplementedError

    def sprite_sheet_kwargs(self):
        raise NotImplementedError

    def update(self, events: list[pygame.event.Event], dt):
        self.y += GAMESTATS.OBJECTS_SPEED * dt
        if self.y - self.sheet.size[1] > Config.HEIGHT:
            self.destroy()

    def interact_with(self, objects: list['BaseObject']):
        if self.y < 50:
            return
        for i in objects:
            if isinstance(i, PlayerBullet):
                if self.rect.colliderect(i.rect):
                    GAMESTATS.POWERUP = self
                    self.on_activate()
                    self.post_event(BULLET_HIT, bullet=i)
                    i.destroy()
                    self.destroy()
            elif isinstance(i, Player):
                if self.rect.colliderect(i.rect):
                    GAMESTATS.POWERUP = self
                    self.on_activate()
                    self.destroy()
                    self.post_event(GAMESTAT_UPDATE)

    def draw(self, surf: pygame.Surface, offset):
        self.sheet.draw(surf, *(self.pos + offset))


class HyperBullet(PowerUp):
    def sprite_sheet_kwargs(self):
        return {
            'sheet': get_path('images', 'background', 'star.png'),
            'rows': 10,
            'cols': 20,
        }

    def on_activate(self):
        GAMESTATS.BULLET_FIRE_RATE = 0.1
        self.post_event(POWERUP_ACTIVATED)
        self.post_event(DISPLAY_SUBTITLE, text=self.__class__.__name__, time=0.5)

    def on_deactivate(self):
        print('hiiii')
        GAMESTATS.BULLET_FIRE_RATE = 0.4


class Shield(PowerUp):
    def sprite_sheet_kwargs(self):
        return {
            'sheet': get_path('images', 'background', 'star1.png'),
            'rows': 10,
            'cols': 20,
        }

    def on_activate(self):
        pass

    def on_deactivate(self):
        pass
