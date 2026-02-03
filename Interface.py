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
        font_name: str = "Arial",
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
            arcade.draw_rectangle_outline(
                self.center_x,
                self.center_y,
                self.width + 4,
                self.height + 4,
                arcade.color.LIGHT_GRAY,
                border_width=2,
            )

        arcade.draw_text(
            self.label,
            start_x=self.center_x,
            start_y=self.center_y,
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
                print(
                    f"[ActionButton] Ошибка в обработчике кнопки "
                    f"'{self.label}': {e}"
                )

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
    def __init__(self, window: arcade.Window = None, levels: Optional[list] = None):
        super().__init__(window)
        arcade.set_background_color(arcade.color.BLACK)
        self.title_text = "Wind & Earth"

        self.levels = levels or ["./level.json"]
        self.buttons_list = arcade.SpriteList()

        start_x = self.window.width // 2 if self.window else 400
        start_y = self.window.height // 2 if self.window else 300
        gap = 70

        for i, level_path in enumerate(self.levels):
            label = f"Уровень {i + 1}"

            def make_action(path=level_path):
                return lambda: self._start_level(path)

            btn = ActionButton(
                width=220,
                height=50,
                label=label,
                action=make_action(level_path),
                center_x=start_x,
                center_y=start_y - i * gap,
                bg_color=arcade.color.DARK_SLATE_BLUE,
                text_color=arcade.color.WHITE,
            )
            self.buttons_list.append(btn)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_MIDNIGHT_BLUE)

    def on_draw(self):
        self.clear()

        if self.window:
            center_x = self.window.width // 2
            top_y = self.window.height - 80
        else:
            center_x = 400
            top_y = 560

        arcade.draw_text(
            self.title_text,
            center_x,
            top_y,
            arcade.color.WHITE,
            font_size=48,
            anchor_x="center",
        )

        for btn in self.buttons_list:
            btn.draw()

        arcade.draw_text(
            "Нажмите ESC чтобы вернуться/пауза в игре",
            10,
            10,
            arcade.color.LIGHT_GRAY,
            12,
        )

    def _start_level(self, level_json_path: str):
        print(f"[Menu] Запуск уровня: {level_json_path}")

        try:
            from Game import WindNEarthGameView
            game_view = WindNEarthGameView(level_json_path)
            if self.window:
                self.window.show_view(game_view)
            else:
                print("[Menu] Нет window в Menu — невозможно показать view.")
        except Exception:
            print("[Menu] Используйте main.py для запуска Game как Window (по умолчанию).")

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        for btn in self.buttons_list:
            btn.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        for btn in self.buttons_list:
            btn.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        for btn in self.buttons_list:
            btn.on_mouse_release(x, y, button, modifiers)

