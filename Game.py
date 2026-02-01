import arcade
import json
from Characters import Character
from Environment import *
from Consts import *

class WindNEarthGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.ALICE_BLUE)
        self.data = dict()
        
        # Списки спрайтов
        self.wallsList = arcade.SpriteList()
        self.crystalsList = arcade.SpriteList()
        self.buttonsList = arcade.SpriteList()
        self.playersList = arcade.SpriteList() 
        self.thingsList = arcade.SpriteList()
        
        self.crystalCount = 0

    def setup(self):
        '''Загрузка уровня и инициализация объектов'''
        with open("./levels/level.json", 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        self.loadSprites()

    def loadCharacters(self):
        '''Загрузка персонажей с использованием констант и данных из JSON'''
        self.Wind = Character(
            "Wind",
            WIND_IMAGE,
            CHAR_SCALE,
            self.data["players"][0]["x"],
            self.data["players"][0]["y"],
            arcade.key.UP,
            arcade.key.LEFT,
            arcade.key.RIGHT,
            arcade.key.PERIOD,
            self
        )
        self.Wind.physSetup()

        self.Earth = Character(
            "Earth",
            EARTH_IMAGE, 
            CHAR_SCALE,  
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
        '''Загрузка стен'''
        for wallData in self.data["walls_static"]:
            # Создаем временный объект, чтобы узнать его размеры для повторений
            temp_wall = Wall(wallData["image"], wallData["scale"], wallData["x"], wallData["y"])
            
            if "repeat_x" in wallData:
                for j in range(wallData["repeat_x"]):
                    self.wallsList.append(Wall(
                        wallData["image"], 
                        wallData["scale"], 
                        wallData["x"] + temp_wall.width * j, 
                        wallData["y"]
                    ))
            elif "repeat_y" in wallData:
                for j in range(wallData["repeat_y"]):
                    self.wallsList.append(Wall(
                        wallData["image"], 
                        wallData["scale"], 
                        wallData["x"], 
                        wallData["y"] + temp_wall.height * j
                    ))
            else:
                self.wallsList.append(temp_wall)

    def loadCrystals(self):
        for crystalData in self.data["crystals"]:
            crystal = Crystal(
                crystalData["image"],
                crystalData["x"],
                crystalData["y"],
                self,
                crystalData["owner"]
            )
            self.crystalsList.append(crystal)

    def loadDoorsNButtons(self):
        for doorData in self.data["doors"]:
            door = Door(doorData["image"], doorData["x"], doorData["y"])
            self.wallsList.append(door)

            # buttonData = self.data["buttons"][i]
            # button = Button(buttonData["image"],
            #                 buttonData["scale"],
            #                 buttonData["x"],
            #                 buttonData["y"],
            #                 buttonData["target_id"])
            # self.buttonsList.append(button)

    def loadSprites(self):
        self.loadWalls()
        self.loadCrystals()
        self.loadCharacters()
        self.loadDoorsNButtons()

    def on_draw(self):
        self.clear()
        self.wallsList.draw()
        self.buttonsList.draw()
        self.crystalsList.draw()
        self.thingsList.draw()
        self.playersList.draw()

    def on_update(self, delta_time):
        self.Wind.move()
        self.Earth.move()

        self.thingsList.update(delta_time)

        if self.Earth.physEngine:
            self.Earth.physEngine.update()
        if self.Wind.physEngine:
            self.Wind.physEngine.update()

        windStream = self.Wind.summonedThing
        if windStream and windStream.active:
            for player in self.playersList:
                if arcade.check_for_collision(player, windStream):
                    player.change_y = PLAYER_JUMP_SPEED * 0.8
                    
                    # Ограничение высоты взлета
                    if player.top > windStream.top:
                        player.top = windStream.top
                        player.change_y = 0

    def on_key_press(self, key, modifiers):
        self.Wind.on_key_press(key, modifiers)
        self.Earth.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.Wind.on_key_release(key, modifiers)
        self.Earth.on_key_release(key, modifiers)

if __name__ == '__main__':
    window = WindNEarthGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()