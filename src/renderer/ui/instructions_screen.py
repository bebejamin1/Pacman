import os
import arcade

from arcade.gui import UIManager, UITextArea

# ----| CONSTANTS |---- #
PATH = "assets/menu/main/"
MUSIC_PATH = "assets/sound/"

INSTRUCTIONS = "Test\nnew-line"
# --------------------- #

class InstructionsView(arcade.View):
    """
    This class will display the game's control and instructions.
    """
    def __init__(self) -> None:
        super().__init__()
        from src.renderer.game_engine import GameEngine
        self.window = GameEngine()
        # self.text_list = []
        
        # Loads the background
        try:
            if not os.path.exists("assets/"):
                raise ValueError

            self.background: arcade.Texture
            self.background = arcade.load_texture(f"{PATH}main_menu.png")
        except FileNotFoundError:
                raise ValueError("\033[1;91mBackground file not found!\033[0m")

        # text = UITextArea(x=100, y=200, width=SCREEN_WIDTH / 2,
        #                   height=SCREEN_HEIGHT / 2, text=INSTRUCTIONS,
        #                   text_color=(0, 0, 0, 255))

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            self.window.switch_menu()

    def on_draw(self) -> None:
        self.clear()

        # Draws the background
        arcade.draw_texture_rect(self.background, 
                                 arcade.LBWH(0, 0, self.width, self.height))

        # Prints a scrollable text
        # self.text_list.draw()
