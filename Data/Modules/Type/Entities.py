import pygame


class Entities:
    def __init__(self, x: int, y: int, size: tuple, color: tuple, spd: float, hp: int, dmg: int, spr: pygame.Surface = None):
        self.x = x
        self.y = y
        self.w = size[0]
        self.h = size[1]
        if spr is not None: 
            self.spr = spr
        else:
            self.spr = color
        self.spd = spd
        self.hp = hp
        self.dmg = dmg
