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
        bg_color: Tuple[int, int, int, int] = arcade.color.DARK_BLUE_GRAY,
        text_color: Tuple[int, int, int, int] = arcade.color.WHITE,
        font_size: int = 18,
        font_name: str = "Arial",
    ):
        super().__init__(width, height, color=bg_color)
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
        if self.is_hovered:
            rect = arcade.rect.XYWH(self.center_x, self.center_y, self.width+4, self.height+4)
            arcade.draw_rect_outline(
                rect,
                color=arcade.color.LIGHT_GRAY,
                border_width=2,
            )

        arcade.draw_text(
            self.label,
            x=self.center_x,
            y=self.center_y,
            color=self.text_color,
            font_size=self.font_size,
            font_name=self.font_name,
            anchor_x="center",
            anchor_y="center",
        )

    def on_click(self):
        if callable(self.action):
            try:
                self.action()
            except Exception as e:
                print(f"[ActionButton] Ошибка в обработчике кнопки '{self.label}': {e}")

    def check_mouse_over(self, x: float, y: float) -> bool:
        # Стандартная проверка попадания точки в прямоугольник спрайта
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
    def __init__(self, levels: Optional[list] = None):
        super().__init__()
        self.title_text = "Wind & Earth"
        self.levels = levels or ["./levels/level.json"] # Путь должен соответствовать твоей папке
        self.buttons_list = arcade.SpriteList()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_MIDNIGHT_BLUE)
        self.setup_buttons()

    def setup_buttons(self):
        self.buttons_list.clear()
        start_x = self.window.width // 2
        start_y = self.window.height // 2 + 50
        gap = 70

        for i, level_path in enumerate(self.levels):
            label = f"Уровень {i + 1}"
            
            # Замыкание для передачи пути уровня в функцию запуска
            def make_action(path):
                return lambda: self._start_level(path)

            btn = ActionButton(
                width=220,
                height=50,
                label=label,
                action=make_action(level_path),
                center_x=start_x,
                center_y=start_y - i * gap,
                bg_color=arcade.color.DARK_SLATE_BLUE,
            )
            self.buttons_list.append(btn)

    def on_draw(self):
        self.clear()

        # Заголовок
        arcade.draw_text(
            self.title_text,
            self.window.width // 2,
            self.window.height - 100,
            arcade.color.WHITE,
            font_size=48,
            anchor_x="center",
        )

        # Кнопки
        for btn in self.buttons_list:
            btn.draw()

        # Подсказка
        arcade.draw_text(
            "Нажмите ESC для паузы во время игры",
            20,
            20,
            arcade.color.LIGHT_GRAY,
            font_size=12,
        )

    def _start_level(self, level_json_path: str):
        print(f"[Menu] Запуск уровня: {level_json_path}")
        from Game import WindNEarthGame
        game_view = WindNEarthGame("./levels/level.json")
        game_view.setup()
        self.window.show_view(game_view)

    def on_mouse_motion(self, x, y, dx, dy):
        for btn in self.buttons_list:
            btn.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        for btn in self.buttons_list:
            btn.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        for btn in self.buttons_list:
            btn.on_mouse_release(x, y, button, modifiers)