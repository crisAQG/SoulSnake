import pygame
import math

from G5.Data.Modules.Type.SpriteSheet import SpriteSheet

class Entities:
    def __init__(self, pos: tuple, size: tuple, color: tuple, spd: float, hp: int, dmg: int, spr: str = None):
        self.pos = pos
        self.w = size[0]
        self.h = size[1]
        self.spr = spr
        self.spd = spd
        self.hp = hp
        self.dmg = dmg

        
class Enemy(Entities):
    def __init__(self, pos: tuple, size: tuple, color: tuple, spd: float, hp: int, dmg: int, spr: str = None):
        super().__init__(pos, size, color, spd, hp, dmg, spr)
        try:
            self.surf = SpriteSheet(spr).get_spr(0, 0, 32, 32)
            self.rect = self.surf.get_rect(topleft=(pos[0], pos[1]))
            self.use_sprite = True
        except:
            self.surf = pygame.Surface([self.w, self.h])
            self.surf.fill(color)
            self.rect = self.surf.get_rect(topleft=(pos[0], pos[1]))
            self.color = color
            self.use_sprite = False
    
    def set_vh(self):
        """
        Genera los vertices de la forma hexagonal
        """
        r = self.w/2
        vertices = []
        for i in range(6):
            angulo = math.pi/3 * i
            vx = self.pos[0] + r * math.cos(angulo)
            vy = self.pos[1] + r * math.sin(angulo)
            vertices.append((int(vx + self.w/2), int(vy + self.w/2)))
        
        return vertices
        
    def draw(self, screen):
        if self.use_sprite:
            screen.blit(self.surf, self.rect)
        else:
            pygame.draw.polygon(screen, self.color, self.set_vh())


class Player (Entities):
    def __init__(self, pos: tuple, size, color, spd, hp, dmg, spr = None):
        super().__init__(pos, size, color, spd, hp, dmg, spr)
        self.color = color
        try:
            self.surf = SpriteSheet(spr).get_spr(0, 0, 32, 32)
            self.rect = self.surf.get_rect(topleft=(pos[0], pos[1]))
            self.use_sprite = True
        except:
            self.surf = pygame.Surface([self.w, self.h])
            self.surf.fill(color)
            self.rect = self.surf.get_rect(topleft=(pos[0], pos[1]))
            self.use_sprite = False

    def set_vh(self):
            """
            Genera los vertices de la forma hexagonal
            """
            r = self.w/2
            vertices = []
            for i in range(6):
                angulo = math.pi/3 * i
                vx = self.pos[0] + r * math.cos(angulo)
                vy = self.pos[1] + r * math.sin(angulo)
                vertices.append((int(vx + self.w/2), int(vy + self.w/2)))
            
            return vertices

    def cambiar_direccion(self, direccion_actual):
        keys = pygame.key.get_pressed()

        # Tecla W
        if keys[pygame.K_w]:
            return (0, -1)

        # Tecla S
        if keys[pygame.K_s]:
            return (0, 1)

        # Tecla A
        if keys[pygame.K_a]:
            return (-1, 0)

        # Tecla D
        if keys[pygame.K_d]:
            return (1, 0)
        
        return direccion_actual


    def avanzar(self, tablero, direccion):
    
        dir_col, dir_fila = direccion
        ind_actual_col, ind_actual_fila = (
            self.pos
        )

        # Aplicamos la dirección a la posición del jugador.
        ind_nueva_col = ind_actual_col + dir_col
        ind_nueva_fila = ind_actual_fila + dir_fila

        # Verificamos que no haya choque con el borde del tablero.
        if not (0 <= ind_nueva_col < 15 and 0 <= ind_nueva_fila < 15):
            return "derrota", self.pos

        pos_elem = tablero[ind_nueva_fila][ind_nueva_col]

        if pos_elem == 2 or pos_elem == 3:
            return "derrota", self.pos

        if pos_elem == 4:
            return "victoria", (ind_nueva_col, ind_nueva_fila)

        # Movimiento normal, si es que no encontramos manzana ni obstáculo.
        tablero[ind_actual_fila][ind_actual_col] = 0
        tablero[ind_nueva_fila][ind_nueva_col] = 1

        return "ok", (ind_nueva_col, ind_nueva_fila)

    def draw(self, screen):
        if self.use_sprite:
            screen.blit(self.surf, self.rect)
        else:
            pygame.draw.polygon(screen, self.color, self.set_vh())
