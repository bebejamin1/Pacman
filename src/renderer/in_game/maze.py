import arcade

from typing import Any

from src.renderer.in_game.characters import Character
from src.engine.entities import Ghost
from src.renderer.in_game.sprite import Object

# ----| CONSTANTS |---- #
PATH = "assets/maze/"
PATH_PAC = "assets/collectibles/"
PLAYER_PATH = "assets/player/"
ENEMY_PATH = "assets/enemies/"

PACGUM = f"{PATH_PAC}pacgum.png"
SUPER_PAC = f"{PATH_PAC}super_pacgum.png"

WALL = f"{PATH}wall.png"
GROUND = f"{PATH}ground.png"

WALL_EDGE = f"{PATH}wall_w_edge.png"
SIDE_WALL = f"{PATH}side_wall.png"

TOP_CORNER = f"{PATH}top_corner.png"
BOT_CORNER = f"{PATH}bot_corner.png"
IN_CORNER = f"{PATH}corner_wall.png"
DEAD_END = f"{PATH}dead_end.png"

SPRITE_SIZE = 32 * 2
CHARACTER_SIZE = 0.6
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

        self.scale: float = self._find_scale()
        self.size: float = SPRITE_SIZE * self.scale

        self.offset_x: float = (self.size / 2) * (self.lvl_width - 1)
        self.offset_y: float = ((self.height / 2) - 100 - (self.size / 2)
                                * (self.lvl_height - 1))

        # Initialize the sprite lists
        self.wall_list: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        self.ground_list: arcade.SpriteList[arcade.Sprite] = \
            arcade.SpriteList()
        self.pacgum_list: arcade.SpriteList[arcade.Sprite] = \
            arcade.SpriteList()
        self.super_pac: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        self.player_list: arcade.SpriteList[arcade.Sprite] = \
            arcade.SpriteList()
        self.enemies: arcade.SpriteList[arcade.Sprite] = \
            arcade.SpriteList()

    def _clear_list(self) -> None:
        self.wall_list.clear()
        self.ground_list.clear()
        self.pacgum_list.clear()
        self.super_pac.clear()
        self.player_list.clear()
        self.enemies.clear()

    def generate_maze(self) -> None:
        self._clear_list()

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

                # Places the walls
                if cell & 1:
                    self._build_walls(screen_x, screen_y - 1, WALL, 0)
                if cell & 2:
                    self._build_walls(screen_x + 1, screen_y, WALL, 0)
                if cell & 4:
                    self._build_walls(screen_x, screen_y + 1, WALL, 0)
                if cell & 8:
                    self._build_walls(screen_x - 1, screen_y, WALL, 0)
                if cell == 15:
                    self._build_walls(screen_x, screen_y, WALL, 0)

                if y == 0:
                    self._build_walls(screen_x - 1, screen_y - 1,
                                      WALL, 0)
                else:
                    self._build_walls(screen_x - 1, screen_y - 1,
                                      WALL, 0)
                self._build_walls(screen_x - 1, screen_y + 1, WALL, 0)
                self._build_walls(screen_x + 1, screen_y + 1, WALL, 0)
                self._build_walls(screen_x + 1, screen_y - 1, WALL, 0)

                # Places the pacgums and super pacgums
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

                # Places the ground
                self._build_ground(screen_x, screen_y)
                self._build_ground(screen_x, screen_y - 1)
                self._build_ground(screen_x, screen_y + 1)

                if y != 0:
                    self._build_ground(screen_x - 1, screen_y)
                    self._build_ground(screen_x - 1, screen_y - 1)
                    self._build_ground(screen_x - 1, screen_y + 1)

                if y != self.lvl_height - 1:
                    self._build_ground(screen_x + 1, screen_y)
                    self._build_ground(screen_x + 1, screen_y - 1)
                    self._build_ground(screen_x + 1, screen_y + 1)

    def _build_walls(self, x: float, y: float,
                     wall: str, angle: float) -> None:
        try:
            front_wall = Object(wall, self.scale, angle)

        except FileNotFoundError:
            raise ValueError("\033[1;91mError: wall asset not found\033[0m")

        front_wall.center_x = (x * self.size + (self.width / 2) -
                               ((self.size * 2 * (x / 2)) / 2) -
                               self.offset_x)
        front_wall.center_y = ((self.height - 100) - (y * self.size) +
                               ((self.size * 2 * (y / 2)) / 2) -
                               self.offset_y)
        front_wall.angle = angle

        self.wall_list.append(front_wall)

    def _build_ground(self, x: float, y: float) -> None:
        try:
            ground = Object(GROUND, self.scale, 0)

        except FileNotFoundError:
            raise ValueError("\033[1;91mError: wall asset not"
                             " found\033[0m")

        ground.center_x = (x * self.size + (self.width / 2) -
                           ((self.size * 2 * (x / 2)) / 2) -
                           self.offset_x)
        ground.center_y = ((self.height - 100) - (y * self.size) +
                           ((self.size * 2 * (y / 2)) / 2) -
                           self.offset_y)

        self.ground_list.append(ground)

    def _build_pacgum(self, x: float, y: float) -> None:
        try:
            pacgum = Object(PACGUM, self.scale * 0.5, 0)

        except FileNotFoundError:
            raise ValueError("\033[1;91mError: wall asset not"
                             " found\033[0m")

        pacgum.center_x = (x * self.size + (self.width / 2) -
                           ((self.size * 2 * (x / 2)) / 2) -
                           self.offset_x)
        pacgum.center_y = ((self.height - 100) - (y * self.size) +
                           ((self.size * 2 * (y / 2)) / 2) -
                           self.offset_y)

        self.pacgum_list.append(pacgum)

    def _build_super_pacgum(self, x: float, y: float) -> None:
        try:
            pacgum = Object(SUPER_PAC, self.scale, 0)

        except FileNotFoundError:
            raise ValueError("\033[1;91mError: wall asset not"
                             " found\033[0m")

        pacgum.center_x = (x * self.size + (self.width / 2) -
                           ((self.size * 2 * (x / 2)) / 2) -
                           self.offset_x)
        pacgum.center_y = ((self.height - 100) - (y * self.size) +
                           ((self.size * 2 * (y / 2)) / 2) -
                           self.offset_y)

        self.super_pac.append(pacgum)

    def _load_entities(self) -> None:
        # Loads the player at its spawn-point
        self._load_player()

        # Loads the enemies at their spawn-point
        self._load_enemy(0, 0)
        self._load_enemy(0, (self.lvl_height * 2 - 2))
        self._load_enemy((self.lvl_width * 2 - 2), 0)
        self._load_enemy((self.lvl_width * 2 - 2), (self.lvl_height * 2 - 2))

    def _load_player(self) -> None:
        try:
            char_walk_anim = [
                arcade.load_texture(f"{PLAYER_PATH}walk/walk1.png"),
                arcade.load_texture(f"{PLAYER_PATH}walk/walk2.png"),
                arcade.load_texture(f"{PLAYER_PATH}walk/walk3.png"),
                arcade.load_texture(f"{PLAYER_PATH}walk/walk4.png"),
                arcade.load_texture(f"{PLAYER_PATH}walk/walk5.png"),
                arcade.load_texture(f"{PLAYER_PATH}walk/walk6.png"),
                arcade.load_texture(f"{PLAYER_PATH}walk/walk7.png"),
                arcade.load_texture(f"{PLAYER_PATH}walk/walk8.png"),
                arcade.load_texture(f"{PLAYER_PATH}walk/walk9.png"),
                arcade.load_texture(f"{PLAYER_PATH}walk/walk10.png"),
                arcade.load_texture(f"{PLAYER_PATH}walk/walk11.png"),
                arcade.load_texture(f"{PLAYER_PATH}walk/walk12.png"),
            ]

        except FileNotFoundError:
            raise ValueError("\033[1;91mError: Assets folder not found\033[0m")

        self.player = Character(f"{PLAYER_PATH}walk/walk1.png",
                                self.scale * (CHARACTER_SIZE / 2),
                                char_walk_anim)

        self.player.center_x = (self.lvl_width * self.size + (self.width / 2) -
                                ((self.size * 2 * (self.lvl_width / 2)) / 2) -
                                self.offset_x) - self.size
        self.player.center_y = ((self.height - 100) -
                                (self.lvl_height * self.size) +
                                ((self.size * 2 * (self.lvl_height / 2)) / 2)
                                - self.offset_y) + self.size / 2

        self.player_list.clear()
        self.player_list.append(self.player)

    def _load_enemy(self, x: float, y: float) -> None:
        try:
            enemy_walk_anim = [
                arcade.load_texture(f"{ENEMY_PATH}placeholder1.png"),
                arcade.load_texture(f"{ENEMY_PATH}placeholder2.png"),
                arcade.load_texture(f"{ENEMY_PATH}placeholder3.png"),
                arcade.load_texture(f"{ENEMY_PATH}placeholder4.png"),
            ]

        except FileNotFoundError:
            raise ValueError("\033[1;91mError: Assets folder not found\033[0m")

        self.enemy = Character(f"{ENEMY_PATH}placeholder1.png", self.scale,
                               enemy_walk_anim)

        self.enemy.center_x = (x * self.size + (self.width / 2) -
                               ((self.size * 2 * (x / 2)) / 2) -
                               self.offset_x)
        self.enemy.center_y = ((self.height - 100) - (y * self.size) +
                               ((self.size * 2 * (y / 2)) / 2) -
                               self.offset_y)

        self.enemies.append(self.enemy)

    def _find_scale(self) -> float:
        margin = 0.9

        maze_px_width = SPRITE_SIZE * (self.lvl_width + 1)
        maze_px_height = SPRITE_SIZE * (self.lvl_height + 1)

        available_width = self.width * margin
        available_height = (self.height - 100) * margin

        return min(available_width / maze_px_width,
                   available_height / maze_px_height)

    def _restart_level(self) -> None:
        # Player's respawn point
        self.player.center_x = (self.lvl_width * self.size + (self.width / 2) -
                                ((self.size * 2 * (self.lvl_width / 2)) / 2) -
                                self.offset_x) - self.size
        self.player.center_y = ((self.height - 100) -
                                (self.lvl_height * self.size) +
                                ((self.size * 2 * (self.lvl_height / 2)) / 2)
                                - self.offset_y) + self.size / 2

        # Ghosts' respawn
        self.enemy.center_x = (0 * self.size + (self.width / 2) -
                               ((self.size * 2 * (0 / 2)) / 2) -
                               self.offset_x)
        self.enemy.center_y = ((self.height - 100) - (0 * self.size) +
                               ((self.size * 2 * (0 / 2)) / 2) -
                               self.offset_y)

        self.enemy.center_x = (0 * self.size + (self.width / 2) -
                               ((self.size * 2 * (0 / 2)) / 2) -
                               self.offset_x)
        self.enemy.center_y = ((self.height - 100) - ((self.lvl_height * 2 - 2)
                                                      * self.size) +
                               ((self.size * 2 * ((self.lvl_height * 2 - 2)
                                                  / 2)) / 2) - self.offset_y)

        self.enemy.center_x = ((self.lvl_width * 2 - 2) * self.size
                               + (self.width / 2) -
                               ((self.size * 2 * ((self.lvl_width * 2 - 2)
                                                  / 2)) / 2) - self.offset_x)
        self.enemy.center_y = ((self.height - 100) - (0 * self.size) +
                               ((self.size * 2 * (0 / 2)) / 2) -
                               self.offset_y)

        self.enemy.center_x = ((self.lvl_width * 2 - 2) * self.size
                               + (self.width / 2) -
                               ((self.size * 2 * ((self.lvl_width * 2 - 2)
                                                  / 2)) / 2) - self.offset_x)
        self.enemy.center_y = ((self.height - 100) - ((self.lvl_height * 2 - 2)
                                                      * self.size) +
                               ((self.size * 2 * ((self.lvl_height * 2 - 2)
                                                  / 2)) / 2) - self.offset_y)
