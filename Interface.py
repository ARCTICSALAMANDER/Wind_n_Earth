import arcade
from typing import Callable, Optional, Tuple











class ActionButton(arcade.SpriteSolidColor):
    def __init__(
        self,
        width: int,
        height: int,
        label: str,
        action: Optional[Callable] = None,
        center_x: float = 0,
        center_y: float = 0,
        bg_color: Tuple[int, int, int] = arcade.color.DARK_BLUE_GRAY,
        text_color: Tuple[int, int, int] = arcade.color.WHITE,
        font_size: int = 18,
        font_name: str = "Arial"
    ):
                super().__init__(width, height, bg_color)
        self.label = label
        self.action = action
        self.center_x = center_x
        self.center_y = center_y
        self.text_color = text_color
        self.font_size = font_size
        self.font_name = font_name

        
        self.is_hovered = False
        self.is_pressed = False

    def draw(self):
        
        super().draw()

        
        if self.is_hovered:
            arcade.draw_rectangle_outline(self.center_x, self.center_y, self.width + 4, self.height + 4, arcade.color.LIGHT_GRAY, border_width=2)

        
        arcade.draw_text(
            self.label,
            start_x=self.center_x,
            start_y=self.center_y,
            color=self.text_color,
            font_size=self.font_size,
            font_name=self.font_name,
            anchor_x="center",
            anchor_y="center"
        )

    def on_click(self):
                if callable(self.action):
            try:
                
                self.action()
            except Exception as e:
                
                print(f"[ActionButton] Ошибка в обработчике кнопки '{self.label}': {e}")

    def check_mouse_over(self, x: float, y: float) -> bool:
                return (self.left <= x <= self.right) and (self.bottom <= y <= self.top)

    
    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.is_hovered = self.check_mouse_over(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if self.check_mouse_over(x, y):
            self.is_pressed = True

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        if self.is_pressed and self.check_mouse_over(x, y):
            self.on_click()
        self.is_pressed = False


class Menu(arcade.View): 
    def __init__(self): 
        # тут нужно настроить внешний вид, т.е.: # поставить цвет фона, отрисовать название игры по центру в верхней части экрана, # отрисовать кнопки с номерами уровней. Для каждой такой кнопки по ее нажатию # нужно создавать объект класса Game, и в качестве аргумента передавать путь # к json-файлу, в котором лежит информация об уровне. Пример можно посмотреть в файле Game.py # в самом низу, после if __name__ == "main" pass
