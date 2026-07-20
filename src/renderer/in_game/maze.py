import arcade

from typing import Any

from mazegen.mazegenerator.mazegenerator import MazeGenerator

from src.engine.game import Game
from src.renderer.in_game.sprite import Object

# ----| CONSTANTS |---- #
PATH = "assets/maze/"

WALL = f"{PATH}front_wall.png"
GROUND = f"{PATH}ground.png"

LS_WALL = f"{PATH}ls_wall.png"
RS_WALL = f"{PATH}rs_wall.png"

TL_CORNER = f"{PATH}tl_corner_wall.png"
TR_CORNER = f"{PATH}tr_corner_wall.png"
BL_CORNER = f"{PATH}bl_corner_wall.png"
BR_CORNER = f"{PATH}br_corner_wall.png"

SPRITE_SIZE = 32
CHARACTER_SIZE = 1
CHARACTER_SPEED = 2

OFFSET_X = 2 * SPRITE_SIZE
OFFSET_Y = 2 * SPRITE_SIZE
# --------------------- #


class Maze():
    def __init__(self, config: dict[str, Any], lvl: int,
                 game: Game, width: int, height: int) -> None:
        self.config = config
        self.lvl = lvl
        self.width = width
        self.height = height

        self.levels: list[dict[str, Any]] = self.config["level"]

        self.seed: int = self.config["seed"]

        self.lvl_width: int = self.levels[self.lvl]["width"]
        self.lvl_height: int = self.levels[self.lvl]["height"]

        self.wall_list: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        self.ground_list: arcade.SpriteList[arcade.Sprite] = \
            arcade.SpriteList()

        self.maze_grid: list[list[int]] = MazeGenerator(size=(self.lvl_width,
                                                              self.lvl_height),
                                                        perfect=False,
                                                        seed=self.seed).maze

    def generate_maze(self, game: Game) -> None:
        level = game.level
        maze_width = 0
        maze_height = 0

        for x in range(self.lvl_height):
            for y in range(self.lvl_width):
                cell = level.maze[x][y]
                screen_x = y * 2
                screen_y = x * 2

                if maze_width < screen_x:
                    maze_width = screen_x
                if maze_height < screen_y:
                    maze_height = screen_y

                if cell & 1:
                    self._build_walls(screen_x, screen_y - 1, WALL)
                if cell & 2:
                    self._build_walls(screen_x + 1, screen_y, WALL)
                if cell & 4:
                    self._build_walls(screen_x, screen_y + 1, WALL)
                if cell & 8:
                    self._build_walls(screen_x - 1, screen_y, WALL)

                self._build_walls(screen_x - 1, screen_y - 1, WALL)
                self._build_walls(screen_x - 1, screen_y + 1, WALL)
                self._build_walls(screen_x + 1, screen_y + 1, WALL)
                self._build_walls(screen_x + 1, screen_y - 1, WALL)

    def _build_walls(self, x: float, y: float, wall: str) -> None:
        try:
            front_wall = Object(wall, 1)
        except FileNotFoundError:
            raise ValueError("\033[1;91mError: wall asset not found\033[0m")
        front_wall.center_x = x * SPRITE_SIZE + (SPRITE_SIZE / 2) + OFFSET_X
        front_wall.center_y = ((self.height - 100) - (y * SPRITE_SIZE) -
                               (SPRITE_SIZE / 2) + OFFSET_Y)
        self.wall_list.append(front_wall)
