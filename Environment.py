import arcade
from arcade.particles import FadeParticle, Emitter, EmitBurst, EmitInterval, EmitMaintainCount
import random


class Door(arcade.Sprite):

    def __init__(self, image, x, y):
        super().__init__(image, scale=0.8)
        self.center_x = x
        self.center_y = y

        self.closed_y = y
        self.is_open = False
        self.open_offset = self.height

    def open(self):
        if not self.is_open:
            self.center_y -= self.open_offset
            self.is_open = True

    def close(self):
        if self.is_open:
            self.center_y = self.closed_y
            self.is_open = False


class Button(arcade.Sprite):
    def __init__(self, image, x, y, door: Door, game):
        super().__init__(image, scale=0.35)
        self.center_x = x
        self.center_y = y
        
        # Запоминаем начальную позицию для анимации
        self.base_y = y
        self.pressed_offset = 20 # На сколько пикселей кнопка уйдет вниз

        self.door = door
        self.isPressed = False
        self.game = game

    def update(self, delta_time):
        potential_pressers = arcade.SpriteList()
        for p in self.game.playersList:
            potential_pressers.append(p)
            
        earth_thing = getattr(self.game.Earth, "summonedThing", None)
        if earth_thing and earth_thing.active:
            potential_pressers.append(earth_thing)

        hit_list = arcade.check_for_collision_with_list(self, potential_pressers)
        pressed_now = len(hit_list) > 0

        if pressed_now:
            # опускаем кнопку
            self.center_y = self.base_y - self.pressed_offset
            
            if not self.isPressed:
                self.isPressed = True
                self.door.open()
        else:
            # исходное положение
            self.center_y = self.base_y
            
            if self.isPressed:
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


class FinalDoor(arcade.Sprite):
    def __init__(self, image, scale, x, y, tint_color, character, game):
        super().__init__(image, scale)
        self.color = tint_color
        self.character = character
        self.game = game
        self.activated = False

        self.position = (x, y)

    def update(self, delta_time):
        hit_players = arcade.check_for_collision_with_list(self, self.game.playersList)
        for player in hit_players:
            if player.name == self.character:
                self.activated = True
                break
        else:
            self.activated = False
