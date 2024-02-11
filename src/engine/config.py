import os
import sys

# constants declaration
import pygame

import platform

GAME_NAME = 'SpaceFire Blitz'
IS_WEB = False

if sys.platform == "emscripten":
    IS_WEB = True
    platform.window.canvas.style.imageRendering = "pixelated"


class Config:
    WIDTH = 1000  # width of the screen
    HEIGHT = 800  # height of the screen
    SCREEN_RECT = pygame.Rect(0, 0, WIDTH, HEIGHT)
    SCREEN_COLLISION_RECT = SCREEN_RECT.inflate(100, 100)

    BG_COlOR = '#000011'
    TEXT_COLOR = '#511309'
    VOLUME = 100  # sound volume
    FPS = 0
    TARGET_FPS = 60


ASSETS = 'assets'
BASE_FONT = 'VeniteAdoremus.ttf'
FONT = os.path.join(ASSETS, 'fonts', BASE_FONT)
FONT_SIZES = FONT_SMALL, FONT_MEDIUM, FONT_LARGE = 12, 25, 50

(
    SONG_FINISHED_EVENT,
    DISPLAY_SUBTITLE,
    MOUSE_HOVERED_ON_CLICKABLE,
    CAMERA_SHAKE,
    BULLET_HIT,
    GAMESTAT_UPDATE,
    POWERUP_ACTIVATED,
    *_,
) = (pygame.event.custom_type() for _ in range(10))

(
    OBJECTS_LAYER,
    PLANET_LAYER,
    BULLET_LAYER,
    PLAYER_LAYER,
    UI_LAYER,
    EXPLOSION_LAYER,
    POWERUP_LAYER,
    *_
) = range(0, 10)

BASE_PATH = ''


class GAMESTATS:
    OBJECTS_SPEED = 1
    PLAYER_SPEED = 10
    BULLET_FIRE_RATE = 0.4
    PLANET_SPAWN_TIMER = 3
    PLAYER_LIVES = 3
    SCORE = 0
    POWERUP = None


class GLOBALS:
    RENDERER = None


DEBUG = True

NUMPY = True
SCIPY = True

try:
    import numpy
except ImportError:
    numpy = ...
    NUMPY = False

try:
    import scipy
except ImportError:
    scipy = ...
    SCIPY = False


# for handling global objects

class Globals:
    _global_dict = {}

    @classmethod
    def set_global(cls, key, value):
        cls._global_dict[key] = value

    @classmethod
    def get_global(cls, key):
        return cls._global_dict.get(key)

    @classmethod
    def pop_global(cls, key):
        try:
            cls._global_dict.pop(key)
        except KeyError:
            pass


# for closing pyinstaller splash screen if loaded from bundle

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    print('running in a PyInstaller bundle')
    BASE_PATH = sys._MEIPASS
    ASSETS = os.path.join(sys._MEIPASS, ASSETS)
    FONT = os.path.join(ASSETS, 'fonts', BASE_FONT)
    try:
        import pyi_splash

        pyi_splash.close()
    except ImportError:
        pass
else:
    print('running in a normal Python process')
