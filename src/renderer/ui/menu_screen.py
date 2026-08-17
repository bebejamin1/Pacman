

import os
import arcade

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.renderer.game_engine import GameEngine

# ----| CONSTANTS |---- #
PATH = "assets/background/"
MUSIC_PATH = "assets/sound/"
BUTTON_PATH = "assets/menu/"
# --------------------- #


class MenuView(arcade.View):
    """
    This class will display the main menu.
    """
    def __init__(self, window: "GameEngine") -> None:
        super().__init__()
        self.window: GameEngine = window
        self.button_list: arcade.SpriteList[arcade.Sprite] = \
            arcade.SpriteList()

        self._load()
        self.window.play_music(self.menu_music, True)
        self.button: int = 0

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            print("Bye bye!")
            arcade.exit()

        # Navigates through the menu using key arrows
        if symbol == arcade.key.UP:
            self.button -= 1
        if symbol == arcade.key.DOWN:
            self.button += 1

        if self.button < 0:
            self.button = 4
        if self.button == 5:
            self.button = 0

        if self.button == 0:
            self.click_exit.kill()
            self.click_start.kill()

        if self.button == 1:
            if self.click_start not in self.button_list:
                self.button_list.append(self.click_start)
            self.click_inst.kill()

        if self.button == 2:
            if self.click_inst not in self.button_list:
                self.button_list.append(self.click_inst)
            self.click_start.kill()
            self.click_high.kill()

        if self.button == 3:
            if self.click_high not in self.button_list:
                self.button_list.append(self.click_high)
            self.click_inst.kill()
            self.click_exit.kill()

        if self.button == 4:
            if self.click_exit not in self.button_list:
                self.button_list.append(self.click_exit)
            self.click_high.kill()

        if symbol == arcade.key.ENTER:
            if self.button == 1:
                arcade.play_sound(self.effect)
                self.window.switch_game(True)
                print("Start Game!")

            if self.button == 2:
                arcade.play_sound(self.effect)
                self.window.switch_instructions()
                print("Instructions")

            if self.button == 3:
                arcade.play_sound(self.effect)
                self.window.switch_highscore()
                print("Highscore")

            if self.button == 4:
                arcade.play_sound(self.effect)
                print("Here's a cookie 🍪, bye!")
                arcade.exit()

    def on_mouse_press(self, x: float, y: float, button: int,
                       _modifiers: int) -> None:
        hit = arcade.get_sprites_at_point((x, y), self.button_list)

        for sprite in hit:
            if sprite == self.start:
                arcade.play_sound(self.effect)
                self.window.switch_game(True)
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

        self.click_start.center_x = self.window.width / 4
        self.click_start.center_y = self.window.height / 1.5

        self.inst.center_x = self.window.width / 3.05
        self.inst.center_y = self.window.height / 1.76

        self.click_inst.center_x = self.window.width / 3.05
        self.click_inst.center_y = self.window.height / 1.76

        self.high.center_x = self.window.width / 3.65
        self.high.center_y = self.window.height / 2.15

        self.click_high.center_x = self.window.width / 3.65
        self.click_high.center_y = self.window.height / 2.15

        self.exit.center_x = self.window.width / 8.47
        self.exit.center_y = self.window.height / 2.75

        self.click_exit.center_x = self.window.width / 8.47
        self.click_exit.center_y = self.window.height / 2.75

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
            self.menu_music = arcade.load_sound(f"{MUSIC_PATH}music/menu.wav")
            self.game_music = arcade.load_sound(f"{MUSIC_PATH}music/game.mp3")
            self.effect = arcade.load_sound(f"{MUSIC_PATH}effect/select.mp3")

            # Loads the buttons' sprites and put them in a list
            self.start = arcade.Sprite(f"{BUTTON_PATH}start.png")
            self.inst = arcade.Sprite(f"{BUTTON_PATH}instructions.png")
            self.high = arcade.Sprite(f"{BUTTON_PATH}highscore.png")
            self.exit = arcade.Sprite(f"{BUTTON_PATH}exit.png")

            self.click_start = arcade.Sprite(f"{BUTTON_PATH}click_start.png")
            self.click_inst = arcade.Sprite(f"{BUTTON_PATH}click_instruc.png")
            self.click_high = arcade.Sprite(f"{BUTTON_PATH}click_highsc.png")
            self.click_exit = arcade.Sprite(f"{BUTTON_PATH}click_exit.png")

            self.button_list.append(self.start)
            self.button_list.append(self.inst)
            self.button_list.append(self.high)
            self.button_list.append(self.exit)

        except FileNotFoundError:
            raise ValueError("\033[1;91massets folder not found!\033[0m")
