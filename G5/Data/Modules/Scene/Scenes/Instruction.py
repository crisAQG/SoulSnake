from G5.Data.Modules.Scene.Scene import Scene
from G5.Data.Modules.Scene.Scenes.Game import Game

import pygame

class Instructions(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.fuente = game.font
        self.titulo = self.fuente.render("Conjunto de instrucciones:", True, (255, 255, 255))
        self.mov = self.fuente.render("- Teclas para movimiento: WASD.", True, (255, 255, 255))
        self.copas = self.fuente.render("- Apareceran copas aleatoreamente, al consumirlas aumentaras tu cola.", True, (255, 255, 255))
        self.enemigos = self.fuente.render("- Apareceran enemigos los cuales podran atacarte, no dejes que te maten.", True, (255, 255, 255))
        self.ataque1 = self.fuente.render("- Puedes atacar a un enemigo manteniendo pulsado [SHIFT] y te restara un pedazo de cola.", True, (255, 255, 255))
        self.ataque2 = self.fuente.render("¡dejara de atacar despues de 3 segundos!", True, (255, 255, 255))
        self.jefe1 = self.fuente.render("- Al terminar la ronda 6 aparecera el jefe final, tendra dos ataques y no te acerques, te matara.", True, (255, 255, 255))
        self.jefe2 = self.fuente.render("- El jefe atacara con bolas de fuego, formando un *, perderas una cola si te quemas.", True, (255, 255, 255))
        self.jefe3 = self.fuente.render("- Despues de terminar con 3 ataques rapido hara un ataque cargado.", True, (255, 255, 255))
        self.jefe4 = self.fuente.render("- Se mostraran cruces en el suelo antes del ataque cargado, si te toca estas muerto.", True, (255, 255, 255))
        self.jefe5 = self.fuente.render("- El jefe posee 20 puntos de vida, podras quitarle un punto con un cuchillo.", True, (255, 255, 255))
        self.cuchillos = self.fuente.render("- Apareceran cuchillos aleatoreamente, al consumirlos podras atacar al jefe.", True, (255, 255, 255))

        self.ronda = self.fuente.render("Rondas:", True, (255, 255, 255))
        self.ronda1 = self.fuente.render("1: Mata 2 enemigos y consume 4 copas.", True, (255, 255, 255))
        self.ronda2 = self.fuente.render("2: Mata 3 enemigos y consume 5 copas.", True, (255, 255, 255))
        self.ronda3 = self.fuente.render("3: Mata 4 enemigos y consume 7 copas.", True, (255, 255, 255))
        self.ronda4 = self.fuente.render("4: Mata 3 enemigos y consume 8 copas.", True, (255, 255, 255))
        self.ronda5 = self.fuente.render("5: Mata 5 enemigos y consume 9 copas.", True, (255, 255, 255))
        self.ronda6 = self.fuente.render("5: Mata al jefe.", True, (255, 255, 255))

        self.game_txt = self.fuente.render("Presione [ENTER] para jugar.", True, (255, 255, 255))

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                pygame.mixer.music.fadeout(1200)
                self.game.set_scene(Game(self.game))

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((150, 142, 136))
        screen.blit(self.titulo, (0, 0))
        screen.blit(self.copas, (0, 32*2))
        screen.blit(self.enemigos, (0, 32*3))
        screen.blit(self.ataque1, (0, 32*4))
        screen.blit(self.ataque2, (0, 32*5))
        screen.blit(self.jefe1, (0, 32*6))
        screen.blit(self.jefe2, (0, 32*7))
        screen.blit(self.jefe3, (0, 32*8))
        screen.blit(self.jefe4, (0, 32*9))
        screen.blit(self.jefe5, (0, 32*10))
        screen.blit(self.cuchillos, (0, 32*11))

        screen.blit(self.ronda, (0, 32*13))
        screen.blit(self.ronda1, (0, 32*14))
        screen.blit(self.ronda2, (0, 32*15))
        screen.blit(self.ronda3, (0, 32*16))
        screen.blit(self.ronda4, (32*15, 32*14))
        screen.blit(self.ronda5, (32*15, 32*15))
        screen.blit(self.ronda6, (32*15, 32*16))
        screen.blit(self.game_txt, (0, 32*20))
    