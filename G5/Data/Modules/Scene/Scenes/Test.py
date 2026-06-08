from G5.Data.Modules.Scene.Scene import Scene
from G5.Data.Modules.Type.Entities import Player
from G5.Data.Modules.Services.MapGen import MapGen


class Test(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.map = MapGen()

        self.map
        self.tab = self.map.map
        self.plr = Player((0, 0), (32, 32), (10, 30, 170), 0, 0, 0)

    def events(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        self.map.draw(screen, self.plr)
