from random import randint

from base import Base_state
from constantes import *
from Pessoa import Pessoa
from pygame.locals import *


class GameManager(Base_state):

    def __init__(self):
        super().__init__()
        self.carrega_pessoas()

    def update(self, clock):
        for pessoa in pessoas:
            pessoa.update(clock.get_time())
        # print(clock.get_time())

    def draw(self, screen):
        for pessoa in pessoas:
            pessoa.draw(screen)

    def handle_input(self, event):
        if event.type == QUIT:
            self.done = True
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.done = True
            if event.key == K_F1:
                draw_influencia = True
            if event.key == K_F2:
                draw_influencia = False
            if event.key == K_F3:
                draw_ligacao = True
            if event.key == K_F4:
                draw_ligacao = False
            if event.key == K_F5:
                self.restart_game()
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            for p in pessoas:
                p.event_click(event)

    def carrega_pessoas(self, total_pessoas=MAX_PESSOAS):
        pessoas.clear()
        for i in range(total_pessoas):
            rand_x = randint(20, WIDTH - 20)
            rand_y = randint(20, HEIGHT - 20)
            rand_sentimento = randint(-1, 1)
            rand_peso = randint(10, 25)
            influencia = rand_peso * 3

            pessoa = Pessoa(rand_x, rand_y, rand_sentimento, influencia, rand_peso)

            while pessoa.colide(pessoas):
                rand_x = randint(30, WIDTH - 30)
                rand_y = randint(30, HEIGHT - 30)
                pessoa.x = rand_x
                pessoa.y = rand_y

            pessoas.append(pessoa)

    def restart_game(self):
        self.carrega_pessoas()

if __name__ == "__main__":
    g = GameManager()
    g.main_loop()