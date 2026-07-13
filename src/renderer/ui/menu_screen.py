import os
import arcade

from src.renderer.ui.buttons import StartButton, InstructionButton,\
                                    HighscoreButton, ExitButton

# ----| CONSTANTS |---- #
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "PAC-MAN by BN🍪"

PATH = "assets/menu/main/"
MUSIC_PATH = "assets/sound/"
# --------------------- #

class GameView(arcade.View):
    """
    This class will show the characters (player and enemies)
    animated sprites.
    """
    def __init__(self) -> None:
        super().__init__()
                         
        self.button_list: arcade.SpriteList[arcade.Sprite]
        self.button_list = arcade.SpriteList()
        self._load()
        self._play_music(self.music, 1.0, True)

    def create_buttons(self) -> None:
        self.start_button = StartButton(center_x=SCREEN_WIDTH,
                                        center_y=100,
                                        texture=self.s_button,
                                        view=self)
        self.button_list.append(self.start_button)

        self.instruction_button = InstructionButton(center_x=SCREEN_WIDTH // 4,
                                                    center_y=200,
                                                    texture=self.i_button,
                                                    view=self)
        self.button_list.append(self.instruction_button)

        self.highscore_button = HighscoreButton(center_x=SCREEN_WIDTH // 4,
                                                center_y=300,
                                                texture=self.h_button,
                                                view=self)
        self.button_list.append(self.highscore_button)

        self.exit_button = ExitButton(center_x=SCREEN_WIDTH // 4,
                                      center_y=400,
                                      texture=self.e_button,
                                      view=self)
        self.button_list.append(self.exit_button)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()

    def on_mouse_press(self, x: float, y: float, button: int,
                       _modifiers: int) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT:
            for button in self.button_list:
                arcade.play_sound(self.effect)
        

    def on_draw(self) -> None:
        self.clear()

        # Draws the background
        arcade.draw_texture_rect(self.background, 
                                 arcade.LBWH(0, 0, self.width, self.height))
        
        # Draws the buttons
        self.button_list.draw()

    def _load(self) -> None:
        try:
            if not os.path.exists("assets/"):
                raise ValueError

            # Loads the background
            self.background: arcade.Texture
            self.background = arcade.load_texture(f"{PATH}main_menu.png")

            # Loads the music and effect
            self.music = arcade.load_sound(f"{MUSIC_PATH}music/menu.wav")
            self.effect = arcade.load_sound(f"{MUSIC_PATH}effect/select.mp3")

            # Loads the buttons' sprites
            self.s_button = arcade.load_texture(f"{PATH}start.png")
            self.i_button = arcade.load_texture(f"{PATH}instructions.png")
            self.h_button = arcade.load_texture(f"{PATH}highscore.png")
            self.e_button = arcade.load_texture(f"{PATH}exit.png")


        except FileNotFoundError:
            raise ValueError("\033[1;91massets file not found!\033[0m")

    def _play_music(self, sound: str, volume: float,
                    loop: bool = False) -> None:
        arcade.play_sound(sound=self.music, loop=loop)


def start_game() -> None:
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE,
                           resizable=False, center_window=True,
                           antialiasing=True)
    game_view = GameView()
    window.show_view(game_view)
    arcade.run()
