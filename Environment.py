import arcade


class Door(arcade.Sprite):
    def __init__(self, image, x, y):
        super().__init__(image, scale=0.5)
        self.center_x = x
        self.center_y = y
        self.start_x = x

    def open(self):
        # дверь уезжает влево
        self.center_x -= 50

    def close(self):
        # дверь возвращается обратно
        self.center_x = self.start_x


class Button(arcade.Sprite):
    def __init__(self, image, x, y, door: Door):
        super().__init__(image, scale=0.5)
        self.center_x = x
        self.center_y = y

        # дверь, которую открывает кнопка
        self.door = door
        self.isPressed = False

    def press(self):
        self.isPressed = True
        self.door.open()

    def release(self):
        self.isPressed = False
        self.door.close()


class Crystal(arcade.Sprite):
    def __init__(self, image, x, y, game, character):
        super().__init__(image, scale=0.5)
        self.center_x = x
        self.center_y = y

        self.character = character
        self.game = game

    def collect(self, character):
        if isinstance(character, self.character):
            self.game.crystalCount += 1
            self.remove_from_sprite_lists()