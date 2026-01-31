import arcade
from Characters import Character
from Environment import *
import json

class WindNEarthGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, "Ветер и Земля")
        arcade.set_background_color(arcade.color.ALICE_BLUE)
        self.data = dict()

    def setup(self):
        with open("./levels/level.json", 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        self.wallsList = arcade.SpriteList() # неподвижные стены и ЗАКРЫТЫЕ двери
        self.crystalsList = arcade.SpriteList()
        self.buttonsList = arcade.SpriteList()
        self.playersList = arcade.SpriteList() 
        self.thingsList = arcade.SpriteList()

        self.loadSprites()

    def loadCharacters(self):
        '''Метод для загрузки персонажей из json-файла с 
            данными об уровне'''
        self.Wind = Character(
            "Wind",
            self.data["players"][0]["image"],
            self.data["players"][0]["scale"],
            self.data["players"][0]["x"],
            self.data["players"][0]["y"],
            arcade.key.UP,
            arcade.key.LEFT,
            arcade.key.RIGHT,
            arcade.key.GREATER,
            self
        )
        self.Wind.physSetup()

        self.Earth = Character(
            "Earth",
            self.data["players"][1]["image"],
            self.data["players"][1]["scale"],
            self.data["players"][1]["x"],
            self.data["players"][1]["y"],
            arcade.key.W,
            arcade.key.A,
            arcade.key.D,
            arcade.key.E,
            self
        )
        self.Earth.physSetup()

        self.playersList.append(self.Wind)
        self.playersList.append(self.Earth)

    def loadWalls(self):
        '''Метод загрузки стен из json-файла'''
        for i in range(len(self.data["walls_static"])):
            wallData = self.data["walls_static"][i]
            wall = Wall(wallData["image"], wallData["scale"], wallData["x"], wallData["y"]) # для получения ширины или высоты
            # print(wall.width, wall.height) 64, 64
            if "repeat_x" in wallData.keys():
                for j in range(wallData["repeat_x"]):
                    self.wallsList.append(Wall(wallData["image"], 
                                               wallData["scale"], 
                                               wallData["x"] + wall.width * j, 
                                               wallData["y"]))
            elif "repeat_y" in wallData.keys():
                for j in range(wallData["repeat_y"]):
                    self.wallsList.append(Wall(wallData["image"], 
                                               wallData["scale"], 
                                               wallData["x"], 
                                               wallData["y"] + wall.height * j))
                    
    def loadCrystals(self):
        '''Метод загрузки кристаллов из json-файла'''
        for i in range(len(self.data["crystals"])):
            crystalData = self.data["crystals"][i]
            crystal = Crystal(crystalData["image"],
                              crystalData["scale"],
                              crystalData["x"],
                              crystalData["y"],
                              self,
                              crystalData["owner"])
            
            self.crystalsList.append(crystal)

    def loadDoorsNButtons(self):
        '''Метод загрузки дверей и кнопок из json-файла'''
        for i in range(len(self.data["doors"])):
            doorData = self.data["doors"][i]
            door = Door(doorData["image"],
                        doorData["scale"],
                        doorData["x"],
                        doorData["y"],
                        doorData["id"])
            self.wallsList.append(door)
            
            # buttonData = self.data["buttons"][i]
            # button = Button(buttonData["image"],
            #                 buttonData["scale"],
            #                 buttonData["x"],
            #                 buttonData["y"],
            #                 buttonData["target_id"])
            # self.buttonsList.append(button)

    def loadSprites(self):
        '''Метод загрузки спрайтов из json-файла'''
        self.loadWalls()
        self.loadCrystals()
        self.loadCharacters()
        self.loadDoorsNButtons()

    def on_draw(self):
        self.clear()

        self.playersList.draw()
        self.wallsList.draw()
        self.crystalsList.draw()
        self.buttonsList.draw()
        self.thingsList.draw()

    def on_update(self, delta_time):
        self.Wind.change_x = 0
        self.Earth.change_x = 0

        self.Wind.move()
        self.Earth.move()

        windStream = self.Wind.summonedThing
        if windStream.active:
            for player in self.playersList:
                if arcade.check_for_collision(player, windStream):
                    player.change_y = 8

                # чтобы игрок не вылетал за пределы воздушного потока
                if player.top > windStream.top:
                    player.top = windStream.top
                    player.change_y = 0

        if self.Earth.physEngine and self.Wind.physEngine:
            self.Earth.physEngine.update()
            self.Wind.physEngine.update()

    def on_key_press(self, key, modifiers):
        self.Wind.on_key_press(key, modifiers)
        self.Earth.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.Wind.on_key_release(key, modifiers)
        self.Earth.on_key_release(key, modifiers)


if __name__ == '__main__':
    window = WindNEarthGame(800, 600)
    window.setup()
    arcade.run()

    