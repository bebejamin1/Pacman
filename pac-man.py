
# python3 pac-man.py config.json

import sys

from src.parsing.parse_main import parser, leaderbord_update

rs = "\033[0m"
r = "\033[31m\033[5m\033[1m"


def main() -> None:
    try:
        if (len(sys.argv) != 2):
            raise ValueError("Execute using this structure: " + "\n"
                             "python3 pac-man.py config.json")
    except ValueError as e:
        print("\n" + f"{r}[ERROR]{rs}: {e}" + "\n")

    parser(f"data/{sys.argv[1]}")
    # fonction pour ajouter un nouveau joueur au leaderbord
    leaderbord_update("testr", 2100)


if __name__ == "__main__":
    main()
