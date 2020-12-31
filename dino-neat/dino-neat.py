from elements import Dino, Cactus
from color import WHITE

from random import randint
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

    cactus_list = [Cactus(600)]
    cactus_spawn_time = 900
    cactus_last_spawn_time = pg.time.get_ticks()

    global generation
    generation += 1

    score = 0

    t0 = pg.time.get_ticks()
    run = True
    while run:

        # make static background
        window.fill((0, 0, 0))
        window.blit(ground, (0, 360))

        # print score
        score = (pg.time.get_ticks() - t0) // 20
        score_text = font.render('Score: '+str(score), True, WHITE)
        window.blit(score_text, (20, 20))

        # print generation number
        gens_text = font.render('Generation: '+str(generation), True, WHITE)
        window.blit(gens_text, (20, 40))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        ######################################
        #      algorithms make decisions     #
        ######################################

        for i, dino in enumerate(dinos):
            cactus_count = len(cactus_list)
            if cactus_count == 0:
                output = nets[i].activate([-1, -1])
            elif cactus_count == 1:
                output = nets[i].activate(
                    [cactus_list[0].x - dino.x, -1])
            elif cactus_count >= 2:
                output = nets[i].activate(
                    [cactus_list[0].x - dino.x,
                     cactus_list[1].x - dino.x])

            i = output[0]
            if i > 0:
                dino.jump()

        ######################################

        #########################################
        # update cactus, check if dino is alive #
        #########################################
        for i, cactus in enumerate(cactus_list):
            cactus.update(window)
            if cactus.x < 20:
                del(cactus_list[i])
                score += 1

            for dino in dinos:
                if cactus.rect.colliderect(dino.rect):
                    dino.alive = False
        #########################################

        #######################################
        #       check remain dino count       #
        #######################################
        remain_dinos = 0
        for index, dino in enumerate(dinos):
            if dino.alive:
                remain_dinos += 1
                dino.update(window)

                genomes[index][1].fitness = score
        if remain_dinos == 0:
            run = False
        #######################################

        if score > 2000:
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
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    p.run(run_game, 200)

pg.quit()
