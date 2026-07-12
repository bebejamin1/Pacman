"""
C'est un algorithme glouton (greedy en anglais) : à chaque case, le fantôme
choisit le voisin qui minimise localement la distance à sa cible,
sans jamais planifier de chemin complet ni revenir en arrière.
distance euclidienne fantome efficace mais pas parfait
"""


import random
from collections import deque
from enum import Enum

NORTH, EAST, SOUTH, WEST = 1, 2, 4, 8

MOVES: list[tuple[int, int, int]] = [
    (0, -1, NORTH),
    (1, 0, EAST),
    (0, 1, SOUTH),
    (-1, 0, WEST),
]

Cell = tuple[int, int]


# *****************************************************************************
# *                                MODE                                       *
# *                                                                           *

class Mode(Enum):

    CHASE = "chase"
    FRIGHTENED = "frightened"


# *****************************************************************************
# *                            PERSONNALITY                                   *
# *                                                                           *

class Personality(Enum):

    CHASER = "chaser"
    AMBUSHER = "ambusher"
    RANDOM = "random"
    SHY = "shy"


# *****************************************************************************
# *                               GREDDY                                      *
# *                                                                           *

class Greddy:

    AMBUSH_LOOKAHEAD = 4
    SHY_DISTANCE = 8
    RANDOM_RATE = 0.5
    JITTER = 0.1
    MEMORY = 12

    def __init__(self, maze: list[list[int]], personality: Personality,
                 home_corner: Cell, seed: int | None = None) -> None:

        self._maze = maze
        self.personality = personality
        self._home = home_corner
        self._prev: Cell | None = None
        self._recent: deque[Cell] = deque(maxlen=self.MEMORY)
        self._rng = random.Random(seed)

# ============================= NEXT MOVE =====================================

    def next_move(self, ghost: Cell, player: Cell,
                  player_dir: Cell = (0, 0),
                  mode: Mode = Mode.CHASE) -> Cell:

        options = self._open_neighbors(ghost)
        if not options:
            return ghost

        if len(options) > 1 and self._prev in options:
            options.remove(self._prev)
        self._prev = ghost
        self._recent.append(ghost)
        self._rng.shuffle(options)

        if mode is Mode.FRIGHTENED:
            if len(options) > 1 and player in options:
                options.remove(player)
            options = self._keep_fresh(options)
            if self._rng.random() < self.JITTER:
                return options[0]
            return min(options, key=lambda c: self._dist(c, self._home))

        if player in options:
            return player

        options = self._keep_fresh(options)

        rate = (self.RANDOM_RATE if self.personality is Personality.RANDOM
                else self.JITTER)
        if self._rng.random() < rate:
            return options[0]

        target = self._target(ghost, player, player_dir)
        return min(options, key=lambda c: self._dist(c, target))

# ============================== RESET ========================================

    def reset(self) -> None:
        self._prev = None
        self._recent.clear()

# ============================= SET MAZE ======================================

    def set_maze(self, maze: list[list[int]]) -> None:
        self._maze = maze
        self.reset()

# ============================== TARGET =======================================

    def _target(self, ghost: Cell, player: Cell, player_dir: Cell) -> Cell:
        manhattan = (abs(ghost[0] - player[0])
                     + abs(ghost[1] - player[1]))
        if self.personality is Personality.AMBUSHER:
            if manhattan <= self.AMBUSH_LOOKAHEAD:
                return player
            return (player[0] + player_dir[0] * self.AMBUSH_LOOKAHEAD,
                    player[1] + player_dir[1] * self.AMBUSH_LOOKAHEAD)
        if self.personality is Personality.SHY:
            return player if manhattan >= self.SHY_DISTANCE else self._home
        return player

# ============================= KEEP FRESH ====================================

    def _keep_fresh(self, options: list[Cell]) -> list[Cell]:
        fresh = [c for c in options if c not in self._recent]
        return fresh if fresh else options

# =========================== OPEN NEIGHBORS ==================================

    def _open_neighbors(self, cell: Cell) -> list[Cell]:
        x, y = cell
        height, width = len(self._maze), len(self._maze[0])
        neighbors = []
        for dx, dy, wall in MOVES:
            nx, ny = x + dx, y + dy
            if (0 <= nx < width and 0 <= ny < height
                    and not self._maze[y][x] & wall
                    and self._maze[ny][nx] != 15):
                neighbors.append((nx, ny))
        return neighbors

# =============================== DIST ========================================

    @staticmethod
    def _dist(a: Cell, b: Cell) -> int:
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
