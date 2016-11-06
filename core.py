from random import randint
from math import sqrt
import pygame
from pygame.locals import *

WIDTH = 800
HEIGHT = 600
MAX_PESSOAS = 150


class Game(object):
    done = False
    pessoas = []
    draw_influencia = False
    clock = ""

    def __init__(self, width=800, height=600):
        pygame.init()
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.clock.tick()

        # start with empty screen, since we modify it every mouseclick
        self.screen.fill(Color("white"))
        self.carrega_pessoas()

    def main_loop(self):
        while not self.done:
            # events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT: self.done = True
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE: self.done = True
                    if event.key == K_F1: self.draw_influencia = False
                    if event.key == K_F2: self.draw_influencia = True
                    if event.key == K_F3: self.restart_game()
                elif event.type == MOUSEMOTION:
                    pass
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    for p in self.pessoas:
                        p.event_click(event)
                    # self.screen.set_at(event.pos, Color("white"))

            # update
            self.clock.tick(60)

            # draw
            self.screen.fill((255,255,255))
            for pessoa in self.pessoas:
                pessoa.update(self.clock.get_time())
                pessoa.draw(self.screen, self.draw_influencia)

            pygame.display.update()

    def carrega_pessoas(self, total_pessoas=MAX_PESSOAS):
        for i in range(total_pessoas):
            rand_x = randint(20, WIDTH - 20)
            rand_y = randint(20, HEIGHT - 20)
            rand_sentimento = randint(-1, 1)
            rand_peso = randint(10, 25)
            influencia = rand_peso * 3

            pessoa = Pessoa(rand_x, rand_y, rand_sentimento, influencia, rand_peso)

            while pessoa.colide(self.pessoas):
                rand_x = randint(30, WIDTH-30)
                rand_y = randint(30, HEIGHT-30)
                pessoa.x = rand_x
                pessoa.y = rand_y

            self.pessoas.append(pessoa)

    def restart_game(self):
        self.pessoas.clear()
        self.carrega_pessoas()



if __name__ == "__main__":
    g = Game(WIDTH, HEIGHT)
    g.main_loop()
