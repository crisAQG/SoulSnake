import pygame


class SpriteSheet:
    _cache = {}
    def __init__(self, file: str):
        """
        :param file: Ruta de la imagen (str)
        :param a: Transparencia (float)
        """
        if file not in SpriteSheet._cache:
            SpriteSheet._cache[file] = pygame.image.load(file).convert_alpha()
        self.sheet = SpriteSheet._cache[file]

    def get_spr(self, x, y, w, h):
        sprite = pygame.Surface([w, h], pygame.SRCALPHA)
        sprite.blit(self.sheet, (0, 0), (x, y, w, h))

        return sprite