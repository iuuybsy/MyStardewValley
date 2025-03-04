import pygame

from settings import *

from player import Player
from overlay import Overlay


class Level:

    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.player = Player((640, 360), self.sprites)
        self.overlay = Overlay(self.player)

    def setup(self):
        pass

    def run(self, dt):
        self.display_surface.fill('black')
        self.sprites.draw(self.display_surface)
        self.sprites.update(dt)
        self.overlay.display()
