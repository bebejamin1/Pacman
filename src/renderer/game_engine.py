import arcade

from src.renderer.ui.menu_screen import MenuView
from src.renderer.ui.instructions_screen import InstructionsView
# from src.renderer.ui.highscore_screen import HighscoreView
# from src.renderer.ui.game_screen import GameView
# from src.renderer.ui.pause_screen import PauseView
# from src.renderer.ui.end_screen import EndView

# ----| CONSTANTS |---- #
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "PAC-MAN by BN🍪"

PATH = "assets/menu/main/"
MUSIC_PATH = "assets/sound/"
# --------------------- #

class GameEngine:
    """
    This class Orchestrate every views.
    """
    def __init__(self) -> None:
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.window = arcade.Window(width=self.width, height=self.height,
                                    title=SCREEN_TITLE, resizable=False, 
                                    center_window=True, antialiasing=True)

    def set_view(self) -> None:
        self.menu_view = MenuView()
        self.instructions_view = InstructionsView()
        # self.highscore_view = HighscoreView()
        # self.game_view = 
        # self.pause_view = 
        # self.victory_view = 
        # self.game_over_view = 

    def switch_menu(self) -> None:
        self.window.show_view(self.menu_view)

    def switch_instructions(self) -> None:
        self.window.show_view(self.instructions_view)

    # def switch_highscore(self) -> None:
    #     self.window.show_view(self.highscore_view)

    def run(self) -> None:
        arcade.run()
