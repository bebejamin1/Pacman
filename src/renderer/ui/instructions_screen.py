import os
import arcade

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.renderer.game_engine import GameEngine

PATH = "assets/background/"
FONT_PATH = "assets/font/"


class InstructionsView(arcade.View):
    """Displays the game's controls and rules."""

    def __init__(self, window: "GameEngine") -> None:
        """Load the instructions background and build the text objects.

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

        self.game_instructions()

    def game_instructions(self) -> None:
        """Build the controls and rules text objects."""
        commands = arcade.Text(text="Commands:", x=30, y=770,
                               color=arcade.color.BLACK, font_size=30,
                               align="left", font_name="Public Pixel")

        play = arcade.Text(text="- Play with WASD or the arrows", x=30,
                           y=700, color=arcade.color.BLACK, font_size=20,
                           align="left", font_name="Public Pixel")

        pause = arcade.Text(text="- Press SPACE to pause", x=30, y=650,
                            color=arcade.color.BLACK, font_size=20,
                            align="left", font_name="Public Pixel")

        quit = arcade.Text(text="- Press ESC to quit", x=30, y=600,
                           color=arcade.color.BLACK, font_size=20,
                           align="left", font_name="Public Pixel")

        self.text_list.append(commands)
        self.text_list.append(play)
        self.text_list.append(pause)
        self.text_list.append(quit)

        rules = arcade.Text(text="Rules:", x=30, y=530,
                            color=arcade.color.BLACK, font_size=28,
                            align="left", font_name="Public Pixel")

        rule1 = arcade.Text(text="- The Minotaur avoids humans", x=30,
                            y=460, color=arcade.color.BLACK, font_size=20,
                            align="left", font_name="Public Pixel")

        rule2 = arcade.Text(text="- Bones gives points", x=30, y=410,
                            color=arcade.color.BLACK, font_size=20,
                            align="left", font_name="Public Pixel")

        rule3 = arcade.Text(text="- Axes gives more points and", x=30,
                            y=360, color=arcade.color.BLACK, font_size=20,
                            align="left", font_name="Public Pixel")

        rule4 = arcade.Text(text="gives the ability to eat humans", x=30,
                            y=310, color=arcade.color.BLACK, font_size=20,
                            align="left", font_name="Public Pixel")

        self.text_list.append(rules)
        self.text_list.append(rule1)
        self.text_list.append(rule2)
        self.text_list.append(rule3)
        self.text_list.append(rule4)

        text = arcade.Text(text="Press ESCAPE to go back",
                           x=self.width / 2, y=100,
                           color=arcade.color.BRONZE,
                           font_size=10, anchor_x="center",
                           font_name="Public Pixel")

        self.text_list.append(text)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Return to the main menu.

        Args:
            symbol: Key that was pressed.
            modifiers: Active modifier keys (unused).
        """
        if symbol == arcade.key.ESCAPE:
            self.window.switch_menu()

    def on_draw(self) -> None:
        """Draw the background and the instructions text."""
        self.clear()

        arcade.draw_texture_rect(self.background,
                                 arcade.LBWH(0, 0, self.width, self.height))

        for text in self.text_list:
            text.draw()
