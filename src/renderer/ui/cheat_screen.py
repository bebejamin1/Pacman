

import os
import arcade

from src.engine.game import Game, Cheats

# ----| CONSTANTS |---- #
PATH = "assets/background/"
MUSIC_PATH = "assets/sound/"
# --------------------- #


class CheatView(arcade.View):
    """
    This class manages the pause menu.
    """
    def __init__(self) -> None:
        super().__init__()
        self.button_list: arcade.SpriteList[arcade.Sprite] = \
            arcade.SpriteList()
        self.game: Game = self.window.game
        self.cheats: Cheats = self.window.cheats

        self._load()

    def on_key_press(self, key: int, _modifiers: int) -> None:
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.menu_view)

        if key == arcade.key.SPACE:
            self.window.show_view(self.window.game_view)

    def on_mouse_press(self, x: float, y: float, button: int,
                       _modifiers: int) -> None:
        hit = arcade.get_sprites_at_point((x, y), self.button_list)

        for sprite in hit:
            if sprite == self.invincible:
                arcade.play_sound(self.effect)

                if self.cheats.invincible is False:
                    self.cheats.invincible = True

                else:
                    self.cheats.invincible = False

                print("Invicibility activated")

            if sprite == self.skip:
                arcade.play_sound(self.effect)

                self.game.skip_level()

                print("Skipping level")

            if sprite == self.stop_ghost:
                arcade.play_sound(self.effect)

                if self.cheats.freeze_ghosts is False:
                    self.cheats.freeze_ghosts = True

                else:
                    self.cheats.freeze_ghosts = False

                print("Stopping the ghosts")

            if sprite == self.more_lives:
                arcade.play_sound(self.effect)

                self.game.add_life()

                print("Adds a life")

            if sprite == self.more_speed:
                arcade.play_sound(self.effect)

                if self.cheats.speed_boost is False:
                    self.cheats.speed_boost = True

                else:
                    self.cheats.speed_boost = False

                print("Adds speed")

            if sprite == self.resume:
                arcade.play_sound(self.effect)

                self.window.switch_game()

                print("Resume Game")

    def on_draw(self) -> None:
        self.clear()

        # Draws the background
        arcade.draw_texture_rect(self.background, arcade.LBWH(0, 0,
                                                              self.width,
                                                              self.height))

        # Draws a semi-opaque black layer on the screen
        arcade.draw_rect_filled(arcade.XYWH(self.width / 2,
                                            self.height / 2,
                                            self.width,
                                            self.height),
                                (0, 0, 0, 128))

        # Buttons' placement
        self.invincible.center_x = self.width / 2
        self.invincible.center_y = self.height - 250

        self.skip.center_x = self.width / 2
        self.skip.center_y = self.height - 375

        self.stop_ghost.center_x = self.width / 2
        self.stop_ghost.center_y = self.height - 500

        self.more_lives.center_x = self.width / 2
        self.more_lives.center_y = self.height - 625

        self.more_speed.center_x = self.width / 2
        self.more_speed.center_y = self.height - 750

        self.resume.center_x = self.width / 2
        self.resume.center_y = self.height - 875

        # Draws text
        self.cheat.draw()

        # Draws the buttons
        self.button_list.draw()

    def _load_text(self) -> None:
        self.cheat = arcade.Text(
            text="CHEATS",
            x=self.width / 2,
            y=self.height - 150,
            color=arcade.color.LAVENDER,
            font_size=60,
            anchor_x="center",
            font_name="Public Pixel"
                                )

        self.invincible = arcade.create_text_sprite(
            text="Invincibility",
            color=arcade.color.LAVENDER,
            font_size=40,
            font_name="Public Pixel"
                                                   )

        self.skip = arcade.create_text_sprite(
            text="Skip Level",
            color=arcade.color.LAVENDER,
            font_size=40,
            font_name="Public Pixel"
                                             )

        self.stop_ghost = arcade.create_text_sprite(
            text="Stop Ghosts",
            color=arcade.color.LAVENDER,
            font_size=40,
            font_name="Public Pixel"
                                                   )

        self.more_lives = arcade.create_text_sprite(
            text="Add a life",
            color=arcade.color.LAVENDER,
            font_size=40,
            font_name="Public Pixel"
                                                   )

        self.more_speed = arcade.create_text_sprite(
            text="Add Speed",
            color=arcade.color.LAVENDER,
            font_size=40,
            font_name="Public Pixel"
                                                   )

        self.resume = arcade.create_text_sprite(
            text="Resume Game",
            color=arcade.color.LAVENDER,
            font_size=40,
            font_name="Public Pixel"
                                               )

        # Appends the buttons on a list
        self.button_list.append(self.invincible)
        self.button_list.append(self.skip)
        self.button_list.append(self.stop_ghost)
        self.button_list.append(self.more_lives)
        self.button_list.append(self.more_speed)
        self.button_list.append(self.resume)

    def _load(self) -> None:
        try:
            if not os.path.exists("assets/"):
                raise ValueError

            # Loads the background
            self.background: arcade.Texture = \
                arcade.load_texture(f"{PATH}maze_back.png")

            # Loads the music and effect
            self.effect = arcade.load_sound(f"{MUSIC_PATH}effect/select.mp3")

            # Loads the text
            self._load_text()

        except FileNotFoundError:
            raise ValueError("\033[1;91massets folder not found!\033[0m")
