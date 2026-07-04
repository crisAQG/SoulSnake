from G5.Data.Modules.Type.Blocks import Tile
from G5.Data.Modules.Type.Entities import Enemy
from G5.Data.Modules.Type.SpriteSheet import SpriteSheet

import random


class MapGen:
    def __init__(self):
        # Tabla de IDs del mapa:
        # 0 = Tile vacío
        # 1 = Jugador (cabeza)
        # 2 = Enemigo
        # 3 = Obstáculo
        # 4 = Item (copa)
        # 5 = Cola del jugador

        self.map = self.gen_map()

        self.gen_object(2, 4)   # 4 enemigos
        self.gen_object(3, 6)   # 6 obstáculos
        self.gen_object(4, 1)   # 1 copa

    def gen_map(self):
        return [[0] * 15 for _ in range(15)]

    def gen_object(self, id_elem, cantidad=1):
        """
        Coloca `cantidad` objetos con el id `id_elem` en celdas vacías aleatorias.
        Devuelve lista de posiciones (col, fila) donde se colocaron.
        """
        colocados = []
        for _ in range(cantidad):
            vacios = [
                (col, fil)
                for fil in range(15)
                for col in range(15)
                if self.map[fil][col] == 0
            ]
            if not vacios:
                break
            columna, fila = random.choice(vacios)
            self.map[fila][columna] = id_elem
            colocados.append((columna, fila))
        return colocados

    def draw(self, screen, player):
        """
        Recorre el mapa celda por celda y dibuja lo que corresponda.
        Para el jugador (id=1) actualizamos su pos_destino para el lerp,
        pero NO lo dibujamos aquí: lo dibuja player.draw() usando pos_visual.
        """
        tam = 32

        for fila in range(15):
            for col in range(15):
                pos_x = col * tam
                pos_y = fila * tam
                valor = self.map[fila][col]

                if valor == 0:
                    tile = Tile(pos_x, pos_y, tam, tam, (140, 124, 137), 0)
                    tile.draw(screen)

                elif valor == 1:
                    # Le decimos al jugador cuál es su destino en píxeles.
                    # Él se moverá suavemente hacia ahí en update_visual().
                    player.set_destino(pos_x, pos_y)

                elif valor == 2:
                    enemy = Enemy((pos_x, pos_y), (tam, tam), (0, 170, 40), 0, 0, 0, SpriteSheet("G5/Data/Sprites/enemigo principal.png").get_spr(0, 0, tam, tam))
                    enemy.draw(screen)

                elif valor == 3:
                    bloque = Tile(pos_x, pos_y, tam, tam, (10, 10, 10), 0)
                    bloque.draw(screen)

                elif valor == 4:
                    item = Tile(pos_x, pos_y, tam, tam, (255, 215, 0), 4)  # dorado
                    item.draw(screen)

                elif valor == 5:
                    # Celda ocupada por la cola: dibujamos el piso debajo.
                    # El segmento de cola real lo dibuja player.draw() con lerp.
                    tile = Tile(pos_x, pos_y, tam, tam, (140, 124, 137), 0)
                    tile.draw(screen)

        # El jugador se dibuja al final, encima de todo, usando pos_visual (suavizado)
        player.draw(screen)