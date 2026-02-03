import arcade
import json
from Characters import Character
from Environment import *
from Consts import *
from typing import Optional
import math


class WindNEarthGame(arcade.Window):
    def __init__(self, width, height, title, levelDataFile: str):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.ALICE_BLUE)

        self.levelDataFile = levelDataFile
        self.data = dict()

        self.wallsList = arcade.SpriteList()
        self.crystalsList = arcade.SpriteList()
        self.buttonsList = arcade.SpriteList()
        self.playersList = arcade.SpriteList()
        self.thingsList = arcade.SpriteList()

        self.time_elapsed = 0.0
        self.paused = False

        self.totalCrystalCount = 0
        self.crystalCount = 0

        self.Wind: Optional[Character] = None
        self.Earth: Optional[Character] = None

    def setup(self):
        """Загрузка данных уровня из JSON и подготовка спрайтов."""
        with open(self.levelDataFile, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        self.loadSprites()

        if "crystals" in self.data:
            self.totalCrystalCount = len(self.data["crystals"])
        else:
            self.totalCrystalCount = len(self.crystalsList)

        self.time_elapsed = 0.0
        self.paused = False

    def loadCharacters(self):
        """Создание объектов персонажей Wind и Earth."""
        players_data = self.data.get("players", [])
        if len(players_data) < 2:
            raise RuntimeError(
                "В JSON ожидается минимум 2 игрока в ключе 'players'"
            )

        self.Wind = Character(
            "Wind",
            WIND_IMAGE,
            CHAR_SCALE,
            players_data[0]["x"],
            players_data[0]["y"],
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
            players_data[1]["x"],
            players_data[1]["y"],
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
        """Загрузка статических стен из данных уровня."""
        for wallData in self.data.get("walls_static", []):
            temp_wall = Wall(
                wallData["image"],
                wallData["scale"],
                wallData["x"],
                wallData["y"]
            )

            if "repeat_x" in wallData:
                for j in range(wallData["repeat_x"]):
                    self.wallsList.append(
                        Wall(
                            wallData["image"],
                            wallData["scale"],
                            wallData["x"] + temp_wall.width * j,
                            wallData["y"]
                        )
                    )
            elif "repeat_y" in wallData:
                for j in range(wallData["repeat_y"]):
                    self.wallsList.append(
                        Wall(
                            wallData["image"],
                            wallData["scale"],
                            wallData["x"],
                            wallData["y"] + temp_wall.height * j
                        )
                    )
            else:
                self.wallsList.append(temp_wall)

    def loadCrystals(self):
        """Создание объектов кристаллов уровня."""
        for crystalData in self.data.get("crystals", []):
            crystal = Crystal(
                crystalData["image"],
                crystalData["x"],
                crystalData["y"],
                self,
                crystalData.get("owner", None)
            )
            self.crystalsList.append(crystal)
