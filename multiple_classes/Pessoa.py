import pygame
from math import sqrt

import constantes


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

    def __init__(self, x=2, y=2, sentimento=0, raio_influencia=40, peso=10):
        self.draw_influencia = False
        self.x = x
        self.y = y
        self.sentimento = sentimento
        self.define_cor_pelo_sentimento()
        self.raio_influencia = raio_influencia
        self.peso = peso
        self.lista_influenciados = []

    def draw(self, screen):
        color = (0, 0, 0)
        if self.ativo:
            pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.peso+3, 0)
            color = (255, 0, 0)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.peso, 0)

        if constantes.draw_influencia:
            pygame.draw.circle(screen, color, (self.x, self.y), self.raio_influencia, 1)
        if constantes.draw_ligacao:
            for p in self.lista_influenciados:
                pygame.draw.line(screen, self.color, (self.x, self.y), (p.x, p.y))
                pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), 2, 0)

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
        for p in constantes.pessoas:
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
