import arcade

from typing import Any

from mazegen.mazegenerator.mazegenerator import MazeGenerator

from src.engine.game import Game
from src.renderer.in_game.sprite import Object
from src.engine import Game  # noqa on peu le supprimer  ???

# ----| CONSTANTS |---- #
PITCH_X = 4
PITCH_Y = 2

PATH = "assets/maze/"

WALL = f"{PATH}front_wall.png",

LS_WALL = f"{PATH}ls_wall.png",
RS_WALL = f"{PATH}rs_wall.png",

TL_CORNER = f"{PATH}tl_corner_wall.png",
TR_CORNER = f"{PATH}tr_corner_wall.png",
BL_CORNER = f"{PATH}bl_corner_wall.png",
BR_CORNER = f"{PATH}br_corner_wall.png"
# --------------------- #


class Maze():
    def __init__(self, config: dict[str, Any], lvl: int, game: Game) -> None:
        self.config = config
        self.lvl = lvl

        self.levels: list[dict[str, Any]] = self.config.get("level")

        self.seed: int = self.config.get("seed")

        self.width: int = self.levels[self.lvl].get("width")
        self.height: int = self.levels[self.lvl].get("height")

        self.wall_list: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        self.ground_list: arcade.SpriteList[arcade.Sprite] = \
            arcade.SpriteList()

        self.maze_grid: list[list[int]] = MazeGenerator(size=(self.width,
                                                              self.height),
                                                        perfect=False,
                                                        seed=self.seed).maze

    def generate_maze(self, game: Game) -> list[str]:
        level = game.level
        for y in range(self.width):
            for x in range(self.height):
                cell = level.maze[y][x]
                ry, cx = y * PITCH_Y + 1, x * PITCH_X

                if cell == 15:
                    for i in range(PITCH_X + 1):
                        self._build_walls(cx + i, ry, WALL)

                if cell & 1:
                    for i in range(1, PITCH_X):
                        self._build_walls(cx + i, ry - 1, LS_WALL)

                if cell & 4:
                    for i in range(1, PITCH_X):
                        self._build_walls(cx + i, ry + 1, RS_WALL)

                if cell & 8:
                    self._build_walls(cx, ry, BL_CORNER)

                if cell & 2:
                    self._build_walls(cx + PITCH_X, ry, TR_CORNER)

    def _build_walls(self, x: float, y: float, wall: str) -> None:
        try:
            front_wall = Object(wall, 1)
        except FileNotFoundError:
            raise ValueError("\033[1;91mError: wall asset not found\033[0m")
        front_wall.center_x = x
        front_wall.center_y = y
        self.wall_list.append(wall)
