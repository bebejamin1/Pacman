import json
import os

rs = "\033[0m"
r = "\033[31m\033[5m\033[1m"


# *****************************************************************************
# *                             PARSE CONF                                    *
# *                                                                           *

def parse_conf(path: str) -> list:

    os.system("clear")

    checks = {
        "live": 2000, "pacgum_points": 2000, "super_pacgum_points": 2000,
        "ghost_points": 2000, "level_max_time": 2000
             }
    max_width = 30  # voir avec noemie
    max_height = 30  # voir avec noemie

    try:
        try:
            with open(path, "r") as f:
                conf = json.load(f)

        except FileNotFoundError:
            os.makedirs(path[:path.rfind("/")], exist_ok=True)
            with open(path, "w") as f:
                json.dump(default_conf, f, indent=2)
                conf = default_conf
    except Exception:
        print("\n" + f"{r}[ERROR]{rs}: The path to the config file "
              "is not accessible" + "\n")
        exit()

    try:
        if (len(conf) > 8):
            raise ValueError("The number of arguments in the JSON file "
                             "does not match")

        if not (conf.get("highscore_filename")):
            raise ValueError("highscore_filename It is required for the game")

        if (not conf["highscore_filename"].endswith(".json")):
            raise ValueError("The leaderboard must be in JSON format.")

        path_leaderbord = conf["highscore_filename"]

        if (not conf.get("seed") or len(conf.get("seed")) < 1):
            raise ValueError("The seed in the JSON conf is not set "
                             "up correctly.")

        for k, v in checks.items():

            if (not isinstance(k, int)):
                raise ValueError(f"The value of {k} must be an integer")

            if not (conf.get(k)):
                raise ValueError(f"The JSON config does not contain {k}")

            if (conf[k] <= 0 or conf[k] > v):
                raise ValueError(f"{k} must be > 0 and < {v}")

        if (not conf.get("level") or len(conf["level"]) < 10):
            raise ValueError("There must be at least 10 levels")

        for lvl, i in zip(conf.get("level"),
                          range(1, len(conf.get("level")) + 1)):

            if (not lvl.get("name") or
                    lvl.get("name")[lvl.get("name").find(" ") + 1:] != str(i)):
                raise ValueError("The level name must be present, "
                                 "and its number must be in ascending order.")

            if (not lvl.get("width") or not lvl.get("height") or
                    lvl["width"] <= 0 or lvl["width"] > max_width or
                    lvl["height"] <= 0 or lvl["height"] > max_height):
                raise ValueError("")

            if (len(lvl) != 3):
                raise ValueError("The parameters in `level` must be only "
                                 "`name`, `width`, and `height`.")

    except (ValueError, TypeError) as e:
        print("\n" + f"{r}[ERROR]{rs}:", e, "\n")
        exit()

    return [path_leaderbord, conf]


# *****************************************************************************
# *                          PARSE LEADERBORD                                 *
# *                                                                           *

def parse_leadbord(path: str) -> dict:
    pass


# *                              ASSETS                                       *

default_conf = {
    "highscore_filename": "data/leaderboard.json",
    "live": 3,
    "pacgum_points": 10,
    "super_pacgum_points": 50,
    "ghost_points": 200,
    "seed": "nono",
    "level_max_time": 180.0,
    "level": [
        {
            "name": "Level 1",
            "width": 12,
            "height": 10
        },
        {
            "name": "Level 2",
            "width": 18,
            "height": 12
        },
        {
            "name": "Level 3",
            "width": 10,
            "height": 10
        },
        {
            "name": "Level 4",
            "width": 10,
            "height": 20
        },
        {
            "name": "Level 5",
            "width": 15,
            "height": 21
        },
        {
            "name": "Level 6",
            "width": 14,
            "height": 10
        },
        {
            "name": "Level 7",
            "width": 15,
            "height": 10
        },
        {
            "name": "Level 8",
            "width": 12,
            "height": 16
        },
        {
            "name": "Level 9",
            "width": 14,
            "height": 10
        },
        {
            "name": "Level 10",
            "width": 20,
            "height": 20
        }
    ]
    }
