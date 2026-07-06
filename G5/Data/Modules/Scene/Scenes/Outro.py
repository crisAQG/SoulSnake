from G5.Data.Modules.Scene.Scene import Scene
import Config

import pygame


class Outro(Scene):
    def __init__(self, game, state: int, copas: int = 0, enemigos: int = 0, puntaje: int = 0):
        """
        :param state: 1 = ganaste, 0 = perdiste
        :param copas: copas totales consumidas en la partida
        :param enemigos: enemigos totales eliminados en la partida
        :param puntaje: puntaje final (copas*10 + enemigos*25, ver Game.py)
        """
        super().__init__(game)
        self.game = game
        self.fuente = game.font

        if state == 1:
            self.titulo = self.fuente.render("Ganaste, ¿pero habrá valido totalmente la pena?", True, (255, 255, 255))
            pygame.mixer.music.load("G5/Data/Sounds/outro-win.mp3")
            pygame.mixer.music.set_volume(Config.musica)
            pygame.mixer.music.play()
        else:
            self.titulo = self.fuente.render("Haz muerto en el intento, puedes volver a hacerlo.", True, (255, 255, 255))
            pygame.mixer.music.load("G5/Data/Sounds/outro-lose.mp3")
            pygame.mixer.music.set_volume(Config.musica)
            pygame.mixer.music.play(-1)

        self.stats_txt = self.fuente.render(
            f"Copas: {copas}   Enemigos eliminados: {enemigos}   Puntaje: {puntaje}",
            True, (255, 215, 0)
        )

        self.volver_m = self.fuente.render("Pulsa [ESCAPE] para volver al menu.", True, (255, 255, 255))
        self.volver_j = self.fuente.render("Pulsa[J] para intentarlo de nuevo.", True, (255, 255, 255))

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from G5.Data.Modules.Scene.Scenes.Menu import Menu
                pygame.mixer.music.fadeout(1000)
                self.game.set_scene(Menu(self.game))
            elif event.key == pygame.K_j:
                from G5.Data.Modules.Scene.Scenes.Game import Game
                pygame.mixer.music.fadeout(1000)
                self.game.set_scene(Game(self.game))

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((153, 136, 130))
        screen.blit(self.titulo, (0, 0))
        screen.blit(self.stats_txt, (0, 32 * 2))
        screen.blit(self.volver_m, (0, 32 * 19))
        screen.blit(self.volver_j, (0, 32 * 20))