import pygame
import math


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

class Player (Entities):
    def __init__(self, x, y, size, color, spd, hp, dmg, spr = None):
        super().__init__(x, y, size, color, spd, hp, dmg, spr)
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

    def cambiar_direccion(self, keys, direccion_actual):
        """
        Cambia la dirección del jugador.

        Parámetros:
            - keys: Arreglo de teclas presionadas.
            - direccion_actual: La dirección en la que estaba avanzando justo antes de analizar
                si hubo un cambio de dirección.

        Retorna:
            - direccion_actual: La nueva dirección del jugador.
        """

        # Tecla W
        if keys[pygame.K_w]:
            # La tupla nos indica que horizontalmente (columnas) no hará nada (0) y
            # que verticalmente (filas) disminuirá el índice en el tablero (-1).
            return (0, -1)

        # Tecla S
        if keys[pygame.K_s]:
            # En este caso avanzará a través de las filas del tablero.
            return (0, 1)

        # Tecla A
        if keys[pygame.K_a]:
            # Retrocede por las columnas del tablero.
            return (-1, 0)

        # Tecla D
        if keys[pygame.K_d]:
            # Avanza por las columnas del tablero.
            return (1, 0)

        # Si no se presiona ninguna de las teclas anteriores, la dirección
        # será la misma que la anterior.
        return direccion_actual


    def avanzar(self, tablero, pos_jugador, direccion):
        """
        Avanza el jugador un paso en la dirección dada.

        Parámetros:
            - tablero: El tablero con sus posiciones actuales.
            - pos_jugador: Tupla con la posición actual (índice con
                estructura (columna, fila)) del jugador en el tablero.
            - direccion: Tupla con la dirección en la que está avanzando actualmente el jugador.

        Retorna:
            - (resultado, nueva_pos_jugador): Retorna el resultado que se obtiene
                al avanzar (derrota, victoria o "ok" (no cambia de pantalla)) y la nueva posición del jugador.
        """

        # Obtenemos los componentes "x" e "y" de cada tupla recibida
        # con información de la dirección y posición del jugador.
        dir_col, dir_fila = direccion
        ind_actual_col, ind_actual_fila = (
            pos_jugador  # Tupla (columna, fila) que representa los índices en el tablero.
        )

        # Aplicamos la dirección a la posición del jugador.
        ind_nueva_col = ind_actual_col + dir_col
        ind_nueva_fila = ind_actual_fila + dir_fila

        # Verificamos que no haya choque con el borde del tablero.
        if not (0 <= ind_nueva_col < 15 and 0 <= ind_nueva_fila < 15):
            return "derrota", pos_jugador

        # Obtenemos el elemento que se encuentre en el tablero en la nueva posición del jugador.
        pos_elem = tablero[ind_nueva_fila][ind_nueva_col]

        if pos_elem == 3:
            return "derrota", pos_jugador

        if pos_elem == 4:
            return "victoria", (ind_nueva_col, ind_nueva_fila)

        # Movimiento normal, si es que no encontramos manzana ni obstáculo.
        tablero[ind_actual_fila][ind_actual_col] = 0
        tablero[ind_nueva_fila][ind_nueva_col] = 1

        return "ok", (ind_nueva_col, ind_nueva_fila)

    def draw(self, screen):
        pass