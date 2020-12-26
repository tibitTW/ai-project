from elements import Dino, Cactus
from color import *

from random import randint, random
import pygame as pg

import neat

pg.init()
WIN_WIDTH, WIN_HEIGHT = 640, 480
window = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

pg.font.init()
font = pg.font.SysFont(None, 24)

ground = pg.Surface((640, 120))
ground.fill((128, 128, 128))

generation = 0


def run_game(genomes, config):

    # Init NEAT
    nets = []
    dinos = []

    for id, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

        # Init dinos
        dinos.append(Dino())

    # dino = Dino()
    cactus_list = [Cactus(600)]
    cactus_spawn_time = 900
    cactus_last_spawn_time = pg.time.get_ticks()

    global generation
    generation += 1

    t0 = pg.time.get_ticks()
    run = True
    while run:

        window.fill((0, 0, 0))
        window.blit(ground, (0, 360))

        score = (pg.time.get_ticks() - t0) // 20
        score_text = font.render('Score: '+str(score), True, WHITE)
        window.blit(score_text, (20, 20))

        gens_text = font.render('Generation: '+str(generation), True, WHITE)
        window.blit(gens_text, (20, 40))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_SPACE:
            #         dino.jump()

        for index, dino in enumerate(dinos):
            cactus_count = len(cactus_list)
            if cactus_count == 0:
                output = nets[index].activate([-1, -1])
            elif cactus_count == 1:
                output = nets[index].activate(
                    [cactus_list[0].x, -1])
            elif cactus_count >= 2:
                output = nets[index].activate(
                    [cactus_list[0].x, cactus_list[1].x])

            i = output.index(max(output))
            if i == 1:
                dino.jump()
            else:
                pass

        remain_dinos = 0
        for i, cactus in enumerate(cactus_list):

            cactus.update(window)
            if cactus.x < 20:
                del(cactus_list[i])

            for index, dino in enumerate(dinos):

                if cactus.rect.colliderect(dino.rect):
                    dino.alive = False

        for i, dino in enumerate(dinos):
            if dino.alive:
                remain_dinos += 1
                dino.update(window)
                genomes[i][1].fitness += 1

        if remain_dinos == 0:
            run = False

        remains_text = font.render(
            'Remain dinos:'+str(remain_dinos), True, WHITE)
        window.blit(remains_text, (20, 60))

        if (pg.time.get_ticks() - cactus_last_spawn_time) > cactus_spawn_time:
            cactus_list.append(Cactus(640))
            cactus_last_spawn_time = pg.time.get_ticks()
            cactus_spawn_time = randint(400, 900)

        pg.display.update()
        pg.time.delay(10)


if __name__ == "__main__":
    config_path = './config-feedforward.txt'
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    p.run(run_game, 100)

pg.quit()
