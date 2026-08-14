

import os
import arcade

from typing import Any

from src.engine.game import Cheats
from src.engine.algo import Cell, Mode, MOVES  # ajout: MOVES
from src.renderer.in_game.maze import Maze
from src.renderer.in_game.characters import Player, Enemies

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.renderer.game_engine import GameEngine

from src.parsing.parse_main import config

# ----| CONSTANTS |---- #
PATH = "assets/background/"
MAZE_PATH = "assets/maze/"
MUSIC_PATH = "assets/sound/"

SPRITE_SIZE = 32 * 2
CHARACTER_SIZE = 0.65

GHOST_SPEED = 0.7
PLAYER_SPEED = 0.7
FRIGHT_TIME = 10.0
GHOST_RESPAWN_TIME = 7.0

# ajout associe une direction (dx, dy) au bit de mur qui la bloque
DIRECTION_WALL: dict[Cell, int] = {(dx, dy): wall for dx, dy, wall in MOVES}
# --------------------- #


class GameView(arcade.View):
    """
    This class will show the game and make the user
    able to control the character's movement.
    """
    def __init__(self, window: "GameEngine") -> None:
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
        # ajout: alterne entre les 2 demipas du deplacement des fantomes
        self._ghost_at_midpoint: bool = False

        self.cheats: Cheats = self.window.cheats
        self.score: Any = 0

        # ajout: etat du deplacement case par case du joueur
        self._player_clock: float = 0.0
        self._player_at_midpoint: bool = False
        self.player_dir: Cell = (0, 0)
        self.player_next_dir: Cell = (0, 0)

        self._prev_player_cell: Cell = (0, 0)  # ajout
        self._prev_ghost_cell: dict[Enemies, Cell] = {}  # ajout
        self._ghost_settled_cell: dict[Enemies, Cell] = {}  # ajout

        # ajout: points de depart/arrivee pour interpoler le rendu en douceur
        self._player_from: tuple[float, float] = (0.0, 0.0)  # ajout
        self._player_to: tuple[float, float] = (0.0, 0.0)  # ajout
        self._ghost_from: dict[Enemies, tuple[float, float]] = {}  # ajout
        self._ghost_to: dict[Enemies, tuple[float, float]] = {}  # ajout

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

        self._reset_collision_tracking()  # ajout

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

        self._move_player(delta_time)
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
        red_hit = self._ghost_collision(  # modif
            self.red, bool(arcade.check_for_collision_with_list(  # modif
                self.player, self.maze.red_lst)))  # modif
        orange_hit = self._ghost_collision(  # modif
            self.orange, bool(arcade.check_for_collision_with_list(  # modif
                self.player, self.maze.orange_lst)))  # modif
        cyan_hit = self._ghost_collision(  # modif
            self.cyan, bool(arcade.check_for_collision_with_list(  # modif
                self.player, self.maze.cyan_lst)))  # modif
        pink_hit = self._ghost_collision(  # modif
            self.pink, bool(arcade.check_for_collision_with_list(  # modif
                self.player, self.maze.pink_lst)))  # modif

        # ajout: memorise la case arriver pour anim
        self._prev_player_cell = self.player.cell  # modif
        for ghost in (self.red, self.orange, self.cyan, self.pink):  # ajout
            self._prev_ghost_cell[ghost] = self._ghost_settled_cell.get(  # modif  # noqa
                ghost, ghost.cell)  # modif

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
                    # ajout: reinitialise le deplacement du joueur au respawn
                    self.player_dir = (0, 0)
                    self.player_next_dir = (0, 0)
                    self._player_at_midpoint = False
                    self.time_elapsed = self.config[1].get("level_max_time")
                    self._reset_collision_tracking()  # ajout

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

        # ajout: evite de sauter 2 case
        half_step = step / 2

        # ajout: meme chose evite de sauter 2 case mais pour les 4 fantomes
        while self._ghost_clock >= half_step:
            self._ghost_clock -= half_step
            self._ghost_at_midpoint = not self._ghost_at_midpoint

            # modif: calcule seulement quand un demi-pas a vraiment lieu
            player_cell = self.maze.convert_cell_coords(  # modif
                self.player.center_x, self.player.center_y)  # modif
            player_dir = self._player_direction()  # modif

            for ghost in (self.red, self.orange, self.cyan, self.pink):
                if self._ghost_at_midpoint:
                    # ajout: demi pas decide de quel case il prend
                    old_cell = ghost.cell
                    new_cell = ghost.next_move(player_cell, player_dir, mode)
                    dx = new_cell[0] - old_cell[0]
                    dy = new_cell[1] - old_cell[1]
                    new_x, new_y = self.maze.convert_screen_coords(
                        (old_cell[0] * 2 + dx, old_cell[1] * 2 + dy))
                else:
                    # ajout: demi pas entier termine le trajet
                    new_x, new_y = self.maze.convert_screen_coords(
                        (ghost.cell[0] * 2, ghost.cell[1] * 2))
                    # ajout: pour debug affichage fantome
                    self._ghost_settled_cell[ghost] = ghost.cell  # ajout

                # ajout: ne saute plus directement, glissement fluide  # noqa
                self._ghost_from[ghost] = self._ghost_to[ghost]  # ajout
                self._ghost_to[ghost] = (new_x, new_y)  # ajout

        # ajout: anim fantome
        t = min(self._ghost_clock / half_step, 1.0)  # ajout
        for ghost in (self.red, self.orange, self.cyan, self.pink):  # ajout
            from_x, from_y = self._ghost_from[ghost]  # ajout
            to_x, to_y = self._ghost_to[ghost]  # ajout
            ghost.center_x = from_x + (to_x - from_x) * t  # ajout
            ghost.center_y = from_y + (to_y - from_y) * t  # ajout

            # Hides the eaten ghosts outside the maze
            if ghost.eaten:
                ghost.center_x = -1000
                ghost.center_y = -1000

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

    # ajout: memorise les case pour ne pas rater des collision
    def _reset_collision_tracking(self) -> None:  # ajout
        self._ghost_settled_cell = {  # ajout
            ghost: ghost.cell  # ajout
            for ghost in (self.red, self.orange, self.cyan, self.pink)  # ajout
        }  # ajout
        self._prev_player_cell = self.player.cell  # ajout
        self._prev_ghost_cell = dict(self._ghost_settled_cell)  # ajout

        # ajout: anim
        self._player_from = (self.player.center_x, self.player.center_y)  # ajout  # noqa
        self._player_to = self._player_from  # ajout
        self._ghost_from = {  # ajout
            ghost: (ghost.center_x, ghost.center_y)  # ajout
            for ghost in (self.red, self.orange, self.cyan, self.pink)  # ajout
        }  # ajout
        self._ghost_to = dict(self._ghost_from)  # ajout

    # ajout: detecte une collision
    def _ghost_collision(self, ghost: Enemies, pixel_hit: bool) -> bool:  # ajout  # noqa
        if ghost.eaten:  # ajout
            return False  # ajout

        player_cell = self.player.cell  # modif
        ghost_cell = self._ghost_settled_cell.get(ghost, ghost.cell)  # modif

        swapped = (player_cell == self._prev_ghost_cell.get(ghost)  # ajout
                   and ghost_cell == self._prev_player_cell)  # ajout

        return pixel_hit or player_cell == ghost_cell or swapped  # ajout

    # ajout: direction du joeur
    def _player_direction(self) -> Cell:
        return self.player_dir

    # ajout: verirfie si le joueur peu avancer
    def _can_step(self, cell: Cell, direction: Cell) -> bool:
        x, y = cell
        dx, dy = direction
        nx, ny = x + dx, y + dy

        maze = self.maze.maze
        height, width = len(maze), len(maze[0])

        return (0 <= nx < width and 0 <= ny < height
                and not maze[y][x] & DIRECTION_WALL[direction]
                and maze[ny][nx] != 15)

    # ajout: deplacement du joueur
    def _move_player(self, delta_time: float) -> None:
        self._player_clock += delta_time
        half_step = self.player_speed / 2

        while self._player_clock >= half_step:
            self._player_clock -= half_step
            self._player_at_midpoint = not self._player_at_midpoint

            if self._player_at_midpoint:
                # ajout: permet de bloquer sur une direction demander et tant
                # que bloquer continue sur la direction de base
                direction = self.player_dir
                if (self.player_next_dir != (0, 0)
                        and self._can_step(self.player.cell,
                                           self.player_next_dir)):
                    direction = self.player_next_dir

                if (direction == (0, 0)
                        or not self._can_step(self.player.cell, direction)):
                    self._player_at_midpoint = False
                    # ajout: pour eviter rollback contact avec mur
                    self._player_from = self._player_to  # ajout
                    continue

                self.player_dir = direction
                dx, dy = direction
                new_x, new_y = self.maze.convert_screen_coords(
                    (self.player.cell[0] * 2 + dx,
                     self.player.cell[1] * 2 + dy))

                if dx > 0:
                    self.player.scale_x = 0.6 * CHARACTER_SIZE
                elif dx < 0:
                    self.player.scale_x = -0.6 * CHARACTER_SIZE
            else:
                x, y = self.player.cell
                dx, dy = self.player_dir

                # ajout: pour changer de direction sans trop de delai
                if (self.player_next_dir == (-dx, -dy)  # ajout
                        and self._can_step(self.player.cell,  # ajout
                                           self.player_next_dir)):  # ajout
                    self.player_dir = self.player_next_dir  # ajout
                    dx, dy = self.player_dir  # ajout

                    if dx > 0:  # ajout
                        self.player.scale_x = 0.6 * CHARACTER_SIZE  # ajout
                    elif dx < 0:  # ajout
                        self.player.scale_x = -0.6 * CHARACTER_SIZE  # ajout
                else:
                    self.player.cell = (x + dx, y + dy)  # modif

                new_x, new_y = self.maze.convert_screen_coords(
                    (self.player.cell[0] * 2, self.player.cell[1] * 2))

            # ajout: anim
            self._player_from = self._player_to  # ajout
            self._player_to = (new_x, new_y)  # ajout

        # ajout: deplacement flui vers la prochaine case
        t = min(self._player_clock / half_step, 1.0)  # ajout
        self.player.center_x = (self._player_from[0]  # ajout
                                + (self._player_to[0]  # ajout
                                   - self._player_from[0]) * t)  # ajout
        self.player.center_y = (self._player_from[1]  # ajout
                                + (self._player_to[1]  # ajout
                                   - self._player_from[1]) * t)  # ajout

    # ajout: change de direction dans le talbeau grace aux coordonnee
    def on_key_press(self, symbol: int, modifiers: int) -> None:
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
        self._ghost_at_midpoint = False  # ajout
        self._player_clock = 0.0  # ajout
        self._player_at_midpoint = False  # ajout
        self.player_dir = (0, 0)  # ajout
        self.player_next_dir = (0, 0)  # ajout
        self._reset_collision_tracking()  # ajout

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
