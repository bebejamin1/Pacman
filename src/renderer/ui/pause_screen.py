import os
import arcade

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.renderer.game_engine import GameEngine

PATH = "assets/background/"
MUSIC_PATH = "assets/sound/"


class PauseView(arcade.View):
    """Pause menu: resume the game or return to the main menu."""

    def __init__(self, window: "GameEngine") -> None:
        """Load the pause menu's background, sound and buttons.

        Args:
            window: Owning game window.
        """
        super().__init__()
        self.window: GameEngine = window
        self.button_list: arcade.SpriteList[arcade.Sprite] = \
            arcade.SpriteList()

        self._load()

    def on_key_press(self, key: int, _modifiers: int) -> None:
        """Resume the game or return to the main menu.

        Args:
            key: Key that was pressed.
            _modifiers: Active modifier keys (unused).
        """
        if key == arcade.key.ESCAPE:
            arcade.play_sound(self.effect)
            self.window.play_music(self.window.game_music, True, False)
            self.window.play_music(self.window.menu_music, True)
            self.window.show_view(self.window.menu_view)

        if key == arcade.key.SPACE:
            arcade.play_sound(self.effect)
            self.window.show_view(self.window.game_view)

    def on_mouse_press(self, x: float, y: float, button: int,
                       _modifiers: int) -> None:
        """Trigger the action of the button clicked with the mouse.

        Args:
            x: Cursor x coordinate.
            y: Cursor y coordinate.
            button: Mouse button that was pressed (unused).
            _modifiers: Active modifier keys (unused).
        """
        hit = arcade.get_sprites_at_point((x, y), self.button_list)

        for sprite in hit:
            if sprite == self.resume:
                arcade.play_sound(self.effect)
                self.window.switch_game(False)
                print("Resume Game")

            if sprite == self.menu:
                arcade.play_sound(self.effect)
                self.window.switch_menu()
                print("Return Menu")

    def on_draw(self) -> None:
        """Draw the background, buttons and pause title."""
        self.clear()

        arcade.draw_texture_rect(self.background, arcade.LBWH(0, 0,
                                                              self.width,
                                                              self.height))

        arcade.draw_rect_filled(arcade.XYWH(self.width / 2,
                                            self.height / 2,
                                            self.width,
                                            self.height),
                                (0, 0, 0, 128))

        self.resume.center_x = self.width / 2
        self.resume.center_y = self.height - 450

        self.menu.center_x = self.width / 2
        self.menu.center_y = self.height - 600

        self.pause.draw()

        self.button_list.draw()

    def _load_text(self) -> None:
        """Create the pause title and button text sprites."""
        self.pause = arcade.Text(
            text="PAUSE",
            x=self.width / 2,
            y=self.height - 300,
            color=arcade.color.LAVENDER,
            font_size=60,
            anchor_x="center",
            font_name="Public Pixel"
                               )

        self.resume = arcade.create_text_sprite(
            text="Resume Game",
            color=arcade.color.LAVENDER,
            font_size=40,
            font_name="Public Pixel"
                                               )

        self.menu = arcade.create_text_sprite(
            text="Return Menu",
            color=arcade.color.LAVENDER,
            font_size=40,
            font_name="Public Pixel"
                                             )

        self.button_list.append(self.resume)
        self.button_list.append(self.menu)

    def _load(self) -> None:
        """Load the pause menu's background, sound and text.

        Raises:
            ValueError: If the ``assets/`` folder is missing.
        """
        try:
            if not os.path.exists("assets/"):
                raise ValueError

            self.background: arcade.Texture = \
                arcade.load_texture(f"{PATH}maze_back.png")

            self.effect = arcade.load_sound(f"{MUSIC_PATH}effect/select.mp3")

            self._load_text()

        except FileNotFoundError:
            raise ValueError("\033[1;91massets folder not found!\033[0m")
