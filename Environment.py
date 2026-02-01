import arcade


class Door(arcade.Sprite):

    def __init__(self, image, x, y):
        super().__init__(image, scale=0.5)
        self.center_x = x
        self.center_y = y

        self.closed_x = x
        self.is_open = False
        self.open_offset = 64

    def open(self):
        if not self.is_open:
            self.center_x -= self.open_offset
            self.is_open = True

    def close(self):
        if self.is_open:
            self.center_x = self.closed_x
            self.is_open = False


class Button(arcade.Sprite):

    def __init__(self, image, x, y, door: Door):
        super().__init__(image, scale=0.5)
        self.center_x = x
        self.center_y = y

        self.door = door
        self.isPressed = False

    def update(self, characters):
        pressed_now = False

        for character in characters:
            if arcade.check_for_collision(self, character):
                pressed_now = True
                break

        if pressed_now and not self.isPressed:
            self.isPressed = True
            self.door.open()
        elif not pressed_now and self.isPressed:
            self.isPressed = False
            self.door.close()


class Crystal(arcade.Sprite):

    def __init__(self, image, x, y, game, character):
        super().__init__(image, scale=0.5)
        self.center_x = x
        self.center_y = y

        self.character = character
        self.game = game
        self.collected = False

    def update(self, characters):
        if self.collected:
            return

        for char in characters:
            if arcade.check_for_collision(self, char):
                if self.character == char.name:
                    self.collected = True
                    self.game.crystalCount += 1
                    self.remove_from_sprite_lists()
                    break

class Wall(arcade.Sprite):
    def __init__(self, image, scale, x, y):
        super().__init__(image, scale)
        self.position = (x, y)