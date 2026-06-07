import pygame
import math


class Tile:
    def __init__(self, x, y, w, h, color, form: int):
        """

        :param x: Coordenada en x
        :param y: Coordenada en y
        :param w: Ancho
        :param h: Alto
        :param color: Color en hexadecimal
        :param form: 0 = cuadrado, 1 = hexagono, 2 = triangulo, 3 = diamante, 4 = circulo
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.form = form

        self.surf = pygame.Surface([w, h])
        self.centerx = self.surf.get_rect().centerx
        self.centery = self.surf.get_rect().centery

    def set_vh(self):
        """
        Genera los vertices de las formas 
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
        match self.form:
            case 0:
                pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))
            case 1:
                pygame.draw.polygon(screen, self.color, self.set_vh())
            case 2:
                pygame.draw.polygon(screen, self.color, [(self.w/2 + self.x, self.y), (self.x, self.h + self.y), (self.w +  + self.x, self.h + self.y)])
            case 3:
                pygame.draw.polygon(screen, self.color, [(self.w  + self.x, self.y), (self.x, self.y), (self.w/2  + self.x, self.h + self.y)])
            case 4:
                pygame.draw.circle(screen, self.color, (self.x + self.w/2, self.y + self.h/2), 16)
