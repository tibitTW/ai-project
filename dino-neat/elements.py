from random import randint
import pygame as pg
from color import RED

random_colors = [
    (255, 255, 255),
    (255, 255, 100),
    (255, 100, 255),
    (255, 100, 100),
    (100, 255, 255),
    (100, 255, 100),
    (100, 100, 255),
]

GRAVITY = 1


class Dino:
    def __init__(self):
        self.x = 80
        self.y = 320
        self.w = 40
        self.h = 40
        self.alive = True
        self.y_speed = 0
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
        self.color = random_colors[randint(0, 6)]

    def __str__(self):
        return f'Dino at [{self.x}, {self.y}]'

    def jump(self):
        if self.y == 320:
            self.y_speed = -15

    def update(self, surface: pg.Surface):
        self.y += self.y_speed
        if self.y < 320:
            self.y_speed += GRAVITY
        if self.y == 320:
            self.y_speed = 0
        if self.y > 320:
            self.y = 0
            self.y_speed = 0
        self.rect.update(self.x, self.y, self.w, self.h)

        pg.draw.rect(surface, self.color, self.rect)


class Cactus:
    def __init__(self, x):
        self.x = x
        self.y = 320
        self.w = 40
        self.h = 40
        self.color = RED
        self.x_speed = -5
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)

    def update(self, surface: pg.Surface):
        self.x += self.x_speed
        self.rect.update(self.x, self.y, self.w, self.h)
        pg.draw.rect(surface, self.color, self.rect)
