import arcade


class Character(arcade.Sprite):
    '''Класс персонажей'''
    def __init__(self, image, scale, x, y, up, left, right, castKey):
        super().__init__(image, scale)
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

    def physSetup(self, game):
        '''Метод создания физических движков'''
        self.game = game
        self.physEngine = arcade.PhysicsEnginePlatformer(self, game.wallsList, gravity_constant=0.5)

    def on_key_press(self, key, modifiers):
        self.pressedKeys.add(key)
        if self.upKey == key:
            if self.physEngine.can_jump():
                self.change_y = self.jumpSpeed

    def move(self):
        '''Метод перемещения персонажа'''
        self.change_x = 0
        if self.leftKey in self.pressedKeys:
            self.change_x = -self.speed
        elif self.rightKey in self.pressedKeys:
            self.change_x = self.speed
            
    def on_key_release(self, key, modifiers):
        if key in self.pressedKeys:
            self.pressedKeys.remove(key)

    def update(self, delta_time):
        ...
    