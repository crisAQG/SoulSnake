import math

import pygame
from Data.Modules.Type.SpriteSheet import SpriteSheet


class Entities:
    def __init__(self, x: int, y: int, size: tuple, color: tuple, spd: float, hp: int, dmg: int, spr: str = None):
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

        
class Enemies(Entities):
    def __init__(self, x: int, y: int, size: tuple, color: tuple, spd: float, hp: int, dmg: int, spr: str = None):
        super().__init__(x, y, size, color, spd, hp, dmg, spr)
        self.x = x
        self.y = y
        self.w = size[0]
        self.h = size[1]
        try:      
            self.spr = SpriteSheet(spr).get_spr(0, 0, 32, 32)
            self.rect = self.spr.get_rect(topleft=(x, y))
            self.centerx = self.surf.get_rect().centerx
            self.centery = self.surf.get_rect().centery
        except:
            self.surf = pygame.Surface([w, h])
            self.rect
            self.color = color
        self.spd = spd
        self.hp = hp
        self.dmg = dmg
        
        def set_vh(self):
            """
            Genera los vertices de la forma hexagonal
            """
            r = self.w/2
            vertices = []
            for i in range(6):
                angulo = math.pi/3 * i
                vx = self.x + r * math.cos(angulo)
                vy = self.y + r * math.sin(angulo)
                vertices.append((int(vx + self.w/2), int(vy + self.w/2)))
            
            return vertices
        
    def draw(self, screen):
            try: 
                screen.blit(self.image)
            
            except: 
                pygame.draw.polygon(screen, self.color, self.set_vh())