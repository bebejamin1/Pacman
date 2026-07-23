import arcade

from typing import Any

from src.renderer.in_game.characters import Character
from src.renderer.in_game.sprite import Object

# ----| CONSTANTS |---- #
PATH = "assets/maze/"
PATH_PAC = "assets/collectibles/"
PLAYER_PATH = "assets/player/"

PACGUM = f"{PATH_PAC}pacgum.png"
SUPER_PAC = f"{PATH_PAC}super_pacgum.png"

WALL = f"{PATH}front_wall.png"
GROUND = f"{PATH}ground.png"

LS_WALL = f"{PATH}ls_wall.png"
RS_WALL = f"{PATH}rs_wall.png"

TL_CORNER = f"{PATH}tl_corner_wall.png"
TR_CORNER = f"{PATH}tr_corner_wall.png"
BL_CORNER = f"{PATH}bl_corner_wall.png"
BR_CORNER = f"{PATH}br_corner_wall.png"

SPRITE_SIZE = 32 * 2
CHARACTER_SIZE = 0.65
# --------------------- #


class Maze():
    def __init__(self, config: dict[str, Any], lvl_nb: int,
                 lvl_info: list[list[int]],
                 width: float, height: float) -> None:
        self.config: dict[str, Any] = config
        self.lvl_nb: int = lvl_nb
        self.lvl_info: list[list[int]] = lvl_info
        self.width: float = width
        self.height: float = height

        self.levels: list[dict[str, Any]] = self.config["level"]

        self.seed: int = self.config["seed"]

        self.lvl_width: int = self.levels[self.lvl_nb]["width"]
        self.lvl_height: int = self.levels[self.lvl_nb]["height"]

        self.offset_x: float = (SPRITE_SIZE / 2) * (self.lvl_width - 1)
        self.offset_y: float = ((self.height / 2) - 100 - (SPRITE_SIZE / 2)
                                * (self.lvl_height - 1))

        self.wall_list: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        self.ground_list: arcade.SpriteList[arcade.Sprite] = \
            arcade.SpriteList()
        self.pacgum_list: arcade.SpriteList[arcade.Sprite] = \
            arcade.SpriteList()
        self.super_pac: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        self.player_list: arcade.SpriteList[arcade.Sprite] = \
            arcade.SpriteList()
        self.enemies_list: arcade.SpriteList[arcade.Sprite] = \
            arcade.SpriteList()

    def generate_maze(self) -> None:
        level = self.lvl_info
        maze_width = self.lvl_width
        maze_height = self.lvl_height

        for x in range(self.lvl_height):
            for y in range(self.lvl_width):
                cell = level[x][y]
                screen_x = y * 2
                screen_y = x * 2

                if maze_width < screen_x:
                    maze_width = screen_x
                if maze_height < screen_y:
                    maze_height = screen_y

                if cell & 1:
                    self._build_walls(screen_x, screen_y - 1, WALL)
                if cell & 2:
                    self._build_walls(screen_x + 1, screen_y, LS_WALL)
                if cell & 4:
                    self._build_walls(screen_x, screen_y + 1, WALL)
                if cell & 8:
                    self._build_walls(screen_x - 1, screen_y, RS_WALL)

                self._build_walls(screen_x - 1, screen_y - 1, WALL)
                self._build_walls(screen_x - 1, screen_y + 1, WALL)
                self._build_walls(screen_x + 1, screen_y + 1, WALL)
                self._build_walls(screen_x + 1, screen_y - 1, WALL)

                if cell != 15:
                    if screen_x == 0 and screen_y == 0:
                        self._build_super_pacgum(screen_x, screen_y)

                    elif (screen_x == 0 and
                          screen_y == (self.lvl_height * 2 - 2)):
                        self._build_super_pacgum(screen_x, screen_y)

                    elif (screen_x == (self.lvl_width * 2 - 2) and
                          screen_y == 0):
                        self._build_super_pacgum(screen_x, screen_y)

                    elif (screen_x == (self.lvl_width * 2 - 2) and
                          screen_y == (self.lvl_height * 2 - 2)):
                        self._build_super_pacgum(screen_x, screen_y)

                    else:
                        self._build_pacgum(screen_x, screen_y)

                self._build_ground(screen_x, screen_y)
                self._build_ground(screen_x - 1, screen_y)
                self._build_ground(screen_x + 1, screen_y)
                self._build_ground(screen_x, screen_y - 1)
                self._build_ground(screen_x, screen_y + 1)
                self._build_ground(screen_x - 1, screen_y - 1)
                self._build_ground(screen_x - 1, screen_y + 1)
                self._build_ground(screen_x + 1, screen_y + 1)
                self._build_ground(screen_x + 1, screen_y - 1)

    def _build_walls(self, x: float, y: float, wall: str) -> None:
        try:
            front_wall = Object(wall, 1)

        except FileNotFoundError:
            raise ValueError("\033[1;91mError: wall asset not found\033[0m")

        front_wall.center_x = (x * SPRITE_SIZE + (self.width / 2) -
                               ((SPRITE_SIZE * 2 * (x / 2)) / 2) -
                               self.offset_x)
        front_wall.center_y = ((self.height - 100) - (y * SPRITE_SIZE) +
                               ((SPRITE_SIZE * 2 * (y / 2)) / 2) -
                               self.offset_y)

        self.wall_list.append(front_wall)

    def _build_ground(self, x: float, y: float) -> None:
        try:
            ground = Object(GROUND, 1)

        except FileNotFoundError:
            raise ValueError("\033[1;91mError: wall asset not"
                             " found\033[0m")

        ground.center_x = (x * SPRITE_SIZE + (self.width / 2) -
                           ((SPRITE_SIZE * 2 * (x / 2)) / 2) -
                           self.offset_x)
        ground.center_y = ((self.height - 100) - (y * SPRITE_SIZE) +
                           ((SPRITE_SIZE * 2 * (y / 2)) / 2) -
                           self.offset_y)

        self.ground_list.append(ground)

    def _build_pacgum(self, x: float, y: float) -> None:
        try:
            pacgum = Object(PACGUM, 0.5)

        except FileNotFoundError:
            raise ValueError("\033[1;91mError: wall asset not"
                             " found\033[0m")

        pacgum.center_x = (x * SPRITE_SIZE + (self.width / 2) -
                           ((SPRITE_SIZE * 2 * (x / 2)) / 2) -
                           self.offset_x)
        pacgum.center_y = ((self.height - 100) - (y * SPRITE_SIZE) +
                           ((SPRITE_SIZE * 2 * (y / 2)) / 2) -
                           self.offset_y)

        self.pacgum_list.append(pacgum)

    def _build_super_pacgum(self, x: float, y: float) -> None:
        try:
            pacgum = Object(SUPER_PAC, 1)

        except FileNotFoundError:
            raise ValueError("\033[1;91mError: wall asset not"
                             " found\033[0m")

        pacgum.center_x = (x * SPRITE_SIZE + (self.width / 2) -
                           ((SPRITE_SIZE * 2 * (x / 2)) / 2) -
                           self.offset_x)
        pacgum.center_y = ((self.height - 100) - (y * SPRITE_SIZE) +
                           ((SPRITE_SIZE * 2 * (y / 2)) / 2) -
                           self.offset_y)

        self.super_pac.append(pacgum)

    def _load_player(self) -> None:
        try:
            char_walk_anim = [
                arcade.load_texture(f"{PLAYER_PATH}/walk/walk1.png"),
                arcade.load_texture(f"{PLAYER_PATH}/walk/walk2.png"),
                arcade.load_texture(f"{PLAYER_PATH}/walk/walk3.png"),
                arcade.load_texture(f"{PLAYER_PATH}/walk/walk4.png"),
                arcade.load_texture(f"{PLAYER_PATH}/walk/walk5.png"),
                arcade.load_texture(f"{PLAYER_PATH}/walk/walk6.png"),
                arcade.load_texture(f"{PLAYER_PATH}/walk/walk7.png"),
                arcade.load_texture(f"{PLAYER_PATH}/walk/walk8.png"),
                arcade.load_texture(f"{PLAYER_PATH}/walk/walk9.png"),
                arcade.load_texture(f"{PLAYER_PATH}/walk/walk10.png"),
                arcade.load_texture(f"{PLAYER_PATH}/walk/walk11.png"),
                arcade.load_texture(f"{PLAYER_PATH}/walk/walk12.png"),
            ]

        except FileNotFoundError:
            raise ValueError("\033[1;91mError: Assets folder not found\033[0m")

        self.player = Character(f"{PLAYER_PATH}/walk/walk1.png",
                                CHARACTER_SIZE / 2, char_walk_anim)

        self.player.center_x = self.width / 2
        self.player.center_y = self.height / 2

        self.player_list.append(self.player)

    # def _load_enemy(self) -> None:
    #     try:
    #         enemy_walk_anim = [
    #             arcade.load_texture(f"{PLAYER_PATH}/walk/walk1.png"),
    #             arcade.load_texture(f"{PLAYER_PATH}/walk/walk2.png"),
    #             arcade.load_texture(f"{PLAYER_PATH}/walk/walk3.png"),
    #         ]

    #     except FileNotFoundError:
    #         raise ValueError("\033[1;91mError: Assets folder not found\033[0m")

    #     self.enemy = Character(f"{PLAYER_PATH}/walk/walk1.png",
    #                             CHARACTER_SIZE / 2, enemy_walk_anim)

    #     self.enemy.center_x = self.width / 2
    #     self.enemy.center_y = self.height / 2

    #     self.player_list.append(self.enemy)
