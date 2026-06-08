from G5.Data.Modules.Scene.Scene import Scene
from G5.Data.Modules.Type.Entities import Player
from G5.Data.Modules.Services.MapGen import MapGen

import pygame


class Game(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.fuente = game.font
        self.volver_txt = self.fuente.render("Presione [ESCAPE] para volver al menu.", True, (255, 255, 255))

        self.map = MapGen()

        self.map
        self.tab = self.map.map
        self.plr = Player((0, 0), (32, 32), (10, 30, 170), 0, 0, 0)

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from G5.Data.Modules.Scene.Scenes.Menu import Menu
                self.game.set_scene(Menu(self.game))

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((139, 153, 160))
        self.map.draw(screen, self.plr)
        screen.blit(self.volver_txt, (0, 32*20))
