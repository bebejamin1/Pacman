

import os
import arcade

# ----| CONSTANTS |---- #
PATH = "assets/menu/"
MUSIC_PATH = "assets/sound/"
BUTTON_PATH = "assets/menu/buttons/"
# --------------------- #


class MenuView(arcade.View):
    """
    This class will display the main menu.
    """
    def __init__(self) -> None:
        super().__init__()
        self.button_list: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList(
        )

        self._load()
        self._play_music(True)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            print("Bye bye!")
            arcade.close_window()

        # ---- debug end screen ---- #
        if symbol == arcade.key.V:
            self.window.switch_end()

    def on_mouse_press(self, x: float, y: float, button: int,
                       _modifiers: int) -> None:
        hit = arcade.get_sprites_at_point((x, y), self.button_list)

        for sprite in hit:
            if sprite == self.start:
                arcade.play_sound(self.effect)
                self.window.switch_game()
                print("Start Game!")

            if sprite == self.inst:
                arcade.play_sound(self.effect)
                self.window.switch_instructions()
                print("Instructions")

            if sprite == self.high:
                arcade.play_sound(self.effect)
                self.window.switch_highscore()
                print("Highscore")

            if sprite == self.exit:
                arcade.play_sound(self.effect)
                print("Here's a cookie 🍪, bye!")
                arcade.exit()

    def on_draw(self) -> None:
        self.clear()

        # Draws the background
        arcade.draw_texture_rect(self.background,
                                 arcade.LBWH(0, 0, self.width, self.height))

        # Buttons' placement
        self.start.center_x = self.window.width / 4
        self.start.center_y = self.window.height / 1.5

        self.inst.center_x = self.window.width / 3.05
        self.inst.center_y = self.window.height / 1.76

        self.high.center_x = self.window.width / 3.65
        self.high.center_y = self.window.height / 2.15

        self.exit.center_x = self.window.width / 8.47
        self.exit.center_y = self.window.height / 2.75

        # Draws the buttons
        self.button_list.draw()

    def _load(self) -> None:
        try:
            if not os.path.exists("assets/"):
                raise ValueError

            # Loads the background
            self.background: arcade.Texture = \
                arcade.load_texture(f"{PATH}main_menu.png")

            # Loads the music and effect
            self.music = arcade.load_sound(f"{MUSIC_PATH}music/menu.wav")
            self.effect = arcade.load_sound(f"{MUSIC_PATH}effect/select.mp3")

            # Loads the buttons' sprites and put them in a list
            self.start = arcade.Sprite(f"{BUTTON_PATH}start.png")
            self.inst = arcade.Sprite(f"{BUTTON_PATH}instructions.png")
            self.high = arcade.Sprite(f"{BUTTON_PATH}highscore.png")
            self.exit = arcade.Sprite(f"{BUTTON_PATH}exit.png")

            self.button_list.append(self.start)
            self.button_list.append(self.inst)
            self.button_list.append(self.high)
            self.button_list.append(self.exit)

        except FileNotFoundError:
            raise ValueError("\033[1;91massets folder not found!\033[0m")

    def _play_music(self, loop: bool = False) -> None:
        arcade.play_sound(sound=self.music, loop=loop)
