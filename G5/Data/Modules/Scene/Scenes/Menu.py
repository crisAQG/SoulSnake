from G5.Data.Modules.Scene.Scene import Scene
import pygame

from G5.Data.Modules.Scene.Scenes import LorePreGame


class Menu(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.fuente = game.font
        self.titulo = self.fuente.render("SoulSnake", True, (255, 255, 255))
        self.jugar_txt = self.fuente.render("Presione [J] para jugar.", True, (255, 255, 255))
        self.Configuracion_txt = self.fuente.render("Presione [C] para ir a configuraciónes.", True, (255, 255, 255))
        self.Exit_txt = self.fuente.render("Presione [E] para salir.", True, (255, 255, 255))
        

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            from G5.Data.Modules.Scene.Scenes import Settings
            if event.key == pygame.K_j:
                self.game.set_scene(LorePreGame.LorePreGame(self.game))
            elif event.key == pygame.K_c:
                self.game.set_scene(Settings.Settings(self.game))
            elif event.key == pygame.K_e:
                self.game.running = False


    def update(self):
        pass

    def draw(self, screen):
        screen.fill((13, 130, 100))
        screen.blit(self.titulo, (0, 0))
        screen.blit(self.jugar_txt, (0, 32*18))
        screen.blit(self.Configuracion_txt, (0, 32*19))
        screen.blit(self.Exit_txt, (0, 32*20))
