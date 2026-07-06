from G5.Data.Modules.Scene.Scene import Scene
from G5.Data.Modules.Scene.Scenes.Instruction import Instructions
import Config

import pygame

class LorePreGame(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.fuente = game.font
        self.titulo = self.fuente.render("Historia:", True, (255, 255, 255))
        self.Primer1 = self.fuente.render("En un universo distopico, existia un imperio el cual generaba cáos en su población,", True, (255, 255, 255))
        self.Primer2 = self.fuente.render("miles de muertos, protestas silenciadas, y un tirano que se alimentaba de los recursos nacionales.", True, (255, 255, 255))
        self.Segundo1 = self.fuente.render("Dentro de las rebeliones habia una guerrilla que resaltaba, tenia mas integrantes y la lideraba un obispo.", True, (255, 255, 255))
        self.Segundo2 = self.fuente.render("Esta guerrilla tenia un disipulo unico, era una serpiente que concedia milagros a quien se le acercase,", True, (255, 255, 255))
        self.Segundo3 = self.fuente.render("Tenian demasiado poder, una serpiente muy fiel a su lider, pero algo no encajaba.", True, (255, 255, 255))
        self.Tercero1 = self.fuente.render("El obispo conspiro contra la serpiente,", True, (255, 255, 255))
        self.Tercero2 = self.fuente.render("deseo tanto su milagro que en el arranque de locura accedio apeticiones del imperio para eliminarlo.", True, (255, 255, 255))
        self.Tercero3 = self.fuente.render("Lo embosco pero no logro asesinarlo. En cambio, le corto la cola.", True, (255, 255, 255))
        self.Tercero4 = self.fuente.render('"Este es el cáliz del milagro, podran beberlo en nombre de la sangre divína".', True, (255, 255, 255))
        self.Tercero5 = self.fuente.render('"Esta es el pan de cada día, sera nuestra fuerza para luchar contra el mal que nos invade".', True, (255, 255, 255))

        self.Cuarto = self.fuente.render("El obispo uso la carne y sangre de la serpiente para fortalecer a sus discipulos, traicionando a su fiel guerrillero.", True, (255, 255, 255))
        self.Final = self.fuente.render("Desde ese día, la serpiente juro venganza.", True, (255, 255, 255))

        self.game_txt = self.fuente.render("Presione [ENTER] para seguir.", True, (255, 255, 255))

        self.count = 1

        pygame.mixer.music.load("G5/Data/Sounds/lore.mp3")
        pygame.mixer.music.set_volume(Config.musica)
        pygame.mixer.music.play(-1)

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.count <= 5:
                self.count += 1
            else:
                self.game.set_scene(Instructions(self.game))

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((153, 136, 130))
        screen.blit(self.titulo, (0, 0))
        if self.count == 1:
            screen.blit(self.Primer1, (0, 32*2))
            screen.blit(self.Primer2, (0, 32*3))
        elif self.count == 2:
            screen.blit(self.Segundo1, (0, 32*2))
            screen.blit(self.Segundo2, (0, 32*3))
            screen.blit(self.Segundo3, (0, 32*4))
        elif self.count == 3:
            screen.blit(self.Tercero1, (0, 32*2))
            screen.blit(self.Tercero2, (0, 32*3))
            screen.blit(self.Tercero3, (0, 32*4))
            screen.blit(self.Tercero4, (0, 32*5))
            screen.blit(self.Tercero5, (0, 32*6))
        elif self.count == 4:
            screen.blit(self.Cuarto, (0, 32*2))
        elif self.count == 5:
            screen.blit(self.Final, (0, 32*2))


        screen.blit(self.game_txt, (0, 32*20))
    