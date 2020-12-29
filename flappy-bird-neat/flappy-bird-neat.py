from constant import WIN_WIDTH, WIN_HEIGHT
from element import Bird, Tube
from color import BLACK, WHITE, RED

from random import randint
import pygame as pg
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
    tube_spawn_time = 1000
    tube_last_spawn_time = pg.time.get_ticks()

    score = 0

    run = True
    while run:
        window.fill(BLACK)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_SPACE:
            #         bird.fly()

        time_now = pg.time.get_ticks()
        if time_now - tube_last_spawn_time > tube_spawn_time:
            tube_last_spawn_time = time_now
            r_num = randint(0, 360)
            tube_list.append(Tube(60 + r_num))
            if tube_list[0].x < -20:
                score += 1
                del(tube_list[0])

        # print('Tube count:', tube_list)
        # pg.time.delay(1000)

        gens_text = font.render(f'Generation: {generation}', True, WHITE)
        window.blit(gens_text, (20, 20))

        for index, bird in enumerate(birds):
            tube_count = len(tube_list)
            if tube_count == 0:
                output = nets[index].activate([-1, -1, -1, -1])
            elif tube_count >= 1:
                tube = tube_list[0]
                d1 = get_distance([bird.x, bird.y], [tube.x, tube.y1])
                d2 = get_distance([bird.x, bird.y], [tube.x, tube.y2])
                output = nets[index].activate([d1, d2, tube.y1, tube.y2])

            i = output[0]
            if i > 0:
                bird.fly()

        for i, tube in enumerate(tube_list):
            tube.update(window)

            for index, bird in enumerate(birds):
                if tube.top_rect.colliderect(bird.rect):
                    bird.alive = False
                if tube.bottom_rect.colliderect(bird.rect):
                    bird.alive = False

        remain_birds = 0
        for i, bird in enumerate(birds):
            if bird.alive:
                bird.update(window)
                genomes[i][1].fitness = score
                remain_birds += 1

        remain_birds_text = font.render(
            f'Remain birds: {remain_birds}', True, WHITE)
        window.blit(remain_birds_text, (20, 40))

        if remain_birds == 0:
            run = False

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
