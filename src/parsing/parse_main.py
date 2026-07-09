

import json

from src.parsing.parse import parse_conf, parse_leaderbord


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
        bord = json.load(f)

    bord["scores"].append({
        "player_name": player_name,
        "player_score": player_score
                          })

    bord["scores"].sort(key=lambda p: p["player_score"], reverse=True)
    bord = delete_over_ten(bord)
    with open(leaderbord_path, "w") as f:
        json.dump(bord, f, indent=2)

    return (bord)


# *****************************************************************************
# *                               PARSER                                      *
# *                                                                           *

def parser(conf_path: str) -> dict:
    conf = parse_conf(conf_path)
    leaderbord = parse_leaderbord(conf[0])

    global leaderbord_path

    leaderbord_path = conf[0]

    return {
        "conf": conf[1],
        "leadbord": delete_over_ten(leaderbord)
           }
