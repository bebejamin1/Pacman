import arcade

from src.renderer.ui.menu_screen import MenuView
from src.renderer.ui.instructions_screen import InstructionsView
from src.renderer.ui.highscore_screen import HighscoreView
from src.renderer.game_mode import GameView
from src.renderer.ui.pause_screen import PauseView
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

    def set_view(self) -> None:
        self.menu_view = MenuView()
        self.instructions_view = InstructionsView()
        self.highscore_view = HighscoreView()
        self.game_view = GameView()
        self.pause_view = PauseView()
        # self.end_view = EndView()

    def switch_menu(self) -> None:
        self.show_view(self.menu_view)

    def switch_instructions(self) -> None:
        self.show_view(self.instructions_view)

    def switch_highscore(self) -> None:
        self.show_view(self.highscore_view)

    def switch_game(self) -> None:
        self.show_view(self.game_view)

    def switch_pause(self) -> None:
        self.show_view(self.pause_view)

    # def switch_end(self) -> None:
    #     self.show_view(self.end_view)

    def run(self) -> None:
        # Goes on the menu by default and run the game
        self.switch_menu()
        arcade.run()
