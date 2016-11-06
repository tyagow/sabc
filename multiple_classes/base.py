import pygame
from pygame.locals import *

FPS = 60
WIDTH = 800
HEIGHT = 600

class Base_state(object):
    done = False
    clock = ""
    manager = None

    def __init__(self, width=WIDTH, height=HEIGHT):
        pygame.init()
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.clock.tick()
        self.screen.fill(Color("white"))

    def main_loop(self):
        while not self.done:
            # events
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT: self.done = True
                elif e.type == KEYDOWN:
                    if e.key == K_ESCAPE: self.done = True
                self.handle_input(e)

            # update
            self.clock.tick(FPS)
            self.update(self.clock)

            # draw
            self.screen.fill((255,255,255))
            self.draw(self.screen)
            pygame.display.update()

    def handle_inputs(self, events):
        pass

    def update(self, clock):
        pass

    def draw(self, screen):
        pass


