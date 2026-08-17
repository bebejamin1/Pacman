import arcade

from typing import Any

from mazegenerator import MazeGenerator

from src.engine.game import Game, Rules, Cheats

from src.renderer.ui.menu_screen import MenuView
from src.renderer.ui.instructions_screen import InstructionsView
from src.renderer.ui.highscore_screen import HighscoreView
from src.renderer.game_mode import GameView
from src.renderer.ui.pause_screen import PauseView
from src.renderer.ui.end_screen import EndView
from src.renderer.ui.cheat_screen import CheatView

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "PAC-MAN by BN🍪"

MUSIC_PATH = "assets/sound/"


class GameEngine(arcade.Window):
    """Orchestrates every view and owns the shared window resources."""

    def __init__(self) -> None:
        """Create the game window and load the shared music tracks."""
        super().__init__(
            width=SCREEN_WIDTH, height=SCREEN_HEIGHT,
            title=SCREEN_TITLE, resizable=False,
            center_window=True, antialiasing=True
                        )

        self.cheats: Cheats = Cheats()

        self.menu_music = arcade.load_sound(f"{MUSIC_PATH}music/menu.wav")
        self.game_music = arcade.load_sound(f"{MUSIC_PATH}music/game.mp3")
        self.end_music = arcade.load_sound(f"{MUSIC_PATH}music/end.mp3")
        self.victory = arcade.load_sound(f"{MUSIC_PATH}effect/victory.mp3")
        self.lose = arcade.load_sound(f"{MUSIC_PATH}effect/lose.mp3")

    def set_view(self) -> None:
        """Instantiate every view of the game."""
        self.menu_view = MenuView(self)
        self.instructions_view = InstructionsView(self)
        self.highscore_view = HighscoreView(self)
        self.game_view = GameView(self)
        self.pause_view = PauseView(self)
        self.cheat_view = CheatView(self)

    def switch_menu(self) -> None:
        """Show the main menu and play its music."""
        self.play_music(self.end_music, True, False)
        self.play_music(self.game_music, True, False)

        self.show_view(self.menu_view)

        self.play_music(self.menu_music, True)

    def switch_instructions(self) -> None:
        """Show the instructions view."""
        self.show_view(self.instructions_view)

    def switch_highscore(self) -> None:
        """Show the highscore view."""
        self.show_view(self.highscore_view)

    def switch_game(self, restart: bool) -> None:
        """Show the game view, optionally restarting from level one.

        Args:
            restart: Whether to reset the game view to its first level.
        """
        self.play_music(self.menu_music, True, False)

        if restart is True:
            lvl_nb: int = 0
            self.game_view.setup(lvl_nb)

        self.show_view(self.game_view)
        self.play_music(self.game_music, True)

    def switch_pause(self) -> None:
        """Show the pause view."""
        self.show_view(self.pause_view)

    def switch_end(self, win: bool, score: int) -> None:
        """Show the end view, with the matching victory or defeat sound.

        Args:
            win: Whether the game ended in a victory.
            score: Final score to display.
        """
        self.play_music(self.game_music, True, False)

        if win is True:
            self.play_music(self.victory, False, True)
        else:
            self.play_music(self.lose, False, True)

        self.show_view(EndView(self, win, score))

        self.play_music(self.end_music, True)

    def switch_cheat(self) -> None:
        """Show the cheat view."""
        self.show_view(self.cheat_view)

    def start_game(self) -> None:
        """Show the main menu and start the Arcade event loop."""
        self.switch_menu()
        arcade.run()

    def new_game(self, config: dict[str, Any],
                 levels: list[dict[str, Any]]) -> Game:
        """Generate the first maze and create the engine's ``Game`` state.

        Args:
            config: Parsed configuration dictionary.
            levels: List of per-level width/height/name dictionaries.

        Returns:
            The newly created ``Game`` instance.
        """
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
        """Generate a maze grid using the assigned A-Maze-ing package.

        Args:
            size: Maze size as a ``(width, height)`` tuple.
            seed: Seed for the maze generator. ``0`` requests a random
                maze, any strictly positive value a reproducible one.

        Returns:
            The generated wall-bitmask grid.
        """
        maze: list[list[int]] = MazeGenerator(size=size,
                                              perfect=False,
                                              seed=seed).maze
        return maze

    def play_music(self, music: arcade.Sound, loop: bool = False,
                   play: bool = True) -> None:
        """Play or stop a sound.

        Args:
            music: Sound to play or stop.
            loop: Whether the sound should loop when played.
            play: If True, play ``music``; if False, stop it.
        """
        if play is True:
            self.play = arcade.play_sound(sound=music, loop=loop)
        if play is False and self.play is not None:
            arcade.stop_sound(self.play)
