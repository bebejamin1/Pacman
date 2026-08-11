

import os
import arcade

from typing import Any

from src.engine.game import Cheats
from src.engine.algo import Cell, Mode
from src.renderer.in_game.maze import Maze
from src.renderer.in_game.characters import Player, Enemies

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.renderer.game_engine import GameEngine

from src.parsing.parse import parse_conf

# ----| CONSTANTS |---- #
PATH = "assets/background/"
MAZE_PATH = "assets/maze/"
MUSIC_PATH = "assets/sound/"

SPRITE_SIZE = 32 * 2
CHARACTER_SIZE = 0.65

GHOST_SPEED = 0.7
FRIGHT_TIME = 10.0
GHOST_RESPAWN_TIME = 7.0
# --------------------- #


class GameView(arcade.View):
    """
    This class will show the game and make the user
    able to control the character's movement.
    """
    def __init__(self, window: "GameEngine") -> None:
        super().__init__()
        self.window: GameEngine = window

        self.config: list[Any] = parse_conf("data/config.json")
        self.seed: int = self.config[1].get("seed")
        self.total_time: int = self.config[1].get("level_max_time")
        self.lvl: list[dict[str, Any]] = self.config[1].get("level")
        self.lvl_nb: int = 0

        self.rules: dict[str, Any] = self.config[1]
        self.lives: int = self.rules.get("live")

        self.flee: bool = False
        self._flee_timer: float = FRIGHT_TIME
        self._ghost_clock = 0.0

        self.cheats: Cheats = self.window.cheats
        self.speed: float = 1.25
        self.score: Any = 0

        self.level_text: arcade.Text
        self.timer_text: arcade.Text
        self.life_text: arcade.Text
        self.score_text: arcade.Text
        self.text: arcade.Text

    def setup(self, lvl_nb: int) -> None:
        self.lvl_nb = lvl_nb
        if self.lvl_nb == 0:
            self._maze_generation()
        else:
            lvl_width: int = self.lvl[self.lvl_nb]["width"]
            lvl_height: int = self.lvl[self.lvl_nb]["height"]

            self.next_level(lvl_width, lvl_height)
        self._collectibles()
        self._load_sprite()
        self._load_hud()

        self.player: Player = self.maze.player

        self.red: Enemies = self.maze.red
        self.orange: Enemies = self.maze.orange
        self.cyan: Enemies = self.maze.cyan
        self.pink: Enemies = self.maze.pink

        self.physic_engine = arcade.PhysicsEngineSimple(self.player,
                                                        self.maze.wall_list)

        self.red_physic_engine = arcade.PhysicsEngineSimple(
            self.red, self.maze.wall_list
                                                           )

        self.orange_physic_engine = arcade.PhysicsEngineSimple(
            self.orange, self.maze.wall_list
                                                              )

        self.cyan_physic_engine = arcade.PhysicsEngineSimple(
            self.cyan, self.maze.wall_list
                                                            )

        self.pink_physic_engine = arcade.PhysicsEngineSimple(
            self.pink, self.maze.wall_list
                                                            )

    def on_draw(self) -> None:
        self.clear()

        arcade.draw_texture_rect(self.background, arcade.LBWH(0, 0,
                                                              self.width,
                                                              self.height))

        # Draws the maze and its collectibles
        self.maze.ground_list.draw()
        self.maze.wall_list.draw()
        self.maze.pacgum_list.draw()
        self.maze.super_pac.draw()

        # Draws entities
        self.maze.player_list.draw()

        self.maze.red_lst.draw()
        self.maze.orange_lst.draw()
        self.maze.cyan_lst.draw()
        self.maze.pink_lst.draw()

        # Draws the HUD
        self.level_text.draw()
        self.timer_text.draw()
        self.life_text.draw()
        self.score_text.draw()
        self.text.draw()

    def on_update(self, delta_time: float) -> None:
        # Updates entities
        self.maze.player_list.update()

        self.maze.red_lst.update()
        self.maze.orange_lst.update()
        self.maze.cyan_lst.update()
        self.maze.pink_lst.update()

        # Makes the physics of the game
        self.physic_engine.update()
        self.red_physic_engine.update()
        self.orange_physic_engine.update()
        self.cyan_physic_engine.update()
        self.pink_physic_engine.update()

        # Entities animations
        self.player.update_animation(delta_time * 2, None, None)

        self.red.update_animation(delta_time, None, None)
        self.orange.update_animation(delta_time, None, None)
        self.cyan.update_animation(delta_time, None, None)
        self.pink.update_animation(delta_time, None, None)

        self._move_ghosts(delta_time)

        # Count down for the ghosts fleeing
        if self.flee:
            self._flee_timer -= delta_time
            if self._flee_timer <= 0:
                self.flee = False
                self._flee_timer = 0.0

        self.red.update_sprite(self.flee)
        self.orange.update_sprite(self.flee)
        self.cyan.update_sprite(self.flee)
        self.pink.update_sprite(self.flee)

        self._tick_ghost_respawn(delta_time)

        # Checks the collisions with collectibles
        pac_hit = arcade.check_for_collision_with_list(self.player,
                                                       self.maze.pacgum_list)
        if pac_hit:
            for p in pac_hit:
                self.score += self.rules.get("pacgum_points")
                self.score_text.text = self.score
                p.kill()

                if len(self.maze.pacgum_list) == 0:
                    if len(self.lvl) - 1 > self.lvl_nb:
                        self.lvl_nb += 1
                        lvl_width: int = self.lvl[self.lvl_nb]["width"]
                        lvl_height: int = self.lvl[self.lvl_nb]["height"]

                        self.next_level(lvl_width, lvl_height)

                    else:
                        self.window.switch_end(True, self.score)

        sup_pac_hit = arcade.check_for_collision_with_list(self.player,
                                                           self.maze.super_pac)
        if sup_pac_hit:
            for p in sup_pac_hit:
                self.score += self.rules.get("super_pacgum_points")
                self.score_text.text = self.score
                p.kill()
                self.flee = True
                self._flee_timer = FRIGHT_TIME

        # Checks the collisions with other entities
        red_hit = arcade.check_for_collision_with_list(self.player,
                                                       self.maze.red_lst)
        orange_hit = arcade.check_for_collision_with_list(self.player,
                                                          self.maze.orange_lst)
        cyan_hit = arcade.check_for_collision_with_list(self.player,
                                                        self.maze.cyan_lst)
        pink_hit = arcade.check_for_collision_with_list(self.player,
                                                        self.maze.pink_lst)

        if red_hit or orange_hit or cyan_hit or pink_hit:
            if self.flee is True:
                self.score += self.rules.get("ghost_points")
                self.score_text.text = self.score

                # Eaten ghost goes back to its spawn
                if red_hit:
                    self._eat_ghost(self.red)
                if orange_hit:
                    self._eat_ghost(self.orange)
                if cyan_hit:
                    self._eat_ghost(self.cyan)
                if pink_hit:
                    self._eat_ghost(self.pink)

            elif self.cheats.invincible is True:
                pass

            else:
                self.life -= 1
                if self.life == 0:
                    self.window.switch_end(False, self.score)
                else:
                    self.maze._restart_level()
                    self.time_elapsed = self.config[1].get("level_max_time")

        # Updates the HUD
        self.life_text.text = f"x{self.life}"
        self.level = self.lvl[self.lvl_nb].get("name")
        self.level_text.text = self.level

        # Updates the countdown
        self.time_elapsed -= delta_time
        minutes = int(self.time_elapsed // 60)
        seconds = int(self.time_elapsed % 60)
        self.timer_text.text = f"{minutes:02d}:{seconds:02d}"

        if "-" in self.timer_text.text:
            self.window.switch_end(False, self.score)

    def _move_ghosts(self, delta_time: float) -> None:
        if self.cheats.freeze_ghosts:
            return

        self._ghost_clock += delta_time

        if self.flee:
            mode = Mode.FRIGHTENED
            step = GHOST_SPEED * 1.5
        else:
            mode = Mode.CHASE
            step = GHOST_SPEED * 1.0

        if self._ghost_clock < step:
            return

        player_cell = self.maze.convert_cell_coords(self.player.center_x,
                                                    self.player.center_y)
        player_dir = self._player_direction()

        while self._ghost_clock >= step:
            self._ghost_clock -= step

            new_cell = self.red.next_move(player_cell, player_dir, mode)
            new_x, new_y = self.maze.convert_screen_coords(
                (new_cell[0] * 2, new_cell[1] * 2))
            self.red.center_x = new_x
            self.red.center_y = new_y

            # Hides the eaten ghosts outside the maze
            if self.red.eaten:
                self.red.center_x = -1000
                self.red.center_y = -1000

            new_cell = self.orange.next_move(player_cell, player_dir, mode)
            new_x, new_y = self.maze.convert_screen_coords(
                (new_cell[0] * 2, new_cell[1] * 2))
            self.orange.center_x = new_x
            self.orange.center_y = new_y

            # Hides the eaten ghosts outside the maze
            if self.orange.eaten:
                self.orange.center_x = -1000
                self.orange.center_y = -1000

            new_cell = self.cyan.next_move(player_cell, player_dir, mode)
            new_x, new_y = self.maze.convert_screen_coords(
                (new_cell[0] * 2, new_cell[1] * 2))
            self.cyan.center_x = new_x
            self.cyan.center_y = new_y

            # Hides the eaten ghosts outside the maze
            if self.cyan.eaten:
                self.cyan.center_x = -1000
                self.cyan.center_y = -1000

            new_cell = self.pink.next_move(player_cell, player_dir, mode)
            new_x, new_y = self.maze.convert_screen_coords(
                (new_cell[0] * 2, new_cell[1] * 2))
            self.pink.center_x = new_x
            self.pink.center_y = new_y

            # Hides the eaten ghosts outside the maze
            if self.pink.eaten:
                self.pink.center_x = -1000
                self.pink.center_y = -1000

    def _eat_ghost(self, ghost: Enemies) -> None:
        # Starts the cooldown
        ghost.eaten = True
        ghost.respawn_timer = GHOST_RESPAWN_TIME

    def _tick_ghost_respawn(self, delta_time: float) -> None:
        for ghost in (self.red, self.orange, self.cyan, self.pink):
            if not ghost.eaten:
                continue

            ghost.respawn_timer -= delta_time
            if ghost.respawn_timer <= 0:
                self._respawn_ghost(ghost)

    def _respawn_ghost(self, ghost: Enemies) -> None:
        ghost.eaten = False
        x, y = ghost.spawn
        nx, ny = self.maze.convert_screen_coords((x * 2, y * 2))
        ghost.center_x = nx
        ghost.center_y = ny
        ghost.cell = ghost.spawn
        ghost.brain.reset()

    def _player_direction(self) -> Cell:
        if self.player.change_x > 0:
            return (1, 0)
        if self.player.change_x < 0:
            return (-1, 0)
        if self.player.change_y > 0:
            return (0, -1)
        if self.player.change_y < 0:
            return (0, 1)
        return (0, 0)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            self.window.switch_menu()

        if symbol == arcade.key.SPACE:
            self.window.switch_pause()

        if symbol == arcade.key.C:
            self.window.switch_cheat()

        elif symbol == arcade.key.UP or symbol == arcade.key.W:
            self.player.change_y += self.speed
        elif symbol == arcade.key.DOWN or symbol == arcade.key.S:
            self.player.change_y -= self.speed
        elif symbol == arcade.key.LEFT or symbol == arcade.key.A:
            self.player.change_x -= self.speed
            self.player.scale_x = -0.6 * CHARACTER_SIZE
        elif symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.player.change_x += self.speed
            self.player.scale_x = 0.6 * CHARACTER_SIZE

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.UP or symbol == arcade.key.W:
            self.player.change_y = 0
        elif symbol == arcade.key.DOWN or symbol == arcade.key.S:
            self.player.change_y = 0
        elif symbol == arcade.key.LEFT or symbol == arcade.key.A:
            self.player.change_x = 0
        elif symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.player.change_x = 0

    def _load_hud(self) -> None:
        self.life = self.config[1].get("live")
        self.score = 0
        self.level = self.lvl[self.lvl_nb].get("name")

        self.level_text = arcade.Text(
            text=f"{self.level}",
            x=self.width / 2, y=self.height - 50,
            color=arcade.color.LAVENDER,
            font_size=25, anchor_x="center",
            font_name="Public Pixel"
                                     )

        self.timer_text = arcade.Text(
            text="00:00",
            x=self.width / 2, y=self.height - 85,
            color=arcade.color.LAVENDER,
            font_size=20, anchor_x="center",
            font_name="Public Pixel"
                                    )
        self.time_elapsed = self.config[1].get("level_max_time")

        self.life_text = arcade.Text(
            text=f"x{self.life}",
            x=50, y=self.height - 50,
            color=arcade.color.LAVENDER,
            font_size=25, anchor_x="left",
            font_name="Public Pixel"
                                    )

        self.score_text = arcade.Text(
            text=f"{self.score}",
            x=self.width - 50, y=self.height - 50,
            color=arcade.color.LAVENDER,
            font_size=25, anchor_x="right",
            font_name="Public Pixel"
                                     )

        self.text = arcade.Text(
            text="Press SPACE to pause",
            x=self.width / 2, y=100,
            color=arcade.color.LAVENDER,
            font_size=10, anchor_x="center",
            font_name="Public Pixel"
                               )

    def _maze_generation(self) -> None:
        self.game = self.window.new_game(self.config[1], self.lvl)

        self.maze: Maze = Maze(self.config[1], self.window.first_maze,
                               self.lvl_nb, self.width, self.height)
        self.maze.generate_maze()

    def next_level(self, width: int, height: int) -> None:
        self.next_maze: list[list[int]] = self.window.new_maze((width,
                                                                height),
                                                               self.seed)

        self.maze = Maze(self.config[1], self.next_maze,
                         self.lvl_nb, self.width, self.height)
        self.maze.generate_maze()

        self.maze._load_entities()

        self.player = self.maze.player
        self.red = self.maze.red
        self.orange = self.maze.orange
        self.cyan = self.maze.cyan
        self.pink = self.maze.pink

        self._ghost_clock = 0.0

        self.time_elapsed = self.config[1].get("level_max_time")

    def _collectibles(self) -> None:
        self.pacgum: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        self.super_pac: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()

    def _load_sprite(self) -> None:
        try:
            if not os.path.exists("assets/"):
                raise ValueError

            # Loads the background
            self.background = arcade.load_texture(f"{PATH}maze_back.png")

            # Loads the maze components and the player
            self.wall = arcade.load_texture(f"{MAZE_PATH}wall.png")
            self.ground = arcade.load_texture(f"{MAZE_PATH}ground.png")

            self.maze._load_entities()

        except FileNotFoundError:
            raise ValueError("\033[1;91mError: Assets folder not found\033[0m")
