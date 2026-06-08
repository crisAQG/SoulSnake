from Data.Modules.Scene.Scene import Scene
from Data.Modules.Type.Blocks import Tile

import pygame


class Test(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.quad = Tile(0, 32, 32, 32, (20, 180, 84), 0)
        self.hex = Tile(32, 32, 32, 32, (230, 40, 70), 1)
        self.triad = Tile(64, 32, 32, 32, (100, 134, 80), 2)
        self.diam = Tile(96, 32, 32, 32, (200, 47, 153), 3)
        self.circ = Tile(128, 32, 32, 32, (244, 40, 40), 4)

    def events(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        self.quad.draw(screen)
        self.hex.draw(screen)
        self.triad.draw(screen)
        self.diam.draw(screen)
        self.circ.draw(screen)
