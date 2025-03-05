import pygame

from settings import *

from player import Player
from overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree
from pytmx.util_pygame import load_pygame
from support import *


class Level:

    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.all_sprites = CameraGroup()
        self.setup()
        self.player = Player((640, 360), self.sprites)
        Generic(pos=(0, 0),
                surf=pygame.image.load('graphics/world/ground.png').convert_alpha(),
                groups=self.all_sprites,
                z=LAYERS['ground'])
        self.all_sprites.add(self.player)
        self.overlay = Overlay(self.player)

    def setup(self):
        tmx_data = load_pygame('data/map.tmx')

        for layer in ['HouseFloor', 'HouseFurnitureBottom', 'HouseWalls', 'HouseFurnitureTop']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic(pos=(x * TILESIZE, y * TILESIZE),
                        surf=surf,
                        groups=self.all_sprites,
                        z=LAYERS['house bottom'])

        for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
            Generic(pos=(x * TILESIZE, y * TILESIZE),
                    surf=surf,
                    groups=self.all_sprites,
                    z=LAYERS['house bottom'])

        water_frames = import_folder('graphics/water')
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            Water(pos=(x * TILESIZE, y * TILESIZE),
                  frames=water_frames,
                  groups=self.all_sprites)

        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree(pos=(obj.x * TILESIZE, obj.y * TILESIZE),
                 surf=obj.image,
                 groups=self.all_sprites,
                 name=obj.name)

        for obj in tmx_data.get_layer_by_name('Decoration'):
            WildFlower(pos=(obj.x * TILESIZE, obj.y * TILESIZE),
                  surf=obj.image,
                  groups=self.all_sprites)

    def run(self, dt):
        self.display_surface.fill('black')
        # self.sprites.draw(self.display_surface)
        self.all_sprites.customize_draw(self.player)
        self.sprites.update(dt)
        self.overlay.display()


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def customize_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)
