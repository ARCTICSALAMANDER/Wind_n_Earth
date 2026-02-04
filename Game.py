import arcade
import json
from Characters import Character
from Environment import *
from Consts import *
from typing import Optional
import math


class WindNEarthGame(arcade.View):
    def __init__(self, levelDataFile: str):
        super().__init__()
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

    def loadDoorsNButtons(self):
        """Создание дверей и кнопок уровня."""
        for doorData in self.data.get("doors", []):
            door = Door(doorData["image"], doorData["x"], doorData["y"])
            self.wallsList.append(door)

    def loadSprites(self):
        """Загрузка всех спрайтов уровня."""
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

        # Отображение таймера
        total_seconds = int(self.time_elapsed)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        time_str = f"{minutes:02d}:{seconds:02d}"

        padding = 10
        font_size = 20
        arcade.draw_text(
            f"Время: {time_str}",
            padding,
            self.height - padding - font_size,
            arcade.color.BLACK,
            font_size
        )

        # Отображение собранных кристаллов
        collected = self.totalCrystalCount - len(self.crystalsList)
        arcade.draw_text(
            f"Кристаллы: {collected} / {self.totalCrystalCount}",
            self.width - padding,
            self.height - padding - font_size,
            arcade.color.BLACK,
            font_size,
            anchor_x="right"
        )

        # Отображение паузы
        if self.paused:
            overlay_w = 400
            overlay_h = 200
            rect = arcade.rect.XYWH(self.width / 2,
                                    self.height / 2,
                                    overlay_w,
                                    overlay_h,)

            arcade.draw_rect_filled(
                rect,
                arcade.color.BLACK,
                180
            )
            arcade.draw_text(
                "Пауза",
                self.width / 2,
                self.height / 2 + 40,
                arcade.color.WHITE,
                34,
                anchor_x="center"
            )
            arcade.draw_text(
                "ESC — продолжить",
                self.width / 2,
                self.height / 2 - 20,
                arcade.color.LIGHT_GRAY,
                16,
                anchor_x="center"
            )

    def on_update(self, delta_time):
        """Обновление состояния игры каждый кадр."""
        if not self.paused:
            self.time_elapsed += delta_time

        if self.Wind:
            self.Wind.move()
        if self.Earth:
            self.Earth.move()

        self.thingsList.update(delta_time)

        if self.Earth and self.Earth.physEngine:
            self.Earth.physEngine.update()
        if self.Wind and self.Wind.physEngine:
            self.Wind.physEngine.update()

        windStream = getattr(self.Wind, "summonedThing", None)
        if windStream and getattr(windStream, "active", False):
            for player in self.playersList:
                if arcade.check_for_collision(player, windStream):
                    player.change_y = PLAYER_JUMP_SPEED * 0.8
                    if player.top > windStream.top:
                        player.top = windStream.top
                        player.change_y = 0

        self.crystalCount = self.totalCrystalCount - len(self.crystalsList)

    def on_key_press(self, key, modifiers):
        if self.Wind:
            self.Wind.on_key_press(key, modifiers)
        if self.Earth:
            self.Earth.on_key_press(key, modifiers)

        if key == arcade.key.ESCAPE:
            self.paused = not self.paused

    def on_key_release(self, key, modifiers):
        if self.Wind:
            self.Wind.on_key_release(key, modifiers)
        if self.Earth:
            self.Earth.on_key_release(key, modifiers)


# if __name__ == '__main__':
#     window = WindNEarthGame("levels/level.json")
#     window.setup()
#     arcade.run()
