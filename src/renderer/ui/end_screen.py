import os
import arcade

# ----| CONSTANTS |---- #
PATH = "assets/background/"
MUSIC_PATH = "assets/sound/"
# --------------------- #

class EndView(arcade.View):
    """
    This class manages the finish screen (Game Over and Victory).
    """
    def __init__(self):
        super().__init__()
        self.button_list: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()

        self._load_victory()
        self._load_defeat()

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.menu_view)

    def on_mouse_press(self, x: float, y: float, button: int,
                       _modifiers: int) -> None:
        hit = arcade.get_sprites_at_point((x, y), self.button_list)

        for sprite in hit:
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

        # Draws text
        self.pause.draw()

        # Draws the buttons
        self.button_list.draw()

    def _load_victory(self) -> None:
        self.victory = arcade.Text(text="Victory",
                                   x=self.width / 2,
                                   y=self.height - 200,
                                   color=arcade.color.LAVENDER,
                                   font_size=60,
                                   anchor_x="center",
                                   font_name="Public Pixel")


        self.congrat = arcade.Text(text="Congratulation!",
                                   x=self.width / 2,
                                   y=self.height - 350,
                                   color=arcade.color.LAVENDER,
                                   font_size=40,
                                   font_name="Public Pixel")

    def _load_defeat(self) -> None:
        self.defeat = arcade.Text(text="Game Over",
                                  x=self.width / 2,
                                  y=self.height - 200,
                                  color=arcade.color.LAVENDER,
                                  font_size=60,
                                  anchor_x="center",
                                  font_name="Public Pixel")

        self.looser = arcade.Text(text="Looser!",
                                  x=self.width / 2,
                                  y=self.height - 350,
                                  color=arcade.color.LAVENDER,
                                  font_size=40,
                                  font_name="Public Pixel")

    def _load_text(self) -> None:
        self.score = arcade.Text(text="Final Score:",
                                 x=self.width / 2,
                                 y=self.height - 450,
                                 color=arcade.color.LAVENDER,
                                 font_size=40,
                                 anchor_x="center",
                                 font_name="Public Pixel")
        self.score_pts = arcade.Text(text="1561",
                                     x=self.width / 2,
                                     y=self.height - 500,
                                     color=arcade.color.LAVENDER,
                                     font_size=40,
                                     anchor_x="center",
                                     font_name="Public Pixel")

        self.name = arcade.Text(text="Enter Name:",
                                x=self.width / 2,
                                y=self.height - 650,
                                color=arcade.color.LAVENDER,
                                font_size=40,
                                anchor_x="center",
                                font_name="Public Pixel")
        self.name_entry = arcade.Text(text="__________",
                                      x=self.width / 2,
                                      y=self.height - 700,
                                      color=arcade.color.LAVENDER,
                                      font_size=40,
                                      anchor_x="center",
                                      font_name="Public Pixel")

    def _load(self) -> None:
        try:
            if not os.path.exists("assets/"):
                raise ValueError

            # Loads the background
            self.background: arcade.Texture = \
                arcade.load_texture(f"{PATH}maze_back.png")

            # Loads the music and effect
            # self.music = arcade.load_sound(f"{MUSIC_PATH}music/menu.wav")

            # Loads the text
            self._load_text()

        except FileNotFoundError:
            raise ValueError("\033[1;91massets folder not found!\033[0m")