"""Greedy pathfinding used to drive the ghosts' autonomous movement.

At each cell, a ghost picks the open neighbour that locally minimizes the
distance to its target: it never plans a full path and never looks ahead
beyond one step. This is cheap to compute and gives each personality a
distinct, recognizable behaviour without needing a full pathfinding graph.
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


class Mode(Enum):
    """Ghost behaviour mode."""

    CHASE = "chase"
    FRIGHTENED = "frightened"


class Personality(Enum):
    """Ghost personality, driving how it picks its target cell."""

    CHASER = "chaser"
    AMBUSHER = "ambusher"
    RANDOM = "random"
    SHY = "shy"


class Greddy:
    """Greedy, personality-driven movement brain for a single ghost."""

    AMBUSH_LOOKAHEAD = 4
    SHY_DISTANCE = 8
    RANDOM_RATE = 0.5
    JITTER = 0.1
    MEMORY = 12

    def __init__(self, maze: list[list[int]], personality: Personality,
                 home_corner: Cell, seed: int | None = None) -> None:
        """Create a movement brain bound to one maze and personality.

        Args:
            maze: Wall-bitmask grid the ghost moves through.
            personality: Behaviour driving target selection.
            home_corner: Cell the ghost returns to when reset or eaten.
            seed: Optional seed for the internal random generator.
        """
        self._maze = maze
        self.personality = personality
        self._home = home_corner
        self._prev: Cell | None = None
        self._recent: deque[Cell] = deque(maxlen=self.MEMORY)
        self._rng = random.Random(seed)

    def next_move(self, ghost: Cell, player: Cell,
                  player_dir: Cell = (0, 0),
                  mode: Mode = Mode.CHASE) -> Cell:
        """Pick the next cell for the ghost to move to.

        Args:
            ghost: Ghost's current cell.
            player: Player's current cell.
            player_dir: Player's current movement direction.
            mode: Current ghost mode (chase or frightened).

        Returns:
            The cell the ghost should move to next.
        """
        options = self._open_neighbors(ghost)
        if not (options):
            return (ghost)

        if (len(options) > 1 and self._prev in options):
            options.remove(self._prev)
        self._prev = ghost
        self._recent.append(ghost)
        self._rng.shuffle(options)

        if (mode is Mode.FRIGHTENED):
            if (len(options) > 1 and player in options):
                options.remove(player)
            options = self._keep_fresh(options)
            if (self._rng.random() < self.JITTER):
                return (options[0])
            return min(options, key=lambda c: self._dist(c, self._home))

        if (player in options):
            return (player)

        options = self._keep_fresh(options)

        rate = (self.RANDOM_RATE if self.personality is Personality.RANDOM
                else self.JITTER)
        if (self._rng.random() < rate):
            return (options[0])

        target = self._target(ghost, player, player_dir)
        return min(options, key=lambda c: self._dist(c, target))

    def reset(self) -> None:
        """Clear the ghost's movement history, as after a respawn."""
        self._prev = None
        self._recent.clear()

    def set_maze(self, maze: list[list[int]]) -> None:
        """Bind the brain to a new maze and reset its movement history.

        Args:
            maze: Wall-bitmask grid of the new level.
        """
        self._maze = maze
        self.reset()

    def _target(self, ghost: Cell, player: Cell, player_dir: Cell) -> Cell:
        """Compute the cell this personality is currently aiming for.

        Args:
            ghost: Ghost's current cell.
            player: Player's current cell.
            player_dir: Player's current movement direction.

        Returns:
            The target cell used to rank the candidate moves.
        """
        manhattan = (abs(ghost[0] - player[0])
                     + abs(ghost[1] - player[1]))
        if (self.personality is Personality.AMBUSHER):
            if (manhattan <= self.AMBUSH_LOOKAHEAD):
                return (player)
            return (player[0] + player_dir[0] * self.AMBUSH_LOOKAHEAD,
                    player[1] + player_dir[1] * self.AMBUSH_LOOKAHEAD)
        if (self.personality is Personality.SHY):
            return (player if manhattan >= self.SHY_DISTANCE else self._home)
        return (player)

    def _keep_fresh(self, options: list[Cell]) -> list[Cell]:
        """Filter out recently visited cells to avoid back-and-forth moves.

        Args:
            options: Candidate cells to move to.

        Returns:
            The candidates not visited recently, or all of them if that
            would leave no option.
        """
        fresh = [c for c in options if c not in self._recent]
        return (fresh if fresh else options)

    def _open_neighbors(self, cell: Cell) -> list[Cell]:
        """List the cells reachable from ``cell`` in a single step.

        Args:
            cell: Cell to look around.

        Returns:
            Neighbouring cells not separated from ``cell`` by a wall.
        """
        x, y = cell
        height, width = len(self._maze), len(self._maze[0])
        neighbors = []
        for dx, dy, wall in MOVES:
            nx, ny = x + dx, y + dy
            if (0 <= nx < width and 0 <= ny < height
                    and not self._maze[y][x] & wall
                    and self._maze[ny][nx] != 15):
                neighbors.append((nx, ny))
        return (neighbors)

    @staticmethod
    def _dist(a: Cell, b: Cell) -> int:
        """Return the squared Euclidean distance between two cells."""
        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
