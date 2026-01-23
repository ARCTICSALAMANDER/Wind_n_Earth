# НЕ ИМПОРТИРОВАТЬ КЛАССЫ ИЗ ДРУГИХ СКРИПТОВ ПРОЕКТА
import arcade


class Door(arcade.Sprite):
    '''Класс двери'''

    def __init__(self, image, scale, x, y, doorId):
        super().__init__(image, scale)
        self.doorId = doorId # номер, по которому связываем кнопку с дверью

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

    def __init__(self, image, scale, x, y, door: Door):
        super().__init__(image, scale)
        self.position = (x, y)
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

    def __init__(self, image, scale, x, y, game, character):
        super().__init__(image, scale)
        self.position = (x, y)
        # сюда кладете строку с именем персонажа, который должен
        # этот кристалл собрать ("Wind" / "Earth"). При коллизии
        # проверяте, что атрибут name у персонажа равен self.character,
        # затем делаем self.kill(), чтобы удалить кристалл
        self.character = character

        # когда кристалл соберется нужным персонажем, нужно сделать
        # self.game.crystalCount += 1
        self.game = game


class Wall(arcade.Sprite):
    def __init__(self, image, scale, x, y):
        super().__init__(image, scale)
        self.position = (x, y)