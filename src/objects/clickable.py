import pygame

from src.engine.config import OBJECTS_LAYER, MOUSE_HOVERED_ON_CLICKABLE
from src.engine.objects import BaseObject
from src.engine.utils import load_image, scale_image, lerp


class Clickable(BaseObject):
    def __init__(self, x, y, size, z=OBJECTS_LAYER):
        self._rect = pygame.Rect(x, y, *size)
        super().__init__(*self.rect.center, z)
        self.active = False

    def update(self, events: list[pygame.event.Event], dt):
        mx, my = pygame.mouse.get_pos()
        if self.rect.collidepoint(mx, my):
            self.active = True
            self.post_event(MOUSE_HOVERED_ON_CLICKABLE, obj=self)
        else:
            self.active = False

    @property
    def rect(self) -> pygame.Rect:
        return self._rect.move(-self._rect.w / 2, -self._rect.h / 2)


class SpriteBasedClickable(Clickable):
    def __init__(self, x, y, path, scale=1.0, appear_animate=True):
        self.img = load_image(path, scale=scale, color_key='white')
        self.mask = pygame.mask.from_surface(self.img)
        self.outline = self.mask.outline(every=5)
        self.scale = 0 if appear_animate else 1
        self.target_scale = 1
        super().__init__(x, y, self.img.get_size())

    def update(self, events: list[pygame.event.Event], dt):
        super().update(events, dt)
        mx, my = pygame.mouse.get_pos()
        if self.active:
            if not self.mask.get_at([mx - self.rect.left, my - self.rect.top]):
                self.active = False
        self.scale = lerp(self.scale, self.target_scale, 0.25 * dt)

    def draw(self, surf: pygame.Surface, offset):
        scale = self.scale
        if self.active:
            if pygame.mouse.get_pressed()[0]:
                scale += 0.05
        if scale == 1:
            img = self.img
        else:
            img = scale_image(self.img, scale)
        surf.blit(img, img.get_rect(center=self.pos + offset))
        if self.active:
            points = [pygame.Vector2(i) * scale + self.rect.scale_by(scale, scale).topleft + offset for i
                      in self.outline]
            pygame.draw.polygon(surf, 'white', points, 5)
