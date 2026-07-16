import os
import arcade

# ----| CONSTANTS |---- #
PATH = "assets/background/"
MUSIC_PATH = "assets/sound/"
# --------------------- #

class PauseView(arcade.View):
    """
    This class manages the pause menu.
    """
    def __init__(self):
        super().__init__()
        self.button_list: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()

        self._load()

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.menu_view)

        if key == arcade.key.SPACE:
            self.window.show_view(self.window.game_view)

    def on_mouse_press(self, x: float, y: float, button: int,
                       _modifiers: int) -> None:
        hit = arcade.get_sprites_at_point((x, y), self.button_list)

        for sprite in hit:
            if sprite == self.resume:
                arcade.play_sound(self.effect)
                self.window.switch_game()
                print("Resume Game")

            if sprite == self.menu:
                arcade.play_sound(self.effect)
                self.window.switch_menu()
                print("Return Menu")

    def on_draw(self):
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
        self.resume.center_x = self.width / 2
        self.resume.center_y =  self.height - 450

        self.menu.center_x = self.width / 2
        self.menu.center_y =  self.height - 600

        # Draws text
        self.pause.draw()

        # Draws the buttons
        self.button_list.draw()

    def _load_text(self) -> None:
        self.pause = arcade.Text(text="PAUSE",
                                 x=self.width / 2,
                                 y=self.height - 300,
                                 color=arcade.color.LAVENDER,
                                 font_size=60,
                                 anchor_x="center",
                                 font_name="Public Pixel")

        self.resume = arcade.create_text_sprite(text="Resume Game",
                                                color=arcade.color.LAVENDER,
                                                font_size=40,
                                                font_name="Public Pixel")

        self.menu = arcade.create_text_sprite(text="Return Menu",
                                              color=arcade.color.LAVENDER,
                                              font_size=40,
                                              font_name="Public Pixel")

        # Appends the buttons on a list
        self.button_list.append(self.resume)
        self.button_list.append(self.menu)

    def _load(self) -> None:
        try:
            if not os.path.exists("assets/"):
                raise ValueError

            # Loads the background
            self.background: arcade.Texture = \
                arcade.load_texture(f"{PATH}maze_back.png")

            # Loads the music and effect
            # self.music = arcade.load_sound(f"{MUSIC_PATH}music/menu.wav")
            self.effect = arcade.load_sound(f"{MUSIC_PATH}effect/select.mp3")

            # Loads the text
            self._load_text()

        except FileNotFoundError:
            raise ValueError("\033[1;91massets folder not found!\033[0m")