

import os
import arcade

from src.parsing.parse_main import leaderboard_extract

# ----| CONSTANTS |---- #
PATH = "assets/menu/"
FONT_PATH = "assets/font/"
LEAD_PATH = "data/leaderboard.json"
# --------------------- #


class HighscoreView(arcade.View):
    """
    This class displays the leaderboard.
    """
    def __init__(self) -> None:
        super().__init__()
        self.text_list: list[arcade.Text] = []

        # Loads the background
        try:
            if not os.path.exists("assets/"):
                raise ValueError

            self.background: arcade.Texture = \
                arcade.load_texture(f"{PATH}main_menu.png")
            arcade.load_font(f"{FONT_PATH}PublicPixel.ttf")

        except FileNotFoundError:
            raise ValueError("\033[1;91mBackground file not found!\033[0m")

        self.text = arcade.Text(text="Press ESCAPE to go back",
                                x=self.width / 2, y=100,
                                color=arcade.color.BRONZE,
                                font_size=10, anchor_x="center",
                                font_name="Public Pixel")

        self.leaderboard()

    def leaderboard(self) -> None:
        y = 800
        i = 0

        content_file = leaderboard_extract(LEAD_PATH)

        content = content_file.split("\n")

        for score in content:
            if i % 2 == 0:
                text = arcade.Text(text=score, x=260, y=y,
                                   color=arcade.color.BLACK, font_size=24,
                                   align="left", font_name="Public Pixel")

            else:
                text = arcade.Text(text=score, x=750, y=y,
                                   color=arcade.color.BLACK, font_size=24,
                                   align="left", font_name="Public Pixel")
                y -= 55

            self.text_list.append(text)

            i += 1

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            self.window.switch_menu()

    def on_draw(self) -> None:
        self.clear()

        # Draws the background
        arcade.draw_texture_rect(self.background,
                                 arcade.LBWH(0, 0, self.width, self.height))

        # Displays the top-scorer
        for text in self.text_list:
            text.draw()

        self.text.draw()
