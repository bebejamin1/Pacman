
import curses
import locale
import time
from typing import Any

from mazegenerator import MazeGenerator
from src.engine import Game, GameState, GhostState, Mode, Rules
from src.parsing.parse_main import leaderbord_update, parser

SIZE = (15, 15)
TOTAL_LEVELS = 3
FIRST_LEVEL_SEED = 42
NAME_MAX = 10
FPS = 30

PITCH_X = 4
PITCH_Y = 2
WALL = "█"
PACGUM = "·"
SUPER = "●"

DIR_KEYS: dict[int, tuple[int, int]] = {
    curses.KEY_UP: (0, -1), ord("w"): (0, -1), ord("z"): (0, -1),
    curses.KEY_DOWN: (0, 1), ord("s"): (0, 1),
    curses.KEY_LEFT: (-1, 0), ord("a"): (-1, 0), ord("q"): (-1, 0),
    curses.KEY_RIGHT: (1, 0), ord("d"): (1, 0),
}

HELP_1 = "fleches/wasd/zqsd: bouger   p: pause   r: rejouer   echap: quitter"
HELP_2 = "1: invincible   2: freeze   3: vitesse   4: +vie   5: skip niveau"


# *****************************************************************************
# *                                 NEW MAZE                                  *
# *                                                                           *

def new_maze(size: tuple[int, int], seed: int = 0) -> list[list[int]]:
    maze: list[list[int]] = MazeGenerator(size=size, perfect=False,
                                          seed=seed).maze
    return maze


# *****************************************************************************
# *                                LEVEL SIZE                                 *
# *                                                                           *

def level_size(levels: list[dict[str, Any]], index: int) -> tuple[int, int]:
    if 0 <= index < len(levels):
        return (int(levels[index].get("width", SIZE[0])),
                int(levels[index].get("height", SIZE[1])))
    return SIZE


# *****************************************************************************
# *                                 NEW GAME                                  *
# *                                                                           *

def new_game(rules: Rules, levels: list[dict[str, Any]],
             first_seed: int) -> Game:
    total = len(levels) if levels else TOTAL_LEVELS
    first = new_maze(level_size(levels, 0), first_seed)
    return Game(rules, first, total)


# *****************************************************************************
# *                                BUILD WALLS                                *
# *                                                                           *

def build_walls(game: Game) -> list[str]:
    level = game.level
    w, h = level.width, level.height
    width, height = w * PITCH_X + 1, h * PITCH_Y + 1
    rows = [[" "] * width for _ in range(height)]
    for y in range(h):
        for x in range(w):
            cell = level.maze[y][x]
            ry, cx = y * PITCH_Y + 1, x * PITCH_X
            if cell == 15:
                for i in range(PITCH_X + 1):
                    rows[ry][cx + i] = WALL
            if cell & 1:
                for i in range(1, PITCH_X):
                    rows[ry - 1][cx + i] = WALL
            if cell & 4:
                for i in range(1, PITCH_X):
                    rows[ry + 1][cx + i] = WALL
            if cell & 8:
                rows[ry][cx] = WALL
            if cell & 2:
                rows[ry][cx + PITCH_X] = WALL
    for ry in range(0, height, PITCH_Y):
        for cx in range(0, width, PITCH_X):
            if ((ry > 0 and rows[ry - 1][cx] == WALL)
                    or (ry < height - 1 and rows[ry + 1][cx] == WALL)
                    or (cx > 0 and rows[ry][cx - 1] == WALL)
                    or (cx < width - 1 and rows[ry][cx + 1] == WALL)):
                rows[ry][cx] = WALL
    return ["".join(r) for r in rows]


# *****************************************************************************
# *                                   DRAW                                    *
# *                                                                           *

def draw(stdscr: "curses.window", game: Game, name: str,
         saved: bool, scores: list[dict[str, Any]]) -> None:
    stdscr.erase()
    ch = game.cheats
    level = game.level
    hud = (f"score: {game.score}   vies: {game.lives}   "
           f"niveau: {game.level_number}/{game.total_levels}   "
           f"temps: {int(game.time_left)}   mode: {game.mode.value}")
    flags = (f"cheats   invincible: {ch.invincible}   "
             f"freeze: {ch.freeze_ghosts}   vitesse: {ch.speed_boost}")
    top = 3
    try:
        stdscr.addstr(0, 0, hud)
        stdscr.addstr(1, 0, flags)
        for i, row in enumerate(build_walls(game)):
            stdscr.addstr(top + i, 0, row, curses.color_pair(4))
        for (x, y) in level.pacgums:
            stdscr.addstr(top + y * PITCH_Y + 1, x * PITCH_X + 2, PACGUM)
        for (x, y) in level.super_pacgums:
            stdscr.addstr(top + y * PITCH_Y + 1, x * PITCH_X + 2, SUPER,
                          curses.A_BOLD)
        for ghost in game.ghosts:
            if ghost.state is not GhostState.ACTIVE:
                continue
            pair = 3 if game.mode is Mode.FRIGHTENED else 2
            gx, gy = ghost.pos
            stdscr.addstr(top + gy * PITCH_Y + 1, gx * PITCH_X + 2, "G",
                          curses.color_pair(pair) | curses.A_BOLD)
        px, py = game.player.pos
        stdscr.addstr(top + py * PITCH_Y + 1, px * PITCH_X + 2, "C",
                      curses.color_pair(1) | curses.A_BOLD)
        if game.state is GameState.PAUSED:
            stdscr.addstr(top + 1, 4, " PAUSE ", curses.A_REVERSE)
        elif game.state in (GameState.GAME_OVER, GameState.VICTORY):
            title = ("VICTOIRE" if game.state is GameState.VICTORY
                     else "GAME OVER")
            stdscr.addstr(top + 1, 4, f" {title}   score: {game.score} ",
                          curses.A_REVERSE)
            if not saved:
                stdscr.addstr(top + 3, 4,
                              f" nom: {name}_   (entree: valider, "
                              "vide ou echap: passer) ", curses.A_REVERSE)
            else:
                stdscr.addstr(top + 3, 4,
                              " r: rejouer   echap: quitter ",
                              curses.A_REVERSE)
                for i, s in enumerate(scores[:5]):
                    line = (f" {i + 1}. {s['player_name']} - "
                            f"{s['player_score']} pts ")
                    stdscr.addstr(top + 5 + i, 4, line, curses.A_REVERSE)
        bottom = top + level.height * PITCH_Y + 2
        stdscr.addstr(bottom, 0, HELP_1)
        stdscr.addstr(bottom + 1, 0, HELP_2)
    except curses.error:
        pass
    stdscr.refresh()


# *****************************************************************************
# *                                HANDLE KEY                                 *
# *                                                                           *

def handle_key(game: Game, key: int, rules: Rules,
               levels: list[dict[str, Any]], first_seed: int) -> Game:
    if key in DIR_KEYS:
        game.set_player_direction(DIR_KEYS[key])
    elif key == ord("p"):
        game.toggle_pause()
    elif key == ord("r"):
        game = new_game(rules, levels, first_seed)
    elif key == ord("1"):
        game.cheats.invincible = not game.cheats.invincible
    elif key == ord("2"):
        game.cheats.freeze_ghosts = not game.cheats.freeze_ghosts
    elif key == ord("3"):
        game.cheats.speed_boost = not game.cheats.speed_boost
    elif key == ord("4"):
        game.add_life()
    elif key == ord("5"):
        game.skip_level()
    return game


# *****************************************************************************
# *                               HANDLE ENTRY                                *
# *                                                                           *

def handle_entry(name: str, key: int) -> tuple[str, bool]:
    if key in (curses.KEY_ENTER, 10, 13):
        return name, True
    if key in (curses.KEY_BACKSPACE, 127, 8):
        return name[:-1], False
    if 32 <= key < 127 and len(name) < NAME_MAX:
        char = chr(key)
        if char.isalnum() or char == " ":
            return name + char, False
    return name, False


# *****************************************************************************
# *                                    RUN                                    *
# *                                                                           *

def run(stdscr: "curses.window", scores: list[dict[str, Any]],
        rules: Rules, levels: list[dict[str, Any]],
        first_seed: int) -> None:
    curses.curs_set(0)
    stdscr.nodelay(True)
    if curses.has_colors():
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_YELLOW, -1)
        curses.init_pair(2, curses.COLOR_RED, -1)
        curses.init_pair(3, curses.COLOR_CYAN, -1)
        curses.init_pair(4, curses.COLOR_BLUE, -1)
    game = new_game(rules, levels, first_seed)
    name, saved = "", False
    last = time.monotonic()
    while True:
        entry = (game.state in (GameState.GAME_OVER, GameState.VICTORY)
                 and not saved)
        key = stdscr.getch()
        while key != -1:
            if entry:
                if key == 27:
                    saved, entry = True, False
                else:
                    name, done = handle_entry(name, key)
                    if done:
                        if name.strip():
                            scores = leaderbord_update(
                                name.strip(), game.score)["scores"]
                        saved, entry = True, False
            elif key in (27, ord("x")):
                return
            else:
                game = handle_key(game, key, rules, levels, first_seed)
                if key == ord("r"):
                    name, saved = "", False
            key = stdscr.getch()
        now = time.monotonic()
        game.update(now - last)
        last = now
        if game.state is GameState.LEVEL_WON:
            game.next_level(new_maze(level_size(levels, game.level_number)))
        draw(stdscr, game, name, saved, scores)
        time.sleep(1 / FPS)


# *****************************************************************************
# *                                   PLAY                                    *
# *                                                                           *

def play(conf_path: str) -> None:
    locale.setlocale(locale.LC_ALL, "")
    data = parser(conf_path)
    conf = data["conf"]
    scores: list[dict[str, Any]] = data["leadbord"]["scores"]
    rules = Rules.from_conf(conf)
    levels: list[dict[str, Any]] = conf.get("level", [])
    seed = conf.get("seed", FIRST_LEVEL_SEED)
    try:
        curses.wrapper(run, scores, rules, levels, seed)
    except curses.error:
        print("Erreur d'affichage: agrandis le terminal et relance.")


# *****************************************************************************
# *                                   MAIN                                    *
# *                                                                           *

def main() -> None:
    play("data/config.json")


if __name__ == "__main__":
    main()
