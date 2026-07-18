

import json

from src.parsing.parse import parse_conf, parse_leaderbord, strip_json_comments

<<<<<<< HEAD
leaderbord_path: str = ""
=======
leaderbord_path = "data/leaderboard.json"
>>>>>>> nono


# *****************************************************************************
# *                           DELETE OVER TEN                                 *
# *                                                                           *

def delete_over_ten(leaderbord: dict) -> dict:

    if (len(leaderbord["scores"]) <= 10):
        return (leaderbord)

    new_bord = []
    for bord in leaderbord["scores"][:10]:
        new_bord.append(bord)

    with open(leaderbord_path, "w") as f:
        json.dump({"scores": new_bord}, f, indent=2)

    return {"scores": new_bord}


# *****************************************************************************
# *                             LEAD UPDATE                                   *
# *                                                                           *

def leaderbord_update(player_name: str, player_score: int) -> dict:

    with open(leaderbord_path, "r") as f:
        bord = json.loads(strip_json_comments(f.read()))

    bord["scores"].append({
        "player_name": player_name,
        "player_score": player_score
                          })
<<<<<<< HEAD
=======
    print(leaderbord_path)
>>>>>>> nono

    bord["scores"].sort(key=lambda p: p["player_score"], reverse=True)
    bord = delete_over_ten(bord)
    with open(leaderbord_path, "w") as f:
        json.dump(bord, f, indent=2)

    return (bord)


# *****************************************************************************
<<<<<<< HEAD
=======
# *                             LEAD EXTRACT                                  *
# *

def leaderboard_extract(pathfile: str) -> str:
    content = ""
    i = 1

    with open(pathfile, "r") as f:
        bord = json.loads(strip_json_comments(f.read()))

    for score, lst in bord.items():
        for dict in lst:
            if i < 10:
                content += f"{i}.  "
                f"{dict['player_name']}:\n{dict['player_score']}\n"
            else:
                content += f"{i}. "
                f"{dict['player_name']}:\n{dict['player_score']}\n"
            i += 1

    return content


# *****************************************************************************
>>>>>>> nono
# *                               PARSER                                      *
# *                                                                           *

def parser(conf_path: str) -> dict:
    conf = parse_conf(conf_path)
    leaderbord = parse_leaderbord(conf[0])

    global leaderbord_path

    leaderbord_path = conf[0]
<<<<<<< HEAD
=======
    print(leaderbord)
>>>>>>> nono

    return {
        "conf": conf[1],
        "leadbord": delete_over_ten(leaderbord)
           }
