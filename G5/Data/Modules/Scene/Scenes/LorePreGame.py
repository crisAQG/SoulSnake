from G5.Data.Modules.Scene.Scene import Scene
from G5.Data.Modules.Scene.Scenes.Instruction import Instructions

import pygame

class LorePreGame(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.fuente = game.font
        self.titulo = self.fuente.render("Historia:", True, (255, 255, 255))
        self.game_txt = self.fuente.render("Presione [ENTER] para seguir.", True, (255, 255, 255))

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.game.set_scene(Instructions(self.game))

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((153, 136, 130))
        screen.blit(self.titulo, (0, 0))
        screen.blit(self.game_txt, (0, 32*20))
    