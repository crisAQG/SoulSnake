import pygame


class SpriteSheet:
    def __init__(self, file):
        """
        Parametros:
        """
        self.sheet = pygame.image.load(file).convert_alpha()

    def get_spr(self, x, y, w, h):
        sprite = pygame.Surface([w, h], pygame.SRCALPHA)
        sprite.blit(self.sheet, (0, 0), (x, y, w, h))

        return sprite