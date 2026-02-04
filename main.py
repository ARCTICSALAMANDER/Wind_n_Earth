import arcade
from Interface import Menu
from Game import WindNEarthGame
from Consts import *


if __name__ == '__main__':
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = Menu(LEVELS_PATHS)
    window.show_view(menu_view)
    arcade.run()