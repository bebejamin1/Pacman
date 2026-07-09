
from src.parsing.parse import parse_conf, parse_leadbord


def lead_update() -> None:
    pass


def parser(conf_path: str) -> dict:
    conf = parse_conf(conf_path)

    return {
        "conf": conf[1],
        "leadbord": parse_leadbord(conf[0])
           }
