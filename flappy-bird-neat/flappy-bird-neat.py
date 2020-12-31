from constant import WIN_WIDTH, WIN_HEIGHT
from element import Bird, Tube
from color import WHITE

import pygame as pg
import os
import neat


pg.init()
window = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

pg.font.init()
font = pg.font.SysFont(None, 24)

generation = 0


def get_distance(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] + b[1]) ** 2) ** 0.5


def run_game(genomes, config):

    global generation
    generation += 1

    nets = []
    birds = []

    for id, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

        birds.append(Bird())

    tube_list = []
    tube_spawn_time = 150
    tube_last_spawn_time = 0

    t0 = pg.time.get_ticks()

    run = True
    while run:
        window.fill((0, 183, 235))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        ################################
        #         produce tube         #
        ################################
        tube_last_spawn_time += 1
        if tube_last_spawn_time > tube_spawn_time:
            tube_last_spawn_time = 0
            tube_list.append(Tube())
            if tube_list[0].x < -20:
                del(tube_list[0])
        ################################
        ################################
        ################################

        gens_text = font.render(f'Generation: {generation}', True, WHITE)
        window.blit(gens_text, (20, 20))

        for i, bird in enumerate(birds):
            tube_count = len(tube_list)
            if tube_count == 0:
                output = nets[i].activate(
                    [bird.y, bird.y_speed, -1, -1, -1, -1])
            elif tube_count >= 1:
                tube = tube_list[0]
                d1 = get_distance([bird.x, bird.y], [tube.x, tube.y1])
                d2 = get_distance([bird.x, bird.y], [tube.x, tube.y2])

                output = nets[i].activate(
                    [bird.y, bird.y_speed, d1, d2, tube.y1, tube.y2])

            i = output[0]
            if i > 0:
                bird.fly()

        for tube in tube_list:
            tube.update(window)

            for bird in birds:
                if tube.top_rect.colliderect(bird.rect):
                    bird.alive = False
                if tube.bottom_rect.colliderect(bird.rect):
                    bird.alive = False

        ###############################
        score = (pg.time.get_ticks() - t0) / 20
        remain_birds = 0
        for i, bird in enumerate(birds):
            if bird.alive:
                bird.update(window)
                genomes[i][1].fitness = score
                remain_birds += 1

        if score > 2000:
            run = False

        remain_birds_text = font.render(
            f'Remain birds: {remain_birds}', True, WHITE)
        window.blit(remain_birds_text, (20, 40))

        if remain_birds == 0:
            run = False
        ###############################

        pg.display.update()
        # pg.time.delay(8)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    p.run(run_game, 150)
    pg.quit()
