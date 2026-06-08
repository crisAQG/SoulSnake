from G5.Data.Modules.Type.Blocks import Tile
from G5.Data.Modules.Type.Entities import Enemy

import random


class MapGen:
    def __init__(self):
        # 0 = Tile
        # 1 = Jugador
        # 2 = Enemigo
        # 3 = Obstaculo
        # 4 = Item

        self.map = self.gen_map()

        self.gen_object(1)
        self.gen_object(2, 4)
        self.gen_object(3, 6)
        self.gen_object(4, 1)

    def gen_map(self):
        return [[0] * 15 for _ in range(15)]

    def gen_object(self, id_elem, cantidad=1):
        colocados = []
 
        for _ in range(cantidad):
            vacios = [
                (col, fil)
                for fil in range(15)
                for col in range(15)
                if self.map[fil][col] == 0
            ]
 
            if not vacios:
                break  # No quedan celdas libres, detener
 
            columna, fila = random.choice(vacios)
            self.map[fila][columna] = id_elem
            colocados.append((columna, fila))
 
        return colocados
    
    def draw(self, screen, player):
        alto_elem = 32
        ancho_elem = 32

        pos_y = 0

        for i in range(15):
            pos_x = 0
            for j in range(15):
                if self.map[i][j] == 0:
                    tile = Tile(pos_x, pos_y, 32, 32, (140, 124, 137), 0)
                    tile.draw(screen)
                if self.map[i][j] == 2:
                    local_enemy = Enemy((pos_x, pos_y), (32, 32), (0, 170, 40), 0, 0, 0)
                    local_enemy.draw(screen)

                elif self.map[i][j] == 3:
                    Block = Tile(pos_x, pos_y, 32, 32, (10, 10, 10), 0)
                    Block.draw(screen)
                    
                elif self.map[i][j] == 1:
                    player.pos = (pos_x, pos_y)
                    player.rect = player.surf.get_rect(topleft=(pos_x, pos_y))
                    player.draw(screen)

                elif self.map[i][j] == 4:
                    Apple = Tile(pos_x, pos_y, 32, 32, (255, 0, 0), 4)
                    Apple.draw(screen)

                pos_x += ancho_elem
            pos_y += alto_elem