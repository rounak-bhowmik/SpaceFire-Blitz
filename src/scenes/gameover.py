import pygame

from src.engine.scene import Scene
from src.engine.utils import *
from src.engine.config import *
from src.engine.sounds import *


class GameOverScene(Scene):
    def __init__(self, manager, name):
        super().__init__(manager, name)
        self.bg = load_image_without_cache(get_path('images', 'background', 'bg1.png'), False)
        self.bg.fill([150] * 3, special_flags=pygame.BLEND_RGB_MULT)
        self.options = [
            'Replay', 'Home', 'Quit'
        ]
        self.actions = [
            lambda: self.manager.switch_mode('gamescene', True, True, False),
            lambda: self.manager.switch_mode('home', True, True, False),
            lambda: sys.exit(0)
        ]
        self.selected = 0
        self.sheet = LoopingSpriteSheet(get_path('images', 'background', f'planet{2}.png'), 10, 20,
                                        timer=0.08, scale=4)

    def enter(self):
        SoundManager.play('bg', loops=-1, volume=80)

    def exit(self):
        SoundManager.stop('bg')

    def update(self, events: list[pygame.event.Event], dt):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    SoundManager.play('click')
                    self.selected -= 1
                if e.key == pygame.K_DOWN:
                    SoundManager.play('click')
                    self.selected += 1
                if e.key == pygame.K_RETURN:
                    SoundManager.play('select')
                    try:
                        if self.actions[self.selected]:
                            self.actions[self.selected]()
                    except IndexError:
                        pass
        self.selected %= len(self.options)

    def draw(self, surf: pygame.Surface, offset):
        surf.blit(self.bg, (0, 0))
        title = text('Game Over!', 60)
        score = text('Your Score:', 45)
        surf.blit(score, score.get_rect(center=(Config.WIDTH / 2, 200)))
        score = text(str(GAMESTATS.SCORE), 100)
        surf.blit(score, score.get_rect(center=(Config.WIDTH / 2, 290)))
        y = 500
        for i, j in enumerate(self.options):
            _text = j
            if i == self.selected:
                _text = '> ' + j
            else:
                _text = '   ' + j
            t = text(_text, 50)
            surf.blit(t, t.get_rect(midleft=[150, y]))
            y += 75
        self.sheet.draw(surf, 650, 550)
        surf.blit(title, title.get_rect(center=(Config.WIDTH / 2, 100)))
