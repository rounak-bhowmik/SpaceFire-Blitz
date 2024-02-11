import asyncio
from pathlib import Path

import pygame

from src.engine.config import *
from src.engine.scene import SceneManager
from src.engine.sounds import SoundManager
from src.engine.utils import clamp, text

import os

# os.environ['SDL_HINT_RENDER_SCALE_QUALITY'] = '0'

parent = Path(__file__).parent
sys.path.append(parent.absolute().__str__())
#
try:
    pygame.mixer.init()
    pygame.mixer.set_num_channels(32)
    Globals.set_global('speakers_init', True)
    # SoundManager.load_sounds()
except pygame.error:
    Globals.set_global('speakers_init', False)
    try:
        pygame.init()
    except pygame.error:
        pass

#
SoundManager.load_sounds()
#
# pygame.key.set_repeat(500, 50)

pygame.init()


class Game:
    def __init__(self):
        # modified display.set_mode usage to include Window API
        full_screen = False
        # self.window = pygame.Window(GAME_NAME, [Config.WIDTH, Config.HEIGHT])
        self.screen = pygame.display.set_mode([Config.WIDTH, Config.HEIGHT], pygame.SCALED)
        # self.window = pygame.Window.from_display_module()
        # self.window.borderless = True
        # self.window.resizable = True
        # pygame.key.set_repeat(500, 10)
        self.full_screen = full_screen
        # if self.full_screen:
        #     self.window.set_fullscreen(True)
        self.manager = SceneManager()
        self.clock = pygame.time.Clock()
        # SoundManager.play_bg('through space.ogg')
        if not IS_WEB:
            self.toggle_full_screen()

    def toggle_full_screen(self):
        self.full_screen = not self.full_screen
        if self.full_screen:
            self.screen = pygame.display.set_mode([Config.WIDTH, Config.HEIGHT], pygame.SCALED | pygame.FULLSCREEN)
            # self.window.set_fullscreen(True)
            # src.engine.config.WIDTH, src.engine.config.HEIGHT = [1920, 1080]
        else:
            self.screen = pygame.display.set_mode([Config.WIDTH, Config.HEIGHT], pygame.SCALED)
            # self.window.set_windowed()

    async def run(self):
        dt = 1
        fps = 60
        while True:
            mouse_hovered = False
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    sys.exit(0)
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_f:
                        self.toggle_full_screen()
                    if e.key == pygame.K_ESCAPE:
                        sys.exit(0)
                    if e.key == pygame.K_c:
                        if fps == 60:
                            fps = 0
                        else:
                            fps = 60
                if e.type == MOUSE_HOVERED_ON_CLICKABLE:
                    mouse_hovered = True
            if mouse_hovered:
                if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_HAND:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            await asyncio.sleep(0)
            self.manager.update(events, dt)
            # t = text('FPS: ' + str(int(self.clock.get_fps())))
            self.manager.draw(self.screen, (0, 0))
            # self.screen.blit(t, [0, 0])
            pygame.display.update()

            SoundManager.update()
            self.clock.tick(fps)
            try:
                dt = Config.TARGET_FPS / self.clock.get_fps()
            except ZeroDivisionError:
                dt = 1
            dt = clamp(dt, 0.1, 2)
