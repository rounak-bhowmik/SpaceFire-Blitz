import math
import os.path
import pathlib
import time
from functools import lru_cache
from pathlib import Path
from typing import Literal

import pygame

from pygame._sdl2 import video

# FONT = os.path.abspath(os.path.join(ASSETS, 'ARCADECLASSIC.TTF'))
from src.engine.config import ASSETS, FONT

from pygame.math import lerp, smoothstep


lerp = lerp
slerp = smoothstep


def clamp(value, mini, maxi):
    """Clamp pos between mini and maxi"""
    if value < mini:
        return mini
    elif maxi < value:
        return maxi
    else:
        return value


def distance(p1, p2):
    """Get distance between 2 points"""
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def map_to_range(value, from_x, from_y, to_x, to_y):
    """map the pos from one range to another"""
    return clamp(value * (to_y - to_x) / (from_y - from_x), to_x, to_y)


def load_image_without_cache(path: str, alpha: bool = True, scale=1.0, color_key=None, smooth_scale=False):
    img = pygame.image.load(path)
    img = pygame.transform.scale_by(img, scale) if not smooth_scale else pygame.transform.smoothscale_by(img, scale)
    if color_key:
        img.set_colorkey(color_key)
    if alpha:
        return img.convert_alpha()
    else:
        return img.convert()


def get_path(*args):
    if len(args) == 1 and isinstance(args[0], str):
        args = args[0].split('/')
    path = pathlib.Path(__file__).parent.parent.parent / ASSETS
    for i in args:
        path /= i
    return path


@lru_cache(maxsize=100)
def scale_image(img: pygame.Surface, scale):
    if isinstance(scale, int) or isinstance(scale, float):
        x, y = scale, scale
    else:
        x, y = scale
    return pygame.transform.scale_by(img, (x, y))


@lru_cache(maxsize=100)
def load_image(path: str, alpha: bool = True, scale=1.0, color_key=None, smooth_scale=False):
    return load_image_without_cache(path, alpha, scale, color_key, smooth_scale)


_radial_glow = None


@lru_cache(maxsize=500)
def get_radial_glow(radius, color='#D600C4'):
    global _radial_glow
    if not _radial_glow:
        _radial_glow = load_image((Path(__file__).parent.parent.parent / 'assets' / 'images' / 'glow.png').__str__(),
                                  alpha=False, color_key='black')
    if color != 'white':
        glow = _radial_glow.copy()
        glow.fill(color, special_flags=pygame.BLEND_RGB_MULT)
        return pygame.transform.scale(glow, (radius * 2, radius * 2))
    else:
        return pygame.transform.scale(_radial_glow, (radius * 2, radius * 2))


_linear_glow = None


@lru_cache(maxsize=500)
def get_linear_vertical_glow(width, height, color='#D600C4'):
    global _linear_glow
    if not _linear_glow:
        _linear_glow = load_image(
            (Path(__file__).parent.parent.parent / 'assets' / 'images' / 'linear_glow.png').__str__(), alpha=False,
            color_key='black')
    if color != 'white':
        glow = _linear_glow.copy()
        glow.fill(color, special_flags=pygame.BLEND_RGB_MULT)
        return pygame.transform.scale(glow, (width, height))
    else:
        return pygame.transform.scale(_linear_glow, (width, height))


_square_glow = None


@lru_cache(maxsize=500)
def get_rectangle_glow(width, height, color='#D600C4'):
    global _square_glow
    if not _square_glow:
        _square_glow = load_image(
            (Path(__file__).parent.parent.parent / 'assets' / 'images' / 'square_glow.png').__str__(), alpha=False,
            color_key='black')
    if color != 'white':
        glow = _square_glow.copy()
        glow.fill(color, special_flags=pygame.BLEND_RGB_MULT)
        return pygame.transform.scale(glow, (width, height))
    else:
        return pygame.transform.scale(_square_glow, (width, height))


@lru_cache(maxsize=10)
def font(size):
    return pygame.font.Font(FONT, size)
    # return pygame.font.SysFont(FONT, size)


@lru_cache(maxsize=100)
def text(msg, size=50, color=(255, 255, 255), bg_color=None, aliased=False, wraplength=0):
    return font(size).render(str(msg), aliased, color, bg_color, wraplength=wraplength)


class Timer:
    def __init__(self, timeout=0.0, reset=True):
        self.timeout = timeout
        self.timer = time.time()
        self.paused_timer = time.time()
        self.paused = False
        self._reset = reset
        self._callback = None

    def set_timeout(self, timeout):
        self.timeout = timeout

    def set_callback(self, callback):
        self._callback = callback

    def reset(self):
        self.timer = time.time()

    def pause(self):
        self.paused = True
        self.paused_timer = time.time()

    def resume(self):
        self.paused = False
        self.timer -= time.time() - self.paused_timer

    @property
    def elapsed(self):
        if self.paused:
            return time.time() - self.timer - (time.time() - self.paused_timer)
        return time.time() - self.timer

    @property
    def tick(self):
        if self.timeout == 'inf':
            return False
        if self.elapsed > self.timeout:
            if self._reset:
                self.reset()  # reset timer
            else:
                self.timeout = 'inf'
            if self._callback:
                self._callback()
            return True
        else:
            return False


class SpriteSheet:
    """
    Class to load sprite-sheets
    """

    def __init__(self, sheet, rows, cols, images=None, alpha=True, scale=1.0,
                 flipped=(0, 0), color_key=None, smooth_scale=False):
        self._sheet = load_image(
            sheet,
            scale=scale,
            smooth_scale=smooth_scale
        ) if isinstance(sheet, str) or isinstance(sheet, Path) else sheet
        self._r = rows
        self._c = cols
        self._flipped = flipped
        self._images = images if images else rows * cols
        self._alpha = alpha
        self._scale = scale
        self._color_key = color_key
        self._rects = []
        if flipped:
            self._sheet = pygame.transform.flip(self._sheet, *flipped)

    def export_sprite_sheet(self, path, rows, cols, images):
        path

    def __str__(self):
        return f'SpriteSheet Object <{self._sheet.__str__()}>'

    @property
    def surf(self):
        return self._sheet

    def get_rects(self):
        if not self._rects:
            raise Exception('Images not loaded yet from sprite sheet. Call get_images to load images first.')
        return self._rects

    def get_images(self):
        w = self._sheet.get_width() // self._c
        h = self._sheet.get_height() // self._r
        images = []
        for i in range(self._r * self._c):
            rect = pygame.Rect(i % self._c * w, i // self._c * h, w, h)
            self._rects.append(rect)
            images.append(self._sheet.subsurface(rect))
        images = images[0:self._images]
        if self._color_key is not None:
            for i in images:
                i.set_colorkey(self._color_key)
        if self._alpha:
            for i in images:
                i.convert_alpha()
        else:
            for i in images:
                i.convert()
        return images


class LoopingSpriteSheet:
    def __init__(self, sheet, rows, cols, images=None, alpha=True, scale=1.0, flipped=(0, 0), color_key=None, timer=0.1,
                 mode: Literal['center', 'topleft'] = 'center', smooth=False, callback=None):
        self.timer = Timer(timeout=timer)
        self.images = SpriteSheet(sheet, rows, cols, images, alpha, scale, flipped, color_key, smooth).get_images()
        self.c = 0
        self.mode = mode
        self.paused = False
        self._done = False
        self.callback = callback

    @property
    def width(self):
        return self.images[0].get_width()

    @property
    def height(self):
        return self.images[0].get_height()

    @property
    def size(self):
        return self.width, self.height

    @property
    def image(self):
        return self.images[self.c]

    def set_frame(self, frame):
        self.c = frame
        self.c %= len(self.images)

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    @property
    def done(self):
        return self._done

    def draw(self, surf: pygame.Surface, x, y, angle=0, size=1, flip=(0, 0)):
        if not self.paused:
            if self.timer.tick:
                self.c += 1
                if self.c == len(self.images) - 1:
                    if self.callback:
                        self.callback()
                    self._done = True
                else:
                    self._done = False
                self.c %= len(self.images)
        img = self.image
        if size != 1:
            img = pygame.transform.scale_by(img, size)
        if angle != 0:
            img = pygame.transform.rotate(img, angle)
        if flip:
            img = pygame.transform.flip(img, *flip)
        if self.mode == 'center':
            surf.blit(img, img.get_rect(center=(x, y)))
        else:
            surf.blit(img, (x, y))


class LinearInterpolator:
    def __init__(self, val, amount, final):
        self.val = pygame.Vector2(val, val)
        self.amt = amount
        self.final = pygame.Vector2(final, final)

    @property
    def value(self):
        return self.val.x

    @property
    def next(self):
        return self.lerp()

    def lerp(self):
        self.val = self.val.lerp(self.final, self.amt)
        return self


class Tween:
    @staticmethod
    def ease_in_sine(x):
        return 1 - math.cos(math.pi * x / 2)
