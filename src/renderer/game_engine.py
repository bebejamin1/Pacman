import arcade

from src.renderer.ui.menu_screen import MenuView
from src.renderer.ui.instructions_screen import InstructionsView
from src.renderer.ui.highscore_screen import HighscoreView
# from src.renderer.ui.game_screen import GameView
# from src.renderer.ui.pause_screen import PauseView
# from src.renderer.ui.end_screen import EndView

# ----| CONSTANTS |---- #
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "PAC-MAN by BN🍪"
# --------------------- #

class GameEngine(arcade.Window):
    """
    This class Orchestrate every views.
    """
    def __init__(self) -> None:
        super().__init__(width=SCREEN_WIDTH, height=SCREEN_HEIGHT,
                         title=SCREEN_TITLE, resizable=False, 
                         center_window=True, antialiasing=True)
        # self.width = SCREEN_WIDTH
        # self.height = SCREEN_HEIGHT
        # self.window = arcade.Window()
        # self.configured = False

    def set_view(self) -> None:
        self.menu_view = MenuView()
        self.instructions_view = InstructionsView()
        self.highscore_view = HighscoreView()
        # self.game_view = 
        # self.pause_view = 
        # self.end_view = 

        # self.switch_menu()

        # self.configured = True

    def switch_menu(self) -> None:
        self.show_view(self.menu_view)

    def switch_instructions(self) -> None:
        self.show_view(self.instructions_view)

    def switch_highscore(self) -> None:
        self.show_view(self.highscore_view)

    def run(self) -> None:
        # if self.configured is True:
        #     arcade.run()

        # Goes on the menu by default and run the game
        self.switch_menu()
        arcade.run()
