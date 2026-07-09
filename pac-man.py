# python3 pac-man.py config.json

import sys

from src.parsing.parse_main import parser

rs = "\033[0m"
r = "\033[31m\033[5m\033[1m"


def main() -> None:
    try:
        if (len(sys.argv) != 2):
            raise ValueError("aled")
        parser(f"data/{sys.argv[1]}")

    except ValueError as e:
        print(f"{r}[ERROR]{rs}:", e)


if __name__ == "__main__":
    main()
