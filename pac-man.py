<<<<<<< HEAD


=======
>>>>>>> nono
# python3 pac-man.py config.json

import sys

rs = "\033[0m"
r = "\033[31m\033[5m\033[1m"
<<<<<<< HEAD
=======
g = "\033[32m\033[5m\033[1m"
>>>>>>> nono


def main() -> None:
    if (len(sys.argv) != 2):
        print("\n" + f"{r}[ERROR]{rs}: Execute using this structure:" + "\n"
              "python3 pac-man.py config.json" + "\n")
        return

    try:
<<<<<<< HEAD
        from src.visuel_place_holder.visual import play
=======
        # from src.visuel_place_holder.visual import play
        from src.renderer.game_engine import GameEngine
>>>>>>> nono
    except ModuleNotFoundError as e:
        print("\n" + f"{r}[ERROR]{rs}: missing dependency ({e.name})." + "\n"
              "Run `make install` then `uv run python pac-man.py "
              "config.json`" + "\n")
        return

<<<<<<< HEAD
    play(f"data/{sys.argv[1]}")


if __name__ == "__main__":
    main()
=======
    # play(f"data/{sys.argv[1]}")

    # Loads the game engine
    engine = GameEngine()
    engine.set_view()

    # Starts the game
    engine.run()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt):
        print(f"{g}[INFO]{rs}: Quitting Pacman!")
>>>>>>> nono
