from Consts import EARTH_CUBE_COLOR, EARTH_CUBE_SIZE, GRAVITY, WIND_STREAM_COLOR
import arcade
import math


class Character(arcade.Sprite):
    '''Класс персонажей'''

    def __init__(self, name: str, image: str, scale: float, x: int, y: int, up, left, right, castKey, game):
        super().__init__(image, scale)
        self.name = name
        self.game = game

        self.position = (x, y)
        self.change_x = 0
        self.change_y = 0

        self.upKey = up
        self.leftKey = left
        self.rightKey = right
        self.castKey = castKey

        self.pressedKeys = set()

        self.speed = 5
        self.jumpSpeed = 7
        self.physEngine = None

    def physSetup(self):
        '''Метод создания физических движков'''
        self.physEngine = arcade.PhysicsEnginePlatformer(
            self, self.game.wallsList, gravity_constant=0.5)

        self.summonedThingSetup()

    def summonedThingSetup(self):
        '''Метод создания кубика Земли или воздушного потока Ветра'''
        if self.name == "Wind":
            streamParams = self.game.data["summoned_things"]
            self.summonedThing = WindStream(streamParams["width"], streamParams["height"], self)
        elif self.name == "Earth":
            cubeParams = self.game.data["summoned_things"]
            self.summonedThing = EarthCube(self, self.game)

    def on_key_press(self, key, modifiers):
        self.pressedKeys.add(key)
        if self.upKey == key:
            if self.physEngine and self.physEngine.can_jump():
                self.change_y = self.jumpSpeed

        if key == self.castKey:
            self.summon()

    def move(self):
        '''Метод перемещения персонажа'''
        self.change_x = 0
        if self.leftKey in self.pressedKeys:
            self.change_x = -self.speed
        elif self.rightKey in self.pressedKeys:
            self.change_x = self.speed

    def summon(self):
        '''Метод призыва кубика или ветряного потока'''
        self.summonedThing.active = True

        self.summonedThing.center_x = self.center_x
        self.summonedThing.bottom = self.bottom

        if self.summonedThing not in self.game.thingsList:
            self.game.thingsList.append(self.summonedThing)

        self.game.update_player_physics()

    def on_key_release(self, key, modifiers):
        if key in self.pressedKeys:
            self.pressedKeys.remove(key)

    def update(self, delta_time):
        ...


class SummonedThing(arcade.SpriteSolidColor):
    def __init__(self, width, height, color: tuple, owner: Character):
        super().__init__(width, height, color=color)
        self.owner = owner
        self.physEngine = None
        self.active = False

        self.center_x = self.owner.center_x
        self.bottom = self.owner.bottom

        self.timer = 0

    def update(self, delta_time):
        if not self.active:
            return 


class WindStream(SummonedThing):
    def __init__(self, width, height, wind: Character):
        super().__init__(width, height, WIND_STREAM_COLOR, wind)

    def update(self, delta_time):
        super().update(delta_time)
        
        # по идее должен красиво мерцать
        self.timer += delta_time
        self.alpha = int(140 + math.sin(self.timer * 6) * 40)
        

class EarthCube(SummonedThing):
    def __init__(self, earth: Character, game):
        super().__init__(EARTH_CUBE_SIZE, EARTH_CUBE_SIZE, EARTH_CUBE_COLOR, earth)
        print(earth.height, self.height)
        self.game = game

        self.physEngine = arcade.PhysicsEnginePlatformer(self, self.game.wallsList, GRAVITY)

    def update(self, delta_time):
        super().update(delta_time)
        self.change_x = 0

        hit_players = arcade.check_for_collision_with_list(self, self.game.playersList)
        for player in hit_players:
            if abs(player.change_x) > 0:
                self.change_x = player.change_x

        self.physEngine.update()
