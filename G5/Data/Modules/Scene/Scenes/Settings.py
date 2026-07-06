from G5.Data.Modules.Scene.Scene import Scene
import Config

import pygame


class Settings(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.fuente = pygame.font.Font(None, 32)
        self.font_musica = pygame.font.Font(None, 32)
        self.font_sfx = pygame.font.Font(None, 32)
        self.titulo = self.fuente.render("Configuraciones:", True, (255, 255, 255))
        self.volver_txt = self.fuente.render("Presione [M] para volver.", True, (255, 255, 255))

        self.config_actual = 1

        pygame.mixer.music.load("G5/Data/Sounds/lore.mp3")
        pygame.mixer.music.play(-1)

    def events(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_m:
                from G5.Data.Modules.Scene.Scenes.Menu import Menu
                pygame.mixer.music.fadeout(1200)
                self.game.set_scene(Menu(self.game))
            if event.key == pygame.K_DOWN:
                self.config_actual -= 1
                self.config_actual = max(0, self.config_actual)
                print(self.config_actual)
            if event.key == pygame.K_UP:
                self.config_actual += 1
                self.config_actual = min(1, self.config_actual)
                print(self.config_actual)
            if event.key == pygame.K_LEFT:
                if self.config_actual == 1: 
                    Config.musica -= 0.1
                    Config.musica = max(0.0, Config.musica)
                else:
                    Config.sfx -= 0.1 
                    Config.sfx = max(0.0, Config.sfx)
                print(f"Musica: %{Config.musica}, SFX: %{Config.sfx}")
            if event.key == pygame.K_RIGHT:
                if self.config_actual == 1: 
                    Config.musica += 0.1
                    Config.musica = min(1.0, Config.musica)
                else:
                    Config.sfx += 0.1 
                    Config.sfx = min(1.0, Config.sfx)
                print(f"Musica: %{Config.musica}, SFX: %{Config.sfx}")
            Config.musica = round(Config.musica, 2)
            Config.sfx = round(Config.sfx, 2)
            print(Config.musica)

    def update(self):
        pygame.mixer.music.set_volume(Config.musica)
        self.font_musica.set_underline(self.config_actual == 1)
        self.musica = self.font_musica.render(
            f"Volumen de musica: % {Config.musica * 100:.2f}",
            True,
            (255, 255, 255)
        )

        self.font_sfx.set_underline(self.config_actual == 0)
        self.sfx = self.font_sfx.render(
            f"Volumen de efectos: % {Config.sfx * 100:.2f}",
            True,
            (255, 255, 255)
        )
    def draw(self, screen):
        screen.blit(pygame.image.load("G5/Data/Sprites/config.jpeg").convert_alpha(), (0, 0))
        screen.blit(self.titulo, (0, 0))
        screen.blit(self.musica, (0, 32*2))
        screen.blit(self.sfx, (0, 32*3))
        screen.blit(self.volver_txt, (0, 32*20))
    