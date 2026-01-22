import arcade


class Character(arcade.Sprite):
    '''Класс персонажей'''
    def __init__(self, image, scale, x, y, up, left, right, castKey):
        super().__init__(image, scale)
        self.centerX = x
        self.centerY = y
        self.position = (self.centerX, self.centerY)

        self.upKey = up
        self.leftKey = left
        self.rightKey = right
        self.castKey = castKey 

        self.pressedKeys = set()

        self.speed = 20

    def on_key_press(self, key, modifiers):
        self.pressedKeys.add(key)

    def on_key_release(self, key, modifiers):
        if key in self.pressedKeys:
            self.pressedKeys.remove(key)

    def update(self, delta_time):
        ...
    