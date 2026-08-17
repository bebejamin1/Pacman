import os
import arcade

from src.parsing.parse_main import leaderboard_extract

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.renderer.game_engine import GameEngine

PATH = "assets/background/"
FONT_PATH = "assets/font/"
LEAD_PATH = "data/leaderboard.json"


class HighscoreView(arcade.View):
    """Displays the top-10 leaderboard."""

    def __init__(self, window: "GameEngine") -> None:
        """Load the highscore background and font.

        Args:
            window: Owning game window.

        Raises:
            ValueError: If the ``assets/`` folder is missing.
        """
        super().__init__()
        self.window: GameEngine = window
        self.text_list: list[arcade.Text] = []

        try:
            if not os.path.exists("assets/"):
                raise ValueError

            self.background: arcade.Texture = \
                arcade.load_texture(f"{PATH}main_menu.png")
            arcade.load_font(f"{FONT_PATH}PublicPixel.ttf")

        except FileNotFoundError:
            raise ValueError("\033[1;91mBackground file not found!\033[0m")

        self.instruction = arcade.Text(text="Press ESCAPE to go back",
                                       x=self.width / 2, y=100,
                                       color=arcade.color.BRONZE,
                                       font_size=10, anchor_x="center",
                                       font_name="Public Pixel")

    def leaderboard(self) -> None:
        """Build the ranked list of highscore text objects."""
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
        """Return to the main menu.

        Args:
            symbol: Key that was pressed.
            modifiers: Active modifier keys (unused).
        """
        if symbol == arcade.key.ESCAPE:
            self.window.switch_menu()

    def on_draw(self) -> None:
        """Draw the background and the leaderboard entries."""
        self.clear()

        arcade.draw_texture_rect(self.background,
                                 arcade.LBWH(0, 0, self.width, self.height))

        for text in self.text_list:
            text.draw()

        self.instruction.draw()

    def on_show_view(self) -> None:
        """Reload the leaderboard content each time the view is shown."""
        self.text_list.clear()
        self.leaderboard()
