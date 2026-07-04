from G5.Data.Modules.Scene.Scene import Scene

import pygame


class Outro(Scene):
    def __init__(self, game, state: int):
        """
        :param game: Pestaña pygame (alojada en clase Window)
        :param state: Si estado = 1: win; Si estado = 0: lose;
        """
        super().__init__(game)
        self.game = game
        self.fuente = game.font
        self.titulo = None 

        if state == 1:
            self.titulo = self.fuente.render("Ganaste. La historia cerro una puerta dañada.", True, (255, 255, 255))
        else:
            self.titulo = self.fuente.render("Haz muerto en el intento, puedes volver a hacerlo.", True, (255, 255, 255))

        self.volver_m = self.fuente.render("Pulsa [ESCAPE] para volver al menu.", True, (255, 255, 255))
        self.volver_j = self.fuente.render("Pulsa[J] para intentarlo de nuevo.", True, (255, 255, 255))

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from G5.Data.Modules.Scene.Scenes.Menu import Menu
                self.game.set_scene(Menu(self.game))
            elif event.key == pygame.K_j:
                from G5.Data.Modules.Scene.Scenes.Game import Game
                self.game.set_scene(Game(self.game))

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((153, 136, 130))
        screen.blit(self.titulo, (0, 0))
        screen.blit(self.volver_m, (0, 32*19))
        screen.blit(self.volver_j, (0, 32*20))
    