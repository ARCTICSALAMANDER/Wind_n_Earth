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
        thingParams = self.game.data["summoned_things"]
        self.summonedThing = SummonedThing(thingParams["width"], thingParams["height"], thingParams["color"], self, self.game)

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

    def on_key_release(self, key, modifiers):
        if key in self.pressedKeys:
            self.pressedKeys.remove(key)

    def update(self, delta_time):
        ...


class SummonedThing(arcade.SpriteSolidColor):
    def __init__(self, width, height, color: tuple, owner: Character, game):
        super().__init__(width, height, color=color)
        self.owner = owner
        self.game = game
        self.physEngine = None
        self.active = False

        self.center_x = self.owner.center_x
        self.bottom = self.owner.bottom

        if self.owner.name == "Earth":
            self.physEngine = self.owner.physEngine

        self.timer = 0

    def update(self, delta_time):
        if not self.active:
            return

        if self.owner.name == "Wind":
            self.timer += delta_time
            self.alpha = int(140 + math.sin(self.timer * 6) * 40)       
        elif self.owner.name == "Earth":
            # Куб земли просто стоит там, где его создали, 
            # но его сделать толкаемым
            pass