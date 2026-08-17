"""Data classes for the player and ghost entities used by the engine."""

from dataclasses import dataclass
from enum import Enum

from src.engine.algo import Cell, Greddy


class GhostState(Enum):
    """Lifecycle state of a ghost."""

    ACTIVE = "active"
    EATEN = "eaten"


@dataclass
class Player:
    """Player entity: position, spawn point and movement state."""

    pos: Cell
    spawn: Cell
    direction: Cell = (0, 0)
    wanted: Cell = (0, 0)
    prev: Cell = (0, 0)

    def __post_init__(self) -> None:
        """Initialize the previous position to the starting position."""
        self.prev = self.pos

    def reset(self) -> None:
        """Move the player back to its spawn point, direction cleared."""
        self.pos = self.spawn
        self.prev = self.spawn
        self.direction = (0, 0)
        self.wanted = (0, 0)


@dataclass
class Ghost:
    """Ghost entity: movement brain, position, home corner and state."""

    brain: Greddy
    pos: Cell
    home: Cell
    state: GhostState = GhostState.ACTIVE
    respawn_in: float = 0.0
    prev: Cell = (0, 0)

    def __post_init__(self) -> None:
        """Initialize the previous position to the starting position."""
        self.prev = self.pos

    def reset(self) -> None:
        """Move the ghost back to its home corner, active and ready."""
        self.pos = self.home
        self.prev = self.home
        self.state = GhostState.ACTIVE
        self.respawn_in = 0.0
        self.brain.reset()
