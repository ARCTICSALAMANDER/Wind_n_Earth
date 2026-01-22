# НЕ ИМПОРТИРОВАТЬ КЛАССЫ ИЗ ДРУГИХ СКРИПТОВ ПРОЕКТА
import arcade


class Door(arcade.Sprite):
    '''Класс двери'''

    def __init__(self, image, x, y):
        super().__init__(image, scale=0.5)

    def open(self):
        '''Метод открытия двери'''
        # чтобы было проще с анимацией, делаем пока что
        # только горизонтальные двери, которые по нажатию
        # кнопки будут уезжать внутрь стены
        ...

    def close(self):
        '''Метод закрытия двери'''
        # дверь выезжает из стены


class Button(arcade.Sprite):
    '''Класс кнопки'''

    def __init__(self, door: Door):
        # сюда кладете дверь, которая будет открываться
        # по нажатию этой кнопки, при коллизии любого
        # персонажа и этой кнопки вызвать self.door.open()
        self.door = door

        # нажата ли кнопка. Если персонаж наступит, 
        # self.isPressed = True, если уйдет с кнопки - 
        # self.isPressed = False и self.door.close()
        self.isPressed = False


class Crystal(arcade.Sprite):
    '''Класс кристалла'''

    def __init__(self, game, character):
        # сюда кладете КЛАСС персонажа, который сможет собрать
        # этот кристалл. Если с кристаллом произойдет коллизия,
        # то соберется он при условии, что класс у self.character
        # и персонажа, соприкоснувшегося с ним, одинаковый
        # (погуглите функцию isinstance)
        self.character = character

        # когда кристалл соберется нужным персонажем, нужно сделать
        # self.game.crystalCount += 1
        self.game = game