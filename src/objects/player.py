import pygame.key

from src.engine.objects import BaseObject
from src.engine.utils import *
from src.engine.config import *
from src.engine.sounds import *


class Player(BaseObject):
    def __init__(self, x, y, ship_id=1):
        super().__init__(x, y, PLAYER_LAYER)
        # self.image = load_image(get_path(ASSETS, 'images', 'spaceship', 'spaceship1.png'))
        self.sheet = LoopingSpriteSheet(get_path('images', 'spaceships', f'Ship_{ship_id}.png'), 1, 1, scale=3)
        self.bullet_timer = Timer(GAMESTATS.BULLET_FIRE_RATE)
        self.scale = 1
        self.blinking = False
        self.blink_count = 0
        self.visible = True
        self.blink_timer = Timer(0.1)

    def start(self):
        SoundManager.play('player_thrust', -1, volume=20)

    @property
    def rect(self) -> pygame.Rect:
        return self.sheet.image.get_rect(center=self.pos).scale_by(0.8, 0.8)

    def get_hit(self):
        GAMESTATS.PLAYER_LIVES -= 1
        self.blinking = True
        self.blink_timer.reset()
        if GAMESTATS.PLAYER_LIVES < 0:
            SoundManager.stop('player_thrust')
        SoundManager.play('hit')

    def update(self, events: list[pygame.event.Event], dt):
        keys = pygame.key.get_pressed()
        speed = GAMESTATS.PLAYER_SPEED  # pixels per frame (standardized at 60 FPS)
        vec = pygame.Vector2()
        if keys[pygame.K_LEFT]:
            vec.x -= 1
        if keys[pygame.K_RIGHT]:
            vec.x += 1
        if keys[pygame.K_UP]:
            vec.y -= 1
        if keys[pygame.K_DOWN]:
            vec.y += 1
        vec = vec.normalize() if not vec.is_normalized() and vec.length() != 0 else vec
        self.x += vec.x * speed * dt
        self.y += vec.y * speed * dt
        w = self.sheet.image.get_width()
        h = self.sheet.image.get_width()
        self.x = clamp(self.x, w / 2, Config.WIDTH - w / 2)
        self.y = clamp(self.y, h / 2, Config.HEIGHT - h / 2)
        # print(GAMESTATS.BULLET_FIRE_RATE)
        if self.bullet_timer.timeout != GAMESTATS.BULLET_FIRE_RATE:
            self.bullet_timer.timeout = GAMESTATS.BULLET_FIRE_RATE
        if self.bullet_timer.tick:
            SoundManager.play('shoot', volume=20)
            self.object_manager.add(
                PlayerBullet(self.x, self.y - self.sheet.image.get_height() / 2)
            )
            self.post_event(CAMERA_SHAKE, intensity=1)
            self.scale = 1.5

        self.scale = lerp(self.scale, 1, 0.4 * dt)

        if self.blinking:
            if self.blink_count >= 20:
                self.blink_count = 0
                self.visible = True
                self.blinking = False
                self.blink_timer.reset()
            if self.blink_timer.tick:
                self.visible = not self.visible
                self.blink_count += 1

    def draw(self, surf: pygame.Surface, offset):
        if self.visible:
            self.sheet.draw(surf, *(self.pos + offset), size=self.scale)


class PlayerBullet(BaseObject):
    def __init__(self, x, y, strength=1):
        super().__init__(x, y, BULLET_LAYER)
        self.sheet = LoopingSpriteSheet(get_path('images', 'projectiles', 'bullet1.png'), 1, 4, scale=3)
        self.strength = strength

    @property
    def rect(self) -> pygame.Rect:
        return self.sheet.image.get_rect(center=self.pos)

    def update(self, events: list[pygame.event.Event], dt):
        speed = 8
        self.y -= speed * dt
        if self.y < 0:
            self.destroy()
        # if not Config.SCREEN_COLLISION_RECT.scale_by(2, 2).collidepoint(*self.pos):
        #     self.destroy()
        for e in events:
            if e.type == BULLET_HIT:
                if e.bullet == self:
                    self.destroy()

    def draw(self, surf: pygame.Surface, offset):
        self.sheet.draw(surf, *(self.pos + offset))
