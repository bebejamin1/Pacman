import os
import arcade

from typing import Any

from src.engine.game import Cheats
from src.engine.algo import Cell, Mode, MOVES
from src.renderer.in_game.maze import Maze
from src.renderer.in_game.characters import Player, Enemies

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.renderer.game_engine import GameEngine

from src.parsing.parse_main import config

PATH = "assets/background/"
MAZE_PATH = "assets/maze/"
MUSIC_PATH = "assets/sound/"

SPRITE_SIZE = 32 * 2
CHARACTER_SIZE = 0.65

GHOST_SPEED = 0.7
PLAYER_SPEED = 0.7
FRIGHT_TIME = 10.0
GHOST_RESPAWN_TIME = 7.0

DIRECTION_WALL: dict[Cell, int] = {(dx, dy): wall for dx, dy, wall in MOVES}


class GameView(arcade.View):
    """Drives the actual gameplay: movement, collisions, HUD and timers."""

    def __init__(self, window: "GameEngine") -> None:
        """Initialize movement, timing and HUD state for a new game view.

        Args:
            window: Owning game window.
        """
        super().__init__()
        self.window: GameEngine = window

        self.player_speed = PLAYER_SPEED

        self.config: list[Any] = config
        self.seed: int = self.config[1].get("seed")
        self.total_time: int = self.config[1].get("level_max_time")
        self.lvl: list[dict[str, Any]] = self.config[1].get("level")
        self.lvl_nb: int = 0

        self.rules: dict[str, Any] = self.config[1]
        self.lives: int = self.rules.get("live")

        self.flee: bool = False
        self._flee_timer: float = FRIGHT_TIME
        self._ghost_clock = 0.0
        self._ghost_at_midpoint: bool = False

        self.cheats: Cheats = self.window.cheats
        self.score: Any = 0

        self._player_clock: float = 0.0
        self._player_at_midpoint: bool = False
        self.player_dir: Cell = (0, 0)
        self.player_next_dir: Cell = (0, 0)

        self._prev_player_cell: Cell = (0, 0)
        self._prev_ghost_cell: dict[Enemies, Cell] = {}
        self._ghost_settled_cell: dict[Enemies, Cell] = {}

        self._player_from: tuple[float, float] = (0.0, 0.0)
        self._player_to: tuple[float, float] = (0.0, 0.0)
        self._ghost_from: dict[Enemies, tuple[float, float]] = {}
        self._ghost_to: dict[Enemies, tuple[float, float]] = {}

        self.level_text: arcade.Text
        self.timer_text: arcade.Text
        self.life_text: arcade.Text
        self.score_text: arcade.Text
        self.text: arcade.Text

    def setup(self, lvl_nb: int) -> None:
        """Load a level, its sprites and its HUD, then bind entities.

        Args:
            lvl_nb: Index of the level to load. ``0`` generates the
                first maze; any other value loads the next one.
        """
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

        self._reset_collision_tracking()

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
        """Draw the maze, entities, collectibles and HUD."""
        self.clear()

        arcade.draw_texture_rect(self.background, arcade.LBWH(0, 0,
                                                              self.width,
                                                              self.height))

        self.maze.ground_list.draw()
        self.maze.wall_list.draw()
        self.maze.pacgum_list.draw()
        self.maze.super_pac.draw()

        self.maze.player_list.draw()

        self.maze.red_lst.draw()
        self.maze.orange_lst.draw()
        self.maze.cyan_lst.draw()
        self.maze.pink_lst.draw()

        self.level_text.draw()
        self.timer_text.draw()
        self.life_text.draw()
        self.score_text.draw()
        self.text.draw()

    def on_update(self, delta_time: float) -> None:
        """Advance one game tick: movement, collisions, timers and HUD.

        Args:
            delta_time: Elapsed time, in seconds, since the last tick.
        """
        self.maze.player_list.update()

        self.maze.red_lst.update()
        self.maze.orange_lst.update()
        self.maze.cyan_lst.update()
        self.maze.pink_lst.update()

        self.physic_engine.update()
        self.red_physic_engine.update()
        self.orange_physic_engine.update()
        self.cyan_physic_engine.update()
        self.pink_physic_engine.update()

        self.player.update_animation(delta_time * 2, None, None)

        self.red.update_animation(delta_time, None, None)
        self.orange.update_animation(delta_time, None, None)
        self.cyan.update_animation(delta_time, None, None)
        self.pink.update_animation(delta_time, None, None)

        self._move_player(delta_time)
        self._move_ghosts(delta_time)

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

        red_hit = self._ghost_collision(
            self.red, bool(arcade.check_for_collision_with_list(
                self.player, self.maze.red_lst)))
        orange_hit = self._ghost_collision(
            self.orange, bool(arcade.check_for_collision_with_list(
                self.player, self.maze.orange_lst)))
        cyan_hit = self._ghost_collision(
            self.cyan, bool(arcade.check_for_collision_with_list(
                self.player, self.maze.cyan_lst)))
        pink_hit = self._ghost_collision(
            self.pink, bool(arcade.check_for_collision_with_list(
                self.player, self.maze.pink_lst)))

        self._prev_player_cell = self.player.cell
        for ghost in (self.red, self.orange, self.cyan, self.pink):
            self._prev_ghost_cell[ghost] = self._ghost_settled_cell.get(
                ghost, ghost.cell)

        if red_hit or orange_hit or cyan_hit or pink_hit:
            if self.flee is True:
                self.score += self.rules.get("ghost_points")
                self.score_text.text = self.score

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
                    self.player_dir = (0, 0)
                    self.player_next_dir = (0, 0)
                    self._player_at_midpoint = False
                    self.time_elapsed = self.config[1].get("level_max_time")
                    self._reset_collision_tracking()

        self.life_text.text = f"x{self.life}"
        self.level = self.lvl[self.lvl_nb].get("name")
        self.level_text.text = self.level

        self.time_elapsed -= delta_time
        minutes = int(self.time_elapsed // 60)
        seconds = int(self.time_elapsed % 60)
        self.timer_text.text = f"{minutes:02d}:{seconds:02d}"

        if "-" in self.timer_text.text:
            self.window.switch_end(False, self.score)

    def _move_ghosts(self, delta_time: float) -> None:
        """Advance every ghost's half-step animation and AI decisions.

        Ghosts move in two half-steps per cell: the first half decides
        and commits to the destination cell, the second half finishes
        sliding into it, which keeps the on-screen motion smooth.

        Args:
            delta_time: Elapsed time, in seconds, since the last tick.
        """
        if self.cheats.freeze_ghosts:
            return

        self._ghost_clock += delta_time

        if self.flee:
            mode = Mode.FRIGHTENED
            step = GHOST_SPEED * 1.5
        else:
            mode = Mode.CHASE
            step = GHOST_SPEED * 1.0

        half_step = step / 2

        while self._ghost_clock >= half_step:
            self._ghost_clock -= half_step
            self._ghost_at_midpoint = not self._ghost_at_midpoint

            player_cell = self.maze.convert_cell_coords(
                self.player.center_x, self.player.center_y)
            player_dir = self._player_direction()

            for ghost in (self.red, self.orange, self.cyan, self.pink):
                if self._ghost_at_midpoint:
                    old_cell = ghost.cell
                    new_cell = ghost.next_move(player_cell, player_dir, mode)
                    dx = new_cell[0] - old_cell[0]
                    dy = new_cell[1] - old_cell[1]
                    new_x, new_y = self.maze.convert_screen_coords(
                        (old_cell[0] * 2 + dx, old_cell[1] * 2 + dy))
                else:
                    new_x, new_y = self.maze.convert_screen_coords(
                        (ghost.cell[0] * 2, ghost.cell[1] * 2))
                    self._ghost_settled_cell[ghost] = ghost.cell

                self._ghost_from[ghost] = self._ghost_to[ghost]
                self._ghost_to[ghost] = (new_x, new_y)

        t = min(self._ghost_clock / half_step, 1.0)
        for ghost in (self.red, self.orange, self.cyan, self.pink):
            from_x, from_y = self._ghost_from[ghost]
            to_x, to_y = self._ghost_to[ghost]
            ghost.center_x = from_x + (to_x - from_x) * t
            ghost.center_y = from_y + (to_y - from_y) * t

            if ghost.eaten:
                ghost.center_x = -1000
                ghost.center_y = -1000

    def _eat_ghost(self, ghost: Enemies) -> None:
        """Mark a ghost as eaten and start its respawn cooldown.

        Args:
            ghost: Ghost that was just eaten.
        """
        ghost.eaten = True
        ghost.respawn_timer = GHOST_RESPAWN_TIME

    def _tick_ghost_respawn(self, delta_time: float) -> None:
        """Count down eaten ghosts' respawn timers and respawn them.

        Args:
            delta_time: Elapsed time, in seconds, since the last tick.
        """
        for ghost in (self.red, self.orange, self.cyan, self.pink):
            if not ghost.eaten:
                continue

            ghost.respawn_timer -= delta_time
            if ghost.respawn_timer <= 0:
                self._respawn_ghost(ghost)

    def _respawn_ghost(self, ghost: Enemies) -> None:
        """Move a ghost back to its home corner and reset its brain.

        Args:
            ghost: Ghost to respawn.
        """
        ghost.eaten = False
        x, y = ghost.spawn
        nx, ny = self.maze.convert_screen_coords((x * 2, y * 2))
        ghost.center_x = nx
        ghost.center_y = ny
        ghost.cell = ghost.spawn
        ghost.brain.reset()

    def _reset_collision_tracking(self) -> None:
        """Reset the cell/position history used for collision detection."""
        self._ghost_settled_cell = {
            ghost: ghost.cell
            for ghost in (self.red, self.orange, self.cyan, self.pink)
        }
        self._prev_player_cell = self.player.cell
        self._prev_ghost_cell = dict(self._ghost_settled_cell)

        self._player_from = (self.player.center_x, self.player.center_y)
        self._player_to = self._player_from
        self._ghost_from = {
            ghost: (ghost.center_x, ghost.center_y)
            for ghost in (self.red, self.orange, self.cyan, self.pink)
        }
        self._ghost_to = dict(self._ghost_from)

    def _ghost_collision(self, ghost: Enemies, pixel_hit: bool) -> bool:
        """Detect a player/ghost collision, including a same-frame swap.

        Combines the sprite-based pixel collision with a logical-cell
        check, so a player and a ghost swapping cells within the same
        tick are still detected as a collision.

        Args:
            ghost: Ghost to check against the player.
            pixel_hit: Whether Arcade's sprite collision already fired.

        Returns:
            True if the player and the ghost collided this tick.
        """
        if ghost.eaten:
            return False

        player_cell = self.player.cell
        ghost_cell = self._ghost_settled_cell.get(ghost, ghost.cell)

        swapped = (player_cell == self._prev_ghost_cell.get(ghost)
                   and ghost_cell == self._prev_player_cell)

        return pixel_hit or player_cell == ghost_cell or swapped

    def _player_direction(self) -> Cell:
        """Return the player's current movement direction."""
        return self.player_dir

    def _can_step(self, cell: Cell, direction: Cell) -> bool:
        """Check whether the player can move from ``cell`` in ``direction``.

        Args:
            cell: Player's current logical cell.
            direction: Movement direction, as a unit vector.

        Returns:
            True if the destination cell exists and is not blocked by a
            wall or a solid cell.
        """
        x, y = cell
        dx, dy = direction
        nx, ny = x + dx, y + dy

        maze = self.maze.maze
        height, width = len(maze), len(maze[0])

        return (0 <= nx < width and 0 <= ny < height
                and not maze[y][x] & DIRECTION_WALL[direction]
                and maze[ny][nx] != 15)

    def _move_player(self, delta_time: float) -> None:
        """Advance the player's half-step animation and grid movement.

        Mirrors ``_move_ghosts``: the first half-step commits to a
        destination cell (preferring the queued direction when it is
        walkable), the second half finishes sliding into it.

        Args:
            delta_time: Elapsed time, in seconds, since the last tick.
        """
        self._player_clock += delta_time
        half_step = self.player_speed / 2

        while self._player_clock >= half_step:
            self._player_clock -= half_step
            self._player_at_midpoint = not self._player_at_midpoint

            if self._player_at_midpoint:
                direction = self.player_dir
                if (self.player_next_dir != (0, 0)
                        and self._can_step(self.player.cell,
                                           self.player_next_dir)):
                    direction = self.player_next_dir

                if (direction == (0, 0)
                        or not self._can_step(self.player.cell, direction)):
                    self._player_at_midpoint = False
                    self._player_from = self._player_to
                    continue

                self.player_dir = direction
                dx, dy = direction
                new_x, new_y = self.maze.convert_screen_coords(
                    (self.player.cell[0] * 2 + dx,
                     self.player.cell[1] * 2 + dy))

                if dx > 0:
                    self.player.scale_x = abs(self.player.scale_x)
                elif dx < 0:
                    self.player.scale_x = -abs(self.player.scale_x)
            else:
                x, y = self.player.cell
                dx, dy = self.player_dir

                if (self.player_next_dir == (-dx, -dy)
                        and self._can_step(self.player.cell,
                                           self.player_next_dir)):
                    self.player_dir = self.player_next_dir
                    dx, dy = self.player_dir

                    if dx > 0:
                        self.player.scale_x = abs(self.player.scale_x)
                    elif dx < 0:
                        self.player.scale_x = -abs(self.player.scale_x)
                else:
                    self.player.cell = (x + dx, y + dy)

                new_x, new_y = self.maze.convert_screen_coords(
                    (self.player.cell[0] * 2, self.player.cell[1] * 2))

            self._player_from = self._player_to
            self._player_to = (new_x, new_y)

        t = min(self._player_clock / half_step, 1.0)
        self.player.center_x = (self._player_from[0]
                                + (self._player_to[0]
                                   - self._player_from[0]) * t)
        self.player.center_y = (self._player_from[1]
                                + (self._player_to[1]
                                   - self._player_from[1]) * t)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Handle pause, cheat menu, quit and movement key presses.

        Args:
            symbol: Key that was pressed.
            modifiers: Active modifier keys (unused).
        """
        if symbol == arcade.key.ESCAPE:
            self.window.switch_menu()

        if symbol == arcade.key.SPACE:
            self.window.switch_pause()

        if symbol == arcade.key.C:
            self.window.switch_cheat()

        elif symbol == arcade.key.UP or symbol == arcade.key.W:
            self.player_next_dir = (0, -1)
        elif symbol == arcade.key.DOWN or symbol == arcade.key.S:
            self.player_next_dir = (0, 1)
        elif symbol == arcade.key.LEFT or symbol == arcade.key.A:
            self.player_next_dir = (-1, 0)
        elif symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.player_next_dir = (1, 0)

    def _load_hud(self) -> None:
        """Create the score, lives, level and timer HUD text objects."""
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
        """Generate the first level's maze and build its ``Maze`` view."""
        self.window.generate_first_maze(self.config[1], self.lvl)

        self.maze: Maze = Maze(self.config[1], self.window.first_maze,
                               self.lvl_nb, self.width, self.height)
        self.maze.generate_maze()

    def next_level(self, width: int, height: int) -> None:
        """Generate the next level's maze, entities and HUD timer.

        Args:
            width: Width of the next level's maze.
            height: Height of the next level's maze.
        """
        self.next_maze: list[list[int]] = self.window.new_maze((width,
                                                                height),
                                                               0)

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
        self._ghost_at_midpoint = False
        self._player_clock = 0.0
        self._player_at_midpoint = False
        self.player_dir = (0, 0)
        self.player_next_dir = (0, 0)
        self._reset_collision_tracking()

        self.time_elapsed = self.config[1].get("level_max_time")

    def _collectibles(self) -> None:
        """Initialize the empty pacgum and super-pacgum sprite lists."""
        self.pacgum: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        self.super_pac: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()

    def _load_sprite(self) -> None:
        """Load the background and maze textures for the current level.

        Raises:
            ValueError: If the ``assets/`` folder is missing.
        """
        try:
            if not os.path.exists("assets/"):
                raise ValueError

            self.background = arcade.load_texture(f"{PATH}maze_back.png")

            self.wall = arcade.load_texture(f"{MAZE_PATH}wall.png")
            self.ground = arcade.load_texture(f"{MAZE_PATH}ground.png")

            self.maze._load_entities()

        except FileNotFoundError:
            raise ValueError("\033[1;91mError: Assets folder not found\033[0m")
