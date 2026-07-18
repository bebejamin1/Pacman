

import json
import os
import re

rs = "\033[0m"
r = "\033[31m\033[5m\033[1m"


# *****************************************************************************
# *                         STIP JSON COMMENTS                                *
# *                                                                           *

def strip_json_comments(text: str) -> str:
    pattern = r'"(?:\\.|[^"\\])*"|(//[^\n]*|#[^\n]*)'
    return re.sub(pattern, lambda m: "" if m.group(1) else m.group(0), text)


# *****************************************************************************
# *                             PARSE CONF                                    *
# *                                                                           *

def parse_conf(path: str) -> list:

<<<<<<< HEAD
    os.system("clear")
=======
    # os.system("clear")
>>>>>>> nono

    checks = {  # a voir avec noemie pour les maxs
        "live": 2000, "pacgum_points": 2000, "super_pacgum_points": 2000,
        "ghost_points": 2000, "level_max_time": 2000
             }
    min_width = 3  # voir avec noemie
    min_height = 3  # voir avec noemie
    max_width = 30  # voir avec noemie
    max_height = 30  # voir avec noemie

    try:
        try:
            with open(path, "r") as f:
                conf = json.loads(strip_json_comments(f.read()))

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

        if not (conf.get("highscore_filename")):
            raise ValueError("highscore_filename It is required for the game")

        path_leaderbord = conf["highscore_filename"]
        if (not isinstance(path_leaderbord, str) or
                not path_leaderbord.endswith(".json") or
                len(path_leaderbord) == 0):
            raise ValueError("The name of the leaderboard file is not "
                             "configured correctly")

        if (not isinstance(conf.get("seed"), int)
                or isinstance(conf.get("seed"), bool)
                or conf["seed"] <= 0):
            raise ValueError("The seed in the JSON conf is not set "
                             "up correctly.")

        for k, v in checks.items():

            if not (conf.get(k)):  # regarder si int
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
                    lvl["width"] <= min_width or lvl["width"] > max_width or
                    lvl["height"] <= min_height or lvl["height"] > max_height):
                raise ValueError("The maximum values must fall within the "
                                 "following ranges:" + "\n"
                                 f"width: > 0 and < {max_width}" + "\n"
                                 f"height: > 0 and < {max_height}")

    except (ValueError) as e:
        print("\n" + f"{r}[ERROR]{rs}: {e}" + "\n")
        with open(path, "w") as f:
            json.dump(default_conf, f, indent=2)
        conf = default_conf

    except TypeError as e:
        print("\n" + f"{r}[ERROR]{rs}:" +
              "The data types do not match" + "\n" + f"{e}")
        with open(path, "w") as f:
            json.dump(default_conf, f, indent=2)
        conf = default_conf

    return [path_leaderbord, conf]


# *****************************************************************************
# *                          PARSE LEADERBORD                                 *
# *                                                                           *

def parse_leaderbord(path: str) -> dict:
<<<<<<< HEAD
    leaderbord: dict
=======
>>>>>>> nono
    try:
        if not (path.endswith(".json")):
            raise ValueError("The leaderboard must be a .json file.")

        os.makedirs(path[:path.rfind("/")], exist_ok=True)
        if not (os.path.exists(path)):
            raise FileNotFoundError

        else:
            with open(path, "r") as f:
<<<<<<< HEAD
                leaderbord = json.loads(strip_json_comments(f.read()))
=======
                leaderbord: dict = json.loads(strip_json_comments(f.read()))
>>>>>>> nono

    except (FileNotFoundError, json.JSONDecodeError,
            ValueError, PermissionError):
        with open(path, "w") as f:
            json.dump(default_leaderbord, f, indent=2)
        leaderbord = default_leaderbord

    try:
        if (leaderbord.get("scores") is None or len(leaderbord) != 1):
            raise ValueError("The leaderboard should be prototyped as follows:"
                             "\n" + f"{default_leaderbord}")

        for p in leaderbord["scores"]:

            if (len(p) != 2 or
                    not p.get("player_name") or not p.get("player_score")):
                raise ValueError("The leaderboard JSON file must contain only"
                                 "\n" + "player_name: str," + "\n"
                                 "player_score: int")

            name = p["player_name"]
            if (len(name) > 10):
                error = ("The player's name must be less than "
                         "10 characters long and consist only of "
                         "alphanumeric and/or numeric characters, "
                         "including spaces. --> " + f"{name}")
                raise ValueError(error)

            for c in name:
                if not (c.isdigit() or c.isalpha() or c.isspace()):
                    raise ValueError(error)

            score = p["player_score"]
            if (score < 0 or score > 2147483647):
                raise ValueError("The score must be greater than 0 and must "
                                 "not exceed 2147483647.")

    except ValueError as e:
        print("\n" + f"{r}[ERROR]{rs}: {e}" + "\n")
        with open(path, "w") as f:
            json.dump(default_leaderbord, f, indent=2)
        leaderbord = default_leaderbord

    leaderbord["scores"].sort(key=lambda p: p["player_score"], reverse=True)
    with open(path, "w") as f:
        json.dump(leaderbord, f, indent=2)

    return (leaderbord)


# *                              ASSETS                                       *

default_leaderbord: dict[str, list] = {"scores": []}

default_conf = {
    "highscore_filename": "data/leaderboard.json",
    "live": 3,
    "pacgum_points": 10,
    "super_pacgum_points": 50,
    "ghost_points": 200,
    "seed": 42,
    "level_max_time": 90,
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
