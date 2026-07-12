
from enum import Enum

from src.engine.algo import Cell

SOLID = 15

WALL_BITS: dict[Cell, int] = {
    (0, -1): 1,
    (1, 0): 2,
    (0, 1): 4,
    (-1, 0): 8,
}


# *****************************************************************************
# *                                   EATEN                                   *
# *                                                                           *

class Eaten(Enum):

    NOTHING = "nothing"
    PACGUM = "pacgum"
    SUPER = "super"


# *****************************************************************************
# *                                   LEVEL                                   *
# *                                                                           *

class Level:
    def __init__(self, maze: list[list[int]], number: int) -> None:
        self.maze = maze
        self.number = number
        self.height = len(maze)
        self.width = len(maze[0]) if maze else 0
        open_cells = {(x, y) for y in range(self.height)
                      for x in range(self.width) if maze[y][x] != SOLID}
        if not open_cells:
            raise ValueError("the maze has no walkable cell")
        self.corners = [self._closest(c, open_cells) for c in
                        ((0, 0), (self.width - 1, 0),
                         (0, self.height - 1),
                         (self.width - 1, self.height - 1))]
        center = (self.width // 2, self.height // 2)
        self.player_spawn = self._closest(center, open_cells)
        self.super_pacgums = set(self.corners)
        self.pacgums = (open_cells - self.super_pacgums
                        - {self.player_spawn})

# ================================= CAN MOVE ==================================

    def can_move(self, cell: Cell, direction: Cell) -> bool:
        bit = WALL_BITS.get(direction)
        if bit is None:
            return False
        x, y = cell
        nx, ny = x + direction[0], y + direction[1]
        return (0 <= nx < self.width and 0 <= ny < self.height
                and not self.maze[y][x] & bit
                and self.maze[ny][nx] != SOLID)

# ==================================== EAT ====================================

    def eat(self, cell: Cell) -> Eaten:
        if cell in self.pacgums:
            self.pacgums.remove(cell)
            return Eaten.PACGUM
        if cell in self.super_pacgums:
            self.super_pacgums.remove(cell)
            return Eaten.SUPER
        return Eaten.NOTHING

# ================================== CLEARED ==================================

    @property
    def cleared(self) -> bool:
        return not self.pacgums and not self.super_pacgums

# ================================== CLOSEST ==================================

    @staticmethod
    def _closest(target: Cell, cells: set[Cell]) -> Cell:
        return min(cells, key=lambda c: (c[0] - target[0]) ** 2
                   + (c[1] - target[1]) ** 2)
