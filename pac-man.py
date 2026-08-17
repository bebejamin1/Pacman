"""Entry point: python3 pac-man.py config.json"""

from src.parsing.parse_main import parser
from fire import Fire

import sys
import os

rs = "\033[0m"
r = "\033[31m\033[5m\033[1m"
g = "\033[32m\033[5m\033[1m"


def main(conf_path: str) -> None:
    """Parse the configuration file and launch the game window.

    Args:
        conf_path: Path to the JSON configuration file.
    """
    os.system("clear")

    parser(conf_path)

    if (len(sys.argv) != 2):
        print("\n" + f"{r}[ERROR]{rs}: Execute using this structure:" + "\n"
              "python3 pac-man.py config.json" + "\n")
        return

    try:
        from src.renderer.game_engine import GameEngine
    except ModuleNotFoundError as e:
        print("\n" + f"{r}[ERROR]{rs}: missing dependency ({e.name})." + "\n"
              "Run `make install` then `uv run python pac-man.py "
              "config.json`" + "\n")
        return

    engine = GameEngine()
    engine.set_view()

    engine.start_game()


if __name__ == "__main__":
    try:
        Fire(main)
    except (KeyboardInterrupt):
        print(f"\n{g}[INFO]{rs}: Quitting Pacman!")
