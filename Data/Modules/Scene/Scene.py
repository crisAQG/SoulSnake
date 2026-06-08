from Data.Modules.Window import Window


class Scene:
    def __init__(self, game: Window):
        self.game = game

    def events(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass