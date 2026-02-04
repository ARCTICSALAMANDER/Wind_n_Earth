import arcade
from arcade.particles import FadeParticle, Emitter, EmitBurst, EmitInterval, EmitMaintainCount
import random


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

    def crystalExplosion(self):
        '''метод создания частиц'''
        return Emitter(
            center_xy=(self.center_x, self.center_y),
            emit_controller=EmitBurst(30), # выбросить 30 частиц
            particle_factory=lambda emitter: FadeParticle(
                filename_or_texture=arcade.make_soft_circle_texture(8, arcade.color.BABY_BLUE),
                change_xy=arcade.math.rand_in_circle((0, 0), 3),
                lifetime=0.5, # живут полсекунды
                scale=0.7,
            )
        )

    def update(self, delta_time):
        if self.collected:
            return

        hit_players = arcade.check_for_collision_with_list(self, self.game.playersList)
        for player in hit_players:
            if player.name == self.character:
                self.game.crystalCount += 1
                self.game.explosionFxList.append(self.crystalExplosion())
                self.collected = True
                self.kill()
                break
                

class Wall(arcade.Sprite):
    def __init__(self, image, scale, x, y):
        super().__init__(image, scale)
        self.position = (x, y)
