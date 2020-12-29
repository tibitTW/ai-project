from constant import WIN_HEIGHT, WIN_WIDTH, GRAVITY
from color import GREEN
import pygame as pg
from random import randint

random_colors = [
    (255, 255, 255),
    (255, 255, 100),
    (255, 100, 255),
    (255, 100, 100),
    (100, 255, 255),
    (100, 255, 100),
    (100, 100, 255),
]


class Bird:
    def __init__(self):
        self.w = 40
        self.h = 40
        self.x = 40
        self.y = (WIN_HEIGHT - self.h) / 2
        self.color = random_colors[randint(0, 6)]
        self.alive = True
        self.y_speed = 0
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)

    def __str__(self):
        return f'x: {self.x}, y:{self.y}, y speed: {self.y_speed}'

    def fly(self):
        if self.y > 0:
            self.y_speed = -6

    def update(self, surface):
        self.y += self.y_speed
        if self.y < 0:
            self.y = 0
        if self.y >= WIN_HEIGHT - self.h:
            self.y = WIN_HEIGHT - self.h
            self.y_speed = 0
        else:
            self.y_speed += GRAVITY

        self.rect.update(self.x, self.y, self.w, self.h)
        pg.draw.rect(surface, self.color, self.rect)


class Tube:
    def __init__(self):
        self.x = WIN_WIDTH
        y = randint(200, 240)
        self.y1 = y - 60
        self.y2 = y + 60
        self.w = 60
        self.color = GREEN
        self.x_speed = -5
        self.top_rect = pg.Rect(self.x, 0, self.w, self.y1)
        self.bottom_rect = pg.Rect(self.x, self.y2, self.w, WIN_HEIGHT)

    def update(self, surface: pg.Surface):
        self.x += self.x_speed
        self.top_rect.update(self.x, 0, self.w, self.y1)
        self.bottom_rect.update(self.x, self.y2, self.w, WIN_HEIGHT)

        pg.draw.rect(surface, self.color, self.top_rect)
        pg.draw.rect(surface, self.color, self.bottom_rect)
