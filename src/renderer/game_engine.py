

import arcade

from typing import Any

from mazegen.mazegenerator.mazegenerator import MazeGenerator

from src.engine.game import Game, Rules, Cheats

from src.renderer.ui.menu_screen import MenuView
from src.renderer.ui.instructions_screen import InstructionsView
from src.renderer.ui.highscore_screen import HighscoreView
from src.renderer.game_mode import GameView
from src.renderer.ui.pause_screen import PauseView
from src.renderer.ui.end_screen import EndView
from src.renderer.ui.cheat_screen import CheatView

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
        super().__init__(
            width=SCREEN_WIDTH, height=SCREEN_HEIGHT,
            title=SCREEN_TITLE, resizable=False,
            center_window=True, antialiasing=True
                        )

        self.cheats: Cheats = Cheats()

    def set_view(self) -> None:
        self.menu_view = MenuView()
        self.instructions_view = InstructionsView()
        self.highscore_view = HighscoreView()
        self.game_view = GameView()
        self.pause_view = PauseView()
        self.cheat_view = CheatView()

    def switch_menu(self) -> None:
        # Goes on the main menu
        self.show_view(self.menu_view)

    def switch_instructions(self) -> None:
        # Goes on the instruction menu
        self.show_view(self.instructions_view)

    def switch_highscore(self) -> None:
        # Goes on the highscore menu
        self.show_view(self.highscore_view)

    def switch_game(self) -> None:
        # Goes on the game
        self.show_view(self.game_view)

    def switch_pause(self) -> None:
        # Goes on the pause menu
        self.show_view(self.pause_view)

    def switch_end(self, win: bool, score: int) -> None:
        # Goes on the end menu
        self.show_view(EndView(win, score))

    def switch_cheat(self) -> None:
        # Goes on the cheat menu
        self.show_view(self.cheat_view)

    def start_game(self) -> None:
        # Goes on the main menu by default
        self.switch_menu()
        arcade.run()

    def new_game(self, config: dict[str, Any],
                 levels: list[dict[str, Any]]) -> Game:
        lvl_width: int = levels[0]["width"]
        lvl_height: int = levels[0]["height"]
        seed: int = config["seed"]
        nb_levels = len(levels)

        self.first_maze: list[list[int]] = self.new_maze((lvl_width,
                                                          lvl_height),
                                                         seed)

        self.game: Game = Game(Rules.from_conf(config),
                               self.first_maze, nb_levels)

        return self.game

    def new_maze(self, size: tuple[int, int],
                 seed: int = 0) -> list[list[int]]:
        maze: list[list[int]] = MazeGenerator(size=size,
                                              perfect=False,
                                              seed=seed).maze
        return maze
