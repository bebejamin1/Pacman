

from dataclasses import dataclass
from enum import Enum
from typing import Any

from src.engine.algo import Cell, Greddy, Mode, Personality
from src.engine.entities import Ghost, GhostState, Player
from src.engine.level import Eaten, Level  # noqa


# *****************************************************************************
# *                                GAME STATE                                 *
# *                                                                           *

class GameState(Enum):

    RUNNING = "running"
    PAUSED = "paused"
    LEVEL_WON = "level_won"
    GAME_OVER = "game_over"
    VICTORY = "victory"


# *****************************************************************************
# *                                   RULES                                   *
# *                                                                           *

@dataclass
class Rules:

    lives: int = 3
    pacgum_points: int = 10
    super_pacgum_points: int = 50
    ghost_points: int = 200
    level_max_time: float = 90.0
    frightened_time: float = 7.0
    ghost_respawn_time: float = 7.0
    player_step: float = 0.16
    ghost_step: float = 0.20

# ================================= FROM CONF =================================

    @classmethod
    def from_conf(cls, conf: dict[str, Any]) -> "Rules":
        rules = cls()
        keys = {"live": "lives",
                "pacgum_points": "pacgum_points",
                "super_pacgum_points": "super_pacgum_points",
                "ghost_points": "ghost_points",
                "level_max_time": "level_max_time"}
        for conf_key, attr in keys.items():
            value = conf.get(conf_key)
            if (isinstance(value, (int, float))
                    and not isinstance(value, bool) and value > 0):
                setattr(rules, attr, value)
        return (rules)


# *****************************************************************************
# *                                  CHEATS                                   *
# *                                                                           *

@dataclass
class Cheats:

    invincible: bool = False
    freeze_ghosts: bool = False
    speed_boost: bool = False


PERSONALITIES: tuple[Personality, ...] = (
    Personality.CHASER, Personality.AMBUSHER,
    Personality.RANDOM, Personality.SHY,
)


# *****************************************************************************
# *                                   GAME                                    *
# *                                                                           *
# rules: Rules,
class Game:
    def __init__(self, first_maze: list[list[int]],
                 total_levels: int) -> None:
        # self.rules = rules
        self.total_levels = max(1, total_levels)
        self.cheats = Cheats()
        self.score = 0
        # self.lives = int(rules.lives)
        self.mode = Mode.CHASE
        self.state = GameState.RUNNING
        self.level_number = 0
        # self.time_left = float(rules.level_max_time)
        self._frightened_left = 0.0
        self._player_clock = 0.0
        self._ghost_clock = 0.0
        self._load(first_maze)

# =========================== SET PLAYER DIRECTION ============================

    def set_player_direction(self, direction: Cell) -> None:
        self.player.wanted = direction

# =============================== TOGGLE PAUSE ================================

    def toggle_pause(self) -> None:
        if (self.state is GameState.RUNNING):
            self.state = GameState.PAUSED
        elif (self.state is GameState.PAUSED):
            self.state = GameState.RUNNING

# ================================ NEXT LEVEL =================================

    def next_level(self, maze: list[list[int]]) -> None:
        if (self.state is GameState.LEVEL_WON):
            self._load(maze)

# ================================ SKIP LEVEL =================================

    def skip_level(self) -> None:
        if (self.state in (GameState.RUNNING, GameState.PAUSED)):
            self._win_level()

# ================================= ADD LIFE ==================================

    def add_life(self) -> None:
        self.lives += 1

# ================================== UPDATE ===================================

    def update(self, dt: float) -> None:
        if (self.state is not GameState.RUNNING):
            return
        self._tick_timers(dt)
        if (self.state is GameState.RUNNING):
            self._move_player(dt)
        if (self.state is GameState.RUNNING):
            self._move_ghosts(dt)

# ============================== FRIGHTENED LEFT ==============================

    @property
    def frightened_left(self) -> float:
        return max(0.0, self._frightened_left)

# =================================== LOAD ====================================

    def _load(self, maze: list[list[int]]) -> None:
        self.level_number += 1
        self.level = Level(maze, self.level_number)
        self.player = Player(pos=self.level.player_spawn,
                             spawn=self.level.player_spawn)

        self.ghosts = [
            Ghost(brain=Greddy(maze, perso, corner),
                  pos=corner, home=corner)
            for corner, perso in zip(self.level.corners, PERSONALITIES)
        ]

        self.mode = Mode.CHASE
        self.state = GameState.RUNNING
        # self.time_left = float(self.rules.level_max_time)
        self._frightened_left = 0.0
        self._player_clock = 0.0
        self._ghost_clock = 0.0

# ================================ TICK TIMERS ================================

    def _tick_timers(self, dt: float) -> None:

        self.time_left -= dt
        if (self.time_left <= 0):
            self._lose_life()
            return

        if (self._frightened_left > 0):
            self._frightened_left -= dt
            if (self._frightened_left <= 0):
                self.mode = Mode.CHASE

        for ghost in self.ghosts:
            if (ghost.state is GhostState.EATEN):
                ghost.respawn_in -= dt
                if (ghost.respawn_in <= 0):
                    ghost.reset()

# ================================ MOVE PLAYER ================================

    def _move_player(self, dt: float) -> None:
        self._player_clock += dt
        step = self.rules.player_step

        if (self.cheats.speed_boost):
            step /= 2

        while (self._player_clock >= step
                and self.state is GameState.RUNNING):
            self._player_clock -= step
            self._step_player()

# ================================ STEP PLAYER ================================

    def _step_player(self) -> None:

        player = self.player
        direction = player.direction

        if (self.level.can_move(player.pos, player.wanted)):
            direction = player.wanted

        if not (self.level.can_move(player.pos, direction)):
            return

        player.prev = player.pos
        player.direction = direction
        player.pos = (player.pos[0] + direction[0],
                      player.pos[1] + direction[1])
        self._eat(player.pos)

        if (self.state is GameState.RUNNING):
            self._check_collisions()

# ================================ MOVE GHOSTS ================================

    def _move_ghosts(self, dt: float) -> None:

        if (self.cheats.freeze_ghosts):
            return
        self._ghost_clock += dt
        step = self.rules.ghost_step

        if (self.mode is Mode.FRIGHTENED):
            step *= 1.5

        while (self._ghost_clock >= step
                and self.state is GameState.RUNNING):
            self._ghost_clock -= step
            lives_before = self.lives

            for ghost in self.ghosts:
                if (ghost.state is not GhostState.ACTIVE):
                    continue
                ghost.prev = ghost.pos
                ghost.pos = ghost.brain.next_move(
                    ghost.pos, self.player.pos,
                    self.player.direction, self.mode)
                self._check_collisions()

                if (self.lives != lives_before
                        or self.state is not GameState.RUNNING):
                    break

# ==================================== EAT ====================================

    def _eat(self, cell: Cell) -> None:
        found = self.level.eat(cell)
        if (found is Eaten.PACGUM):
            self.score += self.rules.pacgum_points
        elif (found is Eaten.SUPER):
            self.score += self.rules.super_pacgum_points
            self.mode = Mode.FRIGHTENED
            self._frightened_left = self.rules.frightened_time
        if (self.level.cleared):
            self._win_level()

# ============================= CHECK COLLISIONS ==============================

    def _check_collisions(self) -> None:

        player = self.player
        for ghost in self.ghosts:
            if (ghost.state is not GhostState.ACTIVE):
                continue
            same = ghost.pos == player.pos
            crossed = (ghost.pos == player.prev
                       and ghost.prev == player.pos)

            if not (same or crossed):
                continue

            if (self.mode is Mode.FRIGHTENED):
                self.score += self.rules.ghost_points
                ghost.state = GhostState.EATEN
                ghost.respawn_in = self.rules.ghost_respawn_time

            elif not (self.cheats.invincible):
                self._lose_life()
                return

# ================================= LOSE LIFE =================================

    def _lose_life(self) -> None:

        self.lives -= 1
        if (self.lives <= 0):
            self.lives = 0
            self.state = GameState.GAME_OVER
            return

        self.mode = Mode.CHASE
        self._frightened_left = 0.0
        self.time_left = float(self.rules.level_max_time)
        self.player.reset()

        for ghost in self.ghosts:
            ghost.reset()

# ================================= WIN LEVEL =================================

    def _win_level(self) -> None:
        if (self.level_number >= self.total_levels):
            self.state = GameState.VICTORY

        else:
            self.state = GameState.LEVEL_WON
