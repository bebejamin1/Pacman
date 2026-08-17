import os
import arcade

from src.parsing.parse_main import leaderbord_update

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.renderer.game_engine import GameEngine

PATH = "assets/background/"
MUSIC_PATH = "assets/sound/"


class EndView(arcade.View):
    """Game Over / Victory screen, with highscore name entry."""

    def __init__(self, window: "GameEngine", win: bool, score: int) -> None:
        """Prepare the end screen for a victory or a defeat.

        Args:
            window: Owning game window.
            win: Whether the game ended in a victory.
            score: Final score to display.
        """
        super().__init__()
        self.window: GameEngine = window
        self.button_list: arcade.SpriteList[arcade.Sprite] = \
            arcade.SpriteList()

        self.win: bool = win
        self.final_score: int = score
        self.player: str = ""

        self.full_name: list[arcade.Text] = []

        self._load()
        if self.win is True:
            self._load_victory()
        else:
            self._load_defeat()

    def on_key_press(self, key: int, _modifiers: int) -> None:
        """Handle the player's name entry and confirmation.

        Args:
            key: Key that was pressed.
            _modifiers: Active modifier keys (unused).
        """
        if key == arcade.key.ESCAPE:
            self.window.switch_menu()

        if len(self.player) < 10:
            if arcade.key.A <= key <= arcade.key.Z:
                self.player += chr(key)
                letter = arcade.Text(
                    text=self.player,
                    x=self.width // 2.72,
                    y=self.height - 800,
                    color=arcade.color.AIR_SUPERIORITY_BLUE,
                    font_size=30,
                    font_name="Public Pixel"
                                    )
                self.full_name.append(letter)

            if (arcade.key.NUM_0 <= key <= arcade.key.NUM_9
                    or arcade.key.KEY_0 <= key <= arcade.key.KEY_9):

                if key == arcade.key.NUM_0 or key == arcade.key.KEY_0:
                    self.player += "0"
                if key == arcade.key.NUM_1 or key == arcade.key.KEY_1:
                    self.player += "1"
                if key == arcade.key.NUM_2 or key == arcade.key.KEY_2:
                    self.player += "2"
                if key == arcade.key.NUM_3 or key == arcade.key.KEY_3:
                    self.player += "3"
                if key == arcade.key.NUM_4 or key == arcade.key.KEY_4:
                    self.player += "4"
                if key == arcade.key.NUM_5 or key == arcade.key.KEY_5:
                    self.player += "5"
                if key == arcade.key.NUM_6 or key == arcade.key.KEY_6:
                    self.player += "6"
                if key == arcade.key.NUM_7 or key == arcade.key.KEY_7:
                    self.player += "7"
                if key == arcade.key.NUM_8 or key == arcade.key.KEY_8:
                    self.player += "8"
                if key == arcade.key.NUM_9 or key == arcade.key.KEY_9:
                    self.player += "9"

                letter = arcade.Text(
                    text=self.player,
                    x=self.width // 2.72,
                    y=self.height - 800,
                    color=arcade.color.AIR_SUPERIORITY_BLUE,
                    font_size=30,
                    font_name="Public Pixel"
                                    )
                self.full_name.append(letter)

            if len(self.player) > 0:
                if key == arcade.key.SPACE:
                    self.player += chr(key)
                    letter = arcade.Text(
                        text=self.player,
                        x=self.width // 2.72,
                        y=self.height - 800,
                        color=arcade.color.AIR_SUPERIORITY_BLUE,
                        font_size=30,
                        font_name="Public Pixel"
                                        )
                    self.full_name.append(letter)

        if len(self.player) > 0:
            if key == arcade.key.BACKSPACE:
                self.player = self.player[:-1]
                if self.full_name:
                    self.full_name.pop()

            if key == arcade.key.ENTER:
                leaderbord_update(self.player, self.final_score)
                self.window.switch_menu()

    def on_draw(self) -> None:
        """Draw the background, result text and name entry."""
        self.clear()

        arcade.draw_texture_rect(self.background, arcade.LBWH(0, 0,
                                                              self.width,
                                                              self.height))

        arcade.draw_rect_filled(arcade.XYWH(self.width / 2,
                                            self.height / 2,
                                            self.width,
                                            self.height),
                                (0, 0, 0, 128))

        if self.win is True:
            self.victory.draw()
            self.congrat.draw()

        else:
            self.defeat.draw()
            self.looser.draw()

        self.score.draw()
        self.score_pts.draw()
        self.name.draw()

        for letter in self.full_name:
            letter.draw()

        self.name_entry.draw()

    def _load_victory(self) -> None:
        """Create the victory title and congratulation text."""
        self.victory = arcade.Text(
            text="Victory",
            x=self.width / 2,
            y=self.height - 200,
            color=arcade.color.LAVENDER,
            font_size=60,
            anchor_x="center",
            font_name="Public Pixel"
                                  )

        self.congrat = arcade.Text(
            text="Congratulation!",
            x=self.width / 2,
            y=self.height - 275,
            color=arcade.color.LAVENDER,
            font_size=30,
            anchor_x="center",
            font_name="Public Pixel"
                                  )

    def _load_defeat(self) -> None:
        """Create the game-over title and defeat text."""
        self.defeat = arcade.Text(
            text="Game Over",
            x=self.width / 2,
            y=self.height - 200,
            color=arcade.color.LAVENDER,
            font_size=60,
            anchor_x="center",
            font_name="Public Pixel"
                                 )

        self.looser = arcade.Text(
            text="Loser!",
            x=self.width / 2,
            y=self.height - 275,
            color=arcade.color.LAVENDER,
            font_size=30,
            anchor_x="center",
            font_name="Public Pixel"
                                 )

    def _load_text(self) -> None:
        """Create the score display and name entry text objects."""
        self.score = arcade.Text(
            text="Final Score:",
            x=self.width / 2,
            y=self.height - 450,
            color=arcade.color.LAVENDER,
            font_size=40,
            anchor_x="center",
            font_name="Public Pixel"
                                )

        self.score_pts = arcade.Text(
            text=f"{self.final_score}",
            x=self.width / 2,
            y=self.height - 575,
            color=arcade.color.AIR_SUPERIORITY_BLUE,
            font_size=50,
            anchor_x="center",
            font_name="Public Pixel"
                                    )

        self.name = arcade.Text(
            text="Enter Name:",
            x=self.width / 2,
            y=self.height - 700,
            color=arcade.color.LAVENDER,
            font_size=40,
            anchor_x="center",
            font_name="Public Pixel"
                               )

        self.name_entry = arcade.Text(
            text="__________",
            x=self.width / 2,
            y=self.height - 810,
            color=arcade.color.LAVENDER,
            font_size=30,
            anchor_x="center",
            font_name="Public Pixel"
                                     )

    def _load(self) -> None:
        """Load the end screen's background and text.

        Raises:
            ValueError: If the ``assets/`` folder is missing.
        """
        try:
            if not os.path.exists("assets/"):
                raise ValueError

            self.background: arcade.Texture = \
                arcade.load_texture(f"{PATH}finish.png")

            self._load_text()

        except FileNotFoundError:
            raise ValueError("\033[1;91massets folder not found!\033[0m")
