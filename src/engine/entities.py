

from dataclasses import dataclass
from enum import Enum

from src.engine.algo import Cell, Greddy


# *****************************************************************************
# *                                GHOST STATE                                *
# *                                                                           *

class GhostState(Enum):

    ACTIVE = "active"
    EATEN = "eaten"


# *****************************************************************************
# *                                  PLAYER                                   *
# *                                                                           *

@dataclass
class Player:

    pos: Cell
    spawn: Cell
    direction: Cell = (0, 0)
    wanted: Cell = (0, 0)
    prev: Cell = (0, 0)

# ================================= POST INIT =================================

    def __post_init__(self) -> None:
        self.prev = self.pos

# =================================== RESET ===================================

    def reset(self) -> None:
        self.pos = self.spawn
        self.prev = self.spawn
        self.direction = (0, 0)
        self.wanted = (0, 0)


# *****************************************************************************
# *                                   GHOST                                   *
# *                                                                           *

@dataclass
class Ghost:

    brain: Greddy
    pos: Cell
    home: Cell
    state: GhostState = GhostState.ACTIVE
    respawn_in: float = 0.0
    prev: Cell = (0, 0)

# ================================= POST INIT =================================

    def __post_init__(self) -> None:
        self.prev = self.pos

# =================================== RESET ===================================

    def reset(self) -> None:
        self.pos = self.home
        self.prev = self.home
        self.state = GhostState.ACTIVE
        self.respawn_in = 0.0
        self.brain.reset()
