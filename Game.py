import arcade
from Characters import Character
import json

class WindNEarthGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, "Ветер и Земля")
        arcade.set_background_color(arcade.color.ALICE_BLUE)
        self.data = dict()

    def setup(self):
        with open("./levels/level.json", 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        self.playersList = arcade.SpriteList() 
        self.loadCharacters()
        self.playersList.append(self.Wind)
        self.playersList.append(self.Earth)

        self.wallsList = arcade.SpriteList() # неподвижные стены и ЗАКРЫТЫЕ двери

    def loadCharacters(self):
        '''Метод для загрузки персонажей из json-файла с 
            данными об уровне'''
        self.Wind = Character(
            self.data["players"][0]["image"],
            self.data["players"][0]["scale"],
            self.data["players"][0]["x"],
            self.data["players"][0]["y"],
            arcade.key.UP,
            arcade.key.LEFT,
            arcade.key.RIGHT,
            arcade.key.GREATER
        )

        self.Earth = Character(
            self.data["players"][1]["image"],
            self.data["players"][1]["scale"],
            self.data["players"][1]["x"],
            self.data["players"][1]["y"],
            arcade.key.W,
            arcade.key.A,
            arcade.key.S,
            arcade.key.E
        )

    def on_draw(self):
        self.playersList.draw()


if __name__ == '__main__':
    window = WindNEarthGame(800, 600)
    window.setup()
    arcade.run()

    