import pygame

from src.engine.objects import BaseObject
import json


class Cuisine:
    def __init__(self, name):
        self.name = name


class Ingredient:
    def __init__(self, name, path, *args):
        self.name = name
        self.path = path
        self.attrs = args


class RecipeStep:
    def __init__(self, desc):
        pass


class Recipe(BaseObject):
    def __init__(self, name, cuisine, ingredients, steps):
        self.name = name
        self.cuisine = cuisine
        self.ingredients = ingredients
        self.steps = steps
        self.current_step = 0
        super().__init__()

    def update(self, events: list[pygame.event.Event], dt):
        pass

    def draw(self, surf: pygame.Surface, offset):
        pass


# pre-defined recipes

# ingredients
ing1 = Ingredient('potato', 'images,')