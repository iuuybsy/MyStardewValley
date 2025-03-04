import pygame
from settings import *


class Overlay:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player

        overlay_path = 'graphics/overlay/'
        self.tool_surf = {tool: pygame.image.load(f'{overlay_path}{tool}.png') for tool in player.tools}
        self.seed_surf = {seed: pygame.image.load(f'{overlay_path}{seed}.png') for seed in player.seeds}

    def display(self):

        tool_surf = self.tool_surf[self.player.selected_tool]
        tool_rect = tool_surf.get_rect(midbottom=OVERLAY_POSITIONS['tool'])
        self.display_surface.blit(tool_surf, tool_rect)

        seed_surf = self.seed_surf[self.player.selected_seed]
        seed_rect = seed_surf.get_rect(midbottom=OVERLAY_POSITIONS['seed'])
        self.display_surface.blit(seed_surf, seed_rect)
