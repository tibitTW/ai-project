from elements import Dino, Cactus
from color import *

from random import randint, random
import pygame as pg

pg.init()
WIN_WIDTH, WIN_HEIGHT = 640, 480
window = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

pg.font.init()
font = pg.font.SysFont(None, 24)

ground = pg.Surface((640, 120))
ground.fill((128, 128, 128))


def run_game():

    dino = Dino()
    cactus_list = []
    cactus_spawn_time = 1200
    cactus_last_spawn_time = pg.time.get_ticks()

    t0 = pg.time.get_ticks()
    run = True
    while run:
        window.fill((0, 0, 0))
        window.blit(ground, (0, 360))

        score = (pg.time.get_ticks() - t0) // 20
        score_text = font.render('Score: '+str(score), True, WHITE)
        window.blit(score_text, (20, 20))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    dino.jump()

        if (pg.time.get_ticks() - cactus_last_spawn_time) > cactus_spawn_time:
            cactus_list.append(Cactus(640))
            cactus_last_spawn_time = pg.time.get_ticks()
            cactus_spawn_time = randint(500, 2000)

        dino.update(window)

        for i, cactus in enumerate(cactus_list):
            cactus.update(window)
            if cactus.x < -50:
                del(cactus_list[i])

            if cactus.rect.colliderect(dino.rect):
                cactus.color = RED
            else:
                cactus.color = GREEN

        pg.display.update()
        pg.time.delay(10)


run_game()
pg.quit()
