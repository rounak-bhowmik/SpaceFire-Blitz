import random

import pygame

from src.engine.config import Config
from src.engine.objects import ObjectManager
from src.engine.scene import Scene
from src.engine.utils import *
from src.objects.planet import Planet
from src.objects.player import Player
from src.objects.powerup import *
from src.engine.sounds import *
from src.engine.subtitles import SubtitleManager, Subtitle


class GameScene(Scene):
    def __init__(self, manager, name):
        super().__init__(manager, name)
        self.object_manager = ObjectManager()
        self.object_manager.add_multiple(
            [
                player := Player(Config.WIDTH / 2, Config.HEIGHT - 150),
            ]
        )
        self.bg = load_image_without_cache(get_path('images', 'background', 'bg1.png'), False)
        self.bg.fill([105] * 3, special_flags=pygame.BLEND_RGB_MULT)
        self.planet_spawner = Timer(GAMESTATS.PLANET_SPAWN_TIMER)
        self.object_manager.add(Planet(random.randint(0, Config.WIDTH), -150))
        self.powerup_spawner = Timer(5)
        # self.object_manager.add(Star(150, -10))
        self.bg_y = 0
        self.life_img = load_image(get_path('images', 'ui', 'heart.png'), scale=4)
        self.player = player
        self.powerup_timer = Timer(3)
        self.first_powerup_done = False

    def enter(self):
        GAMESTATS.OBJECTS_SPEED = 1
        GAMESTATS.PLAYER_SPEED = 10
        # GAMESTATS.POWERUP_SPAWN_RATE =
        GAMESTATS.BULLET_FIRE_RATE = 0.4
        GAMESTATS.PLANET_SPAWN_TIMER = 2
        GAMESTATS.PLAYER_LIVES = 3
        GAMESTATS.SCORE = 0
        GAMESTATS.POWERUP = None
        self.player.start()
        self.first_powerup_done = False
        self.powerup_spawner = Timer(5)
        # SoundManager.set_bg_volume(0.1)
        SoundManager.play('bg', volume=50, loops=-1)

    def exit(self):
        pass
        SoundManager.stop('bg')

    def update(self, events: list[pygame.event.Event], dt):
        for e in events:
            if e.type == POWERUP_ACTIVATED:
                self.powerup_timer.reset()
        self.object_manager.update(events, dt)
        if self.planet_spawner.tick:
            self.object_manager.add(
                Planet(random.randint(0, Config.WIDTH), -250)
            )
        self.bg_y += 0.5 * dt
        if self.bg_y >= self.bg.get_height():
            self.bg_y = 0
        if GAMESTATS.PLAYER_LIVES < 0:
            self.manager.switch_mode('gameoverscene', True, True, False)
        if self.powerup_timer.tick:
            if GAMESTATS.POWERUP:
                GAMESTATS.POWERUP.on_deactivate()
                GAMESTATS.POWERUP = None
        if self.powerup_spawner.tick:
            self.object_manager.add(
                random.choice([HyperBullet])(random.randint(50, Config.WIDTH - 50), -150)
            )
            if not self.first_powerup_done:
                self.first_powerup_done = True
                self.powerup_spawner.timeout = 10

    def draw(self, surf: pygame.Surface, offset):
        surf.blit(self.bg, (0, self.bg_y))
        if self.bg_y > 0:
            diff = self.bg_y
            surf.blit(self.bg, (0, 0), area=[0, self.bg.get_height() - diff, self.bg.get_width(), diff])
        self.object_manager.draw(surf, offset)
        # UI Layer
        score = text('SCORE', 25)
        surf.blit(score, score.get_rect(topright=(Config.WIDTH - 25, 10)))
        score = text(str(GAMESTATS.SCORE), 50)
        surf.blit(score, score.get_rect(topright=(Config.WIDTH - 25, 35)))
        for i in range(GAMESTATS.PLAYER_LIVES):
            surf.blit(self.life_img, (25 + i * 70, 25))
