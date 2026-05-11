import pygame

from Config import *
from Data.Modules.Scene.Scenes import test

class Window:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()
        self.running = True

        self.scene = self.set_scene(test.test(self))

    def set_scene(self, scene):
        """
        Sistema de escenas, al seleccionar una clase anidada de scene (Data/Modules/Scene/Scene.py)
        se mostrara en pantalla los contenidos de la clase Scene, haciendo el enfoque modular

        Parametros:
            - scene: Escena anidada de scene.py
        """
        self.scene = scene

    def events(self):
        """
        Eventos de pygame con expansión a las escenas
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.scene:
                self.scene.events(event)

    def update(self):
        """
        Actualización en la escena actual
        """
        if self.scene:
            self.scene.update()

    def draw(self):
        """
        Se muestra en pantalla la escena actual
        """
        if self.scene:
            self.scene.draw(self.screen)

    def loop(self):
        """
        Bucle principal del juego
        """
        while self.running:
            self.clock.tick(fps)
            self.events()
            self.update()
            self.draw()
            pygame.display.flip()

