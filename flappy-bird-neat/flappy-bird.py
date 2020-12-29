from constant import WIN_WIDTH, WIN_HEIGHT
from element import Bird, Tube
from color import BLACK, WHITE, RED, GREEN
import pygame as pg
# import random

pg.init()
window = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

pg.font.init()
font = pg.font.SysFont(None, 24)


def run_game():

    bird = Bird()
    tube_list = []
    tube_spawn_time = 1000
    tube_last_spawn_time = pg.time.get_ticks()

    score = 0
    best_score = 0

    run = True
    while run:
        window.fill((0, 183, 235))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    bird.fly()

        colli = False
        for tube in tube_list:
            if tube.top_rect.colliderect(bird.rect):
                colli = True
                best_score = max(score, best_score)
                score = 0
            if tube.bottom_rect.colliderect(bird.rect):
                colli = True
                best_score = max(score, best_score)
                score = 0

            if colli:
                tube.color = RED
            else:
                tube.color = GREEN

            tube.update(window)

        time_now = pg.time.get_ticks()
        if time_now - tube_last_spawn_time > tube_spawn_time:
            tube_last_spawn_time = time_now
            tube_list.append(Tube())
            if tube_list[0].x < -20:
                score += 1
                del(tube_list[0])

        score_text = font.render(
            f'Score:{score} Best score:{best_score}', True, WHITE)
        window.blit(score_text, (20, 20))

        bird.update(window)

        pg.display.update()
        pg.time.delay(10)


if __name__ == "__main__":
    run_game()
    pg.quit()
