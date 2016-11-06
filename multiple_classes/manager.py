from random import randint

import base
import constantes
from Pessoa import Pessoa
from base import Base_state
from pygame.locals import *


MAX_PESSOAS = 150
DRAW_INFLUENCIA = False


class GameManager(Base_state):

    def __init__(self):
        super().__init__()
        self.carrega_pessoas()

    def update(self, clock):
        for pessoa in constantes.pessoas:
            pessoa.update(clock.get_time())
        # print(clock.get_time())

    def draw(self, screen):
        for pessoa in constantes.pessoas:
            pessoa.draw(screen)

    def handle_input(self, event):
        if event.type == QUIT:
            self.done = True
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.done = True
            if event.key == K_F1:
                constantes.draw_influencia = True
            if event.key == K_F2:
                constantes.draw_influencia = False
            if event.key == K_F3:
                constantes.draw_ligacao = True
            if event.key == K_F4:
                constantes.draw_ligacao = False
            if event.key == K_F5:
                self.restart_game()


        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            for p in constantes.pessoas:
                p.event_click(event)

    def carrega_pessoas(self, total_pessoas=MAX_PESSOAS):
        constantes.pessoas.clear()
        for i in range(total_pessoas):
            rand_x = randint(20, base.WIDTH - 20)
            rand_y = randint(20, base.HEIGHT - 20)
            rand_sentimento = randint(-1, 1)
            rand_peso = randint(10, 25)
            influencia = rand_peso * 3

            pessoa = Pessoa(rand_x, rand_y, rand_sentimento, influencia, rand_peso)

            while pessoa.colide(constantes.pessoas):
                rand_x = randint(30, base.WIDTH - 30)
                rand_y = randint(30, base.HEIGHT - 30)
                pessoa.x = rand_x
                pessoa.y = rand_y

            constantes.pessoas.append(pessoa)

    def restart_game(self):
        self.carrega_pessoas()

if __name__ == "__main__":
    g = GameManager()
    g.main_loop()