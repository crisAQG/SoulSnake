from Data.Modules.Type.Blocks import Tile


class MapGen:
    def __init__(self):
        # 0 = Tile
        # 1 = Jugador
        # 2 = Enemigo
        # 3 = Obstaculo
        # 4 = Item

        self.map = [
            [000000000000000],
            [000000000000000],
            [000000000000000],
            [000000000000000],
            [000000000000000],
            [000000000000000],
            [000000000000000],
            [000000000000000],
            [000000000000000],
            [000000000000000],
            [000000000000000],
            [000000000000000],
            [000000000000000],
            [000000000000000],
            [000000000000000],
            [000000000000000],
        ]

        self.gen_map()
        self.gen_enemies()
        self.gen_items()
        self.gen_player()
        self.gen_obst()

    def gen_map(self):
        for i in range(map):
            for j in range(i):
                pass

    def gen_enemies(self):
        pass

    def gen_obst(self):
        pass
    
    def gen_player(self):
        pass

    def gen_items(self):
        pass
