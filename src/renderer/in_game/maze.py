import arcade

from typing import Any
from random import random

from src.engine.algo import Cell, Personality
from src.engine.level import Level

from src.renderer.in_game.characters import Player, Enemies
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
PAC_CHANCE = 0.95
# --------------------- #


class Maze():
    def __init__(self, config: dict[str, Any], maze: list[list[int]],
                 lvl_nb: int, width: float, height: float) -> None:
        self.config: dict[str, Any] = config
        self.maze: list[list[int]] = maze
        self.width: float = width
        self.height: float = height

        self.level: Level = Level(self.maze, lvl_nb)
        self.game_levels: list[dict[str, Any]] = self.config["level"]

        self.seed: int = self.config["seed"]
        self.lvl_width: int = self.level.width
        self.lvl_height: int = self.level.height

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

        self.red_lst: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        self.orange_lst: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        self.cyan_lst: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        self.pink_lst: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()

    def _clear_list(self) -> None:
        self.wall_list.clear()
        self.ground_list.clear()

        self.pacgum_list.clear()
        self.super_pac.clear()

        self.player_list.clear()

        self.red_lst.clear()
        self.orange_lst.clear()
        self.cyan_lst.clear()
        self.pink_lst.clear()

    def generate_maze(self) -> None:
        self._clear_list()

        level = self.maze
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

                self._build_walls(screen_x - 1, screen_y - 1, WALL, 0)
                self._build_walls(screen_x - 1, screen_y + 1, WALL, 0)
                self._build_walls(screen_x + 1, screen_y + 1, WALL, 0)
                self._build_walls(screen_x + 1, screen_y - 1, WALL, 0)

                # Places the pacgums and super pacgums
                if cell != 15:
                    if screen_x == 0 and screen_y == 0:
                        self._build_super_pacgum((screen_x, screen_y))

                    elif (screen_x == 0 and
                          screen_y == (self.lvl_height * 2 - 2)):
                        self._build_super_pacgum((screen_x, screen_y))

                    elif (screen_x == (self.lvl_width * 2 - 2) and
                          screen_y == 0):
                        self._build_super_pacgum((screen_x, screen_y))

                    elif (screen_x == (self.lvl_width * 2 - 2) and
                          screen_y == (self.lvl_height * 2 - 2)):
                        self._build_super_pacgum((screen_x, screen_y))

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

        # "cell" est deja utilise plus haut pour un int (level[x][y]),
        # mypy voulait un tuple[int, int] ici -> renomme en "pac_cell"
        # for cell in self.level.pacgums:  # avant
        #     if random() <= PAC_CHANCE:  # avant
        #         self._build_pacgum(cell)  # avant
        for pac_cell in self.level.pacgums:  # apres
            if random() <= PAC_CHANCE:  # apres
                self._build_pacgum(pac_cell)  # apres

    # mypy: appele uniquement avec des int (screen_x/screen_y +-1)
    # def _build_walls(self, x: float, y: float,  # avant
    def _build_walls(self, x: int, y: int,  # apres
                     wall: str, angle: float) -> None:
        try:
            front_wall = Object(wall, self.scale, angle)

        except FileNotFoundError:
            raise ValueError("\033[1;91mError: wall asset not found\033[0m")

        new_x, new_y = self.convert_screen_coords((x, y))
        front_wall.center_x = new_x
        front_wall.center_y = new_y
        front_wall.angle = angle

        self.wall_list.append(front_wall)

    # def _build_ground(self, x: float, y: float) -> None:  # avant
    def _build_ground(self, x: int, y: int) -> None:  # apres
        try:
            ground = Object(GROUND, self.scale, 0)

        except FileNotFoundError:
            raise ValueError("\033[1;91mError: wall asset not"
                             " found\033[0m")

        new_x, new_y = self.convert_screen_coords((x, y))
        ground.center_x = new_x
        ground.center_y = new_y

        self.ground_list.append(ground)

    def _build_pacgum(self, cell: Cell) -> None:
        try:
            pacgum = Object(PACGUM, self.scale * 0.5, 0)

        except FileNotFoundError:
            raise ValueError("\033[1;91mError: wall asset not"
                             " found\033[0m")

        x, y = cell
        new_x, new_y = self.convert_screen_coords((x * 2, y * 2))
        pacgum.center_x = new_x
        pacgum.center_y = new_y

        self.pacgum_list.append(pacgum)

    def _build_super_pacgum(self, cell: Cell) -> None:
        try:
            sup_pacgum = Object(SUPER_PAC, self.scale, 0)

        except FileNotFoundError:
            raise ValueError("\033[1;91mError: wall asset not"
                             " found\033[0m")

        new_x, new_y = self.convert_screen_coords(cell)
        sup_pacgum.center_x = new_x
        sup_pacgum.center_y = new_y

        self.super_pac.append(sup_pacgum)

    def _load_entities(self) -> None:
        # Clears the entities lists
        self.player_list.clear()
        # self.enemies.clear()
        self.red_lst.clear()
        self.orange_lst.clear()
        self.cyan_lst.clear()
        self.pink_lst.clear()

        # Loads the player at its spawn-point
        self._load_player()

        # Loads the enemies at their spawn-point
        self._load_enemies()

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

        self.player = Player(f"{PLAYER_PATH}walk/walk1.png",
                             self.scale * (CHARACTER_SIZE / 2),
                             char_walk_anim)

        x, y = self.level.player_spawn
        new_x, new_y = self.convert_screen_coords((x * 2, y * 2))
        self.player.center_x = new_x
        self.player.center_y = new_y

        self.player_list.append(self.player)

    def _load_enemies(self) -> None:
        try:
            red_anim = [
                arcade.load_texture(f"{ENEMY_PATH}alive/red_ghost.png"),
            ]
            orange_anim = [
                arcade.load_texture(f"{ENEMY_PATH}alive/orange_ghost.png"),
            ]
            cyan_anim = [
                arcade.load_texture(f"{ENEMY_PATH}alive/cyan_ghost.png"),
            ]
            pink_anim = [
                arcade.load_texture(f"{ENEMY_PATH}alive/pink_ghost.png"),
            ]

        except FileNotFoundError:
            raise ValueError("\033[1;91mError: Assets folder not found\033[0m")

        # on donne cell et plus spawn pour que le fantome se libere de ses chaines  # noqa
        i: int = 0
        for cell in self.level.corners:
            x, y = cell
            new_x, new_y = self.convert_screen_coords((x * 2, y * 2))

            if i == 0:
                self.red = Enemies(f"{ENEMY_PATH}alive/red_ghost.png",
                                   self.scale / 1.5, red_anim,
                                   #  self.maze, Personality.CHASER, spawn)  # avant # noqa
                                   self.maze, Personality.CHASER, cell)  # apres  # noqa
                self.red.center_x = new_x
                self.red.center_y = new_y

            if i == 1:
                self.orange = Enemies(f"{ENEMY_PATH}alive/orange_ghost.png",
                                      self.scale / 1.5, orange_anim,
                                      #  self.maze, Personality.SHY, spawn)  # avant # noqa
                                      self.maze, Personality.SHY, cell)  # apres  # noqa
                self.orange.center_x = new_x
                self.orange.center_y = new_y

            if i == 2:
                self.cyan = Enemies(f"{ENEMY_PATH}alive/cyan_ghost.png",
                                    self.scale / 1.5, cyan_anim,
                                    #  self.maze, Personality.RANDOM, spawn)  # avant # noqa
                                    self.maze, Personality.RANDOM, cell)  # apres # noqa
                self.cyan.center_x = new_x
                self.cyan.center_y = new_y

            if i == 3:
                self.pink = Enemies(f"{ENEMY_PATH}alive/pink_ghost.png",
                                    self.scale / 1.5, pink_anim,
                                    #  self.maze, Personality.AMBUSHER, spawn)  # avant # noqa
                                    self.maze, Personality.AMBUSHER, cell)  # apres # noqa
                self.pink.center_x = new_x
                self.pink.center_y = new_y

            i += 1

        self.red_lst.append(self.red)
        self.orange_lst.append(self.orange)
        self.cyan_lst.append(self.cyan)
        self.pink_lst.append(self.pink)

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
        x, y = self.level.player_spawn
        nx, ny = self.convert_screen_coords((x * 2, y * 2))
        self.player.center_x = nx
        self.player.center_y = ny

        # Ghosts' respawn
        i: int = 0
        for cell in self.level.corners:
            x, y = cell
            nx, ny = self.convert_screen_coords((x * 2, y * 2))

            if i == 0:
                self.red.center_x = nx
                self.red.center_y = ny
                self.red.cell = cell
                self.red.brain.reset()

            if i == 1:
                self.orange.center_x = nx
                self.orange.center_y = ny
                self.orange.cell = cell
                self.orange.brain.reset()

            if i == 2:
                self.cyan.center_x = nx
                self.cyan.center_y = ny
                self.cyan.cell = cell
                self.cyan.brain.reset()

            if i == 3:
                self.pink.center_x = nx
                self.pink.center_y = ny
                self.pink.cell = cell
                self.pink.brain.reset()

            i += 1

    def convert_screen_coords(self, cell: Cell) -> Cell:
        x, y = cell

        nx = round(x * self.size + (self.width / 2) -
                   ((self.size * 2 * (x / 2)) / 2) - self.offset_x)
        ny = round((self.height - 100) - (y * self.size) +
                   ((self.size * 2 * (y / 2)) / 2) - self.offset_y)

        return (nx, ny)

    # les parenthese etait mal placer du coup le calcul etait un peu casser
    def convert_cell_coords(self, screen_x: int, screen_y: int) -> Cell:

        # nx = round(screen_x - (self.width / 2 - self.offset_x)
        #            / self.size)  # avant  # noqa
        nx = round((screen_x - (self.width / 2 - self.offset_x))
                   / self.size)  # apres

        ny = round(((self.height - 100 - self.offset_y)
                    - screen_y) / self.size)

        return (nx, ny)
