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


class Pessoa(object):
    SENTIMENTO_RUIM_COR = (0, 0, 0)
    SENTIMENTO_NEUTRO_COR = (0, 0, 255)
    SENTIMENTO_BOM_COR = (0, 255, 0)

    x = 0
    y = 0
    color = (255, 255, 0)
    raio_influencia = 40
    sentimento = 0
    tempo_maximo = 2500
    tempo_de_vida = 0
    ativo = False
    peso = 10
    influenciador = False
    lista_influenciados = []

    def __init__(self, x=2, y=2, sentimento=0, raio_influencia=40, peso=10):
        self.x = x
        self.y = y
        self.sentimento = sentimento
        self.define_cor_pelo_sentimento()
        self.raio_influencia = raio_influencia
        self.peso = peso

    def draw(self, screen, draw_influencia):
        color = (0, 0, 0)
        if self.ativo:
            pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.peso+3, 0)
            color = (255, 0, 0)
        if draw_influencia:
            pygame.draw.circle(screen, color, (self.x, self.y), self.raio_influencia, 1)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.peso, 0)
        # for p in self.lista_influenciados:
        #     pygame.draw.line(screen, self.color, (self.x, self.y), (p.x, p.y))
            # pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), 2, 0)

    def update(self, difftime):
        if self.ativo:
            # if not self.influenciando:
            #     self.influenciando = True
            #     self.influencia_pessoas()
            self.tempo_de_vida += difftime

            if self.tempo_de_vida >= self.tempo_maximo:
                self.influencia_pessoas()
                self.ativo = False
                self.tempo_de_vida = 0
                self.define_cor_pelo_sentimento()

    def colide_circular(self, x1, y1, size1, x2, y2, size2):
         return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) <= size1 + size2
        # return (x1 - x2)**2 + (y1-y2)**2 < size1*size2

    def em_cima(self, outra_pessoa):
        return self.colide_circular(self.x, self.y, self.peso, outra_pessoa.x, outra_pessoa.y, outra_pessoa.peso)

    def colide(self, pessoas):
        for p in pessoas:
            if self.em_cima(p):
                return True
        return False

    def event_click(self, event):
        if self.colide_circular(self.x, self.y, self.peso, event.pos[0], event.pos[1], 5):
            self.ativo = True

    def define_cor_pelo_sentimento(self):
        if self.sentimento < 0:
            self.color = self.SENTIMENTO_RUIM_COR
        elif self.sentimento == 0:
            self.color = self.SENTIMENTO_NEUTRO_COR
        else:
            self.color = self.SENTIMENTO_BOM_COR

    def influencia_pessoas(self):
        for p in Game.pessoas:
            if p != self and self.consegue_influenciar(p) and not p.influenciador:
                self.influenciador = True
                self.influencia(p)
                self.lista_influenciados.append(p)
                p.ativo = True

    def consegue_influenciar(self, pessoa):
        return self.colide_circular(self.x, self.y, self.raio_influencia, pessoa.x, pessoa.y, pessoa.peso)

    def influencia(self, p):
        if self.sentimento > 0:
            if p.sentimento < 1:
                p.sentimento += 1
                p.define_cor_pelo_sentimento()
        elif self.sentimento < 0:
            if p.sentimento >= 0:
                p.sentimento -= 1
                p.define_cor_pelo_sentimento()


if __name__ == "__main__":
    g = Game(WIDTH, HEIGHT)
    g.main_loop()
