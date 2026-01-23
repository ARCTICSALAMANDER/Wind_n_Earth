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

        self.speed = 10
        self.jumpSpeed = 20
        self.physEngine = arcade.PhysicsEnginePlatformer(self)

    def on_key_press(self, key, modifiers):
        self.pressedKeys.add(key)
        if self.upKey == key:
            if self.physEngine.can_jump():
                self.change_y = self.jumpSpeed

    def move(self):
        '''Метод перемещения персонажа'''
        if self.leftKey in self.pressedKeys:
            self.change_x = -self.speed
        if self.rightKey in self.pressedKeys:
            self.change_x = self.speed

    def on_key_release(self, key, modifiers):
        if key in self.pressedKeys:
            self.pressedKeys.remove(key)

    def update(self, delta_time):
        ...
    