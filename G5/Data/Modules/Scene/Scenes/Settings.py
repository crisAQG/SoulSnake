from G5.Data.Modules.Scene.Scene import Scene

import pygame


class Settings(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.fuente = game.font
        self.titulo = self.fuente.render("Configuraciones:", True, (255, 255, 255))
        self.volver_txt = self.fuente.render("Presione [M] para volver.", True, (255, 255, 255))

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                from G5.Data.Modules.Scene.Scenes.Menu import Menu
                self.game.set_scene(Menu(self.game))

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((120, 120, 120))
        screen.blit(self.titulo, (0, 0))
        screen.blit(self.volver_txt, (0, 32*20))
    