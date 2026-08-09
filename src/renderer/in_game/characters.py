import arcade

from typing import Any
from arcade.types import PathOrTexture

from src.engine.algo import Greddy, Personality, Cell, Mode

# ----| CONSTANTS |---- #
ANIM_SPEED = 5
# --------------------- #


class Player(arcade.Sprite):
    """
    This class will show the player animated sprites.
    """
    def __init__(self, path: PathOrTexture, scale: float,
                 character_animation: list[arcade.Texture]) -> None:
        super().__init__(path, scale)

        self.curr_texture: int = 0
        self.animation: list[arcade.Texture] = character_animation
        self.timer: float = 0.0

    def update_animation(self, delta_time: float = 1 / 60,
                         *args: Any, **kwargs: Any) -> None:
        self.timer += delta_time

        if self.timer > (1 / ANIM_SPEED):
            self.curr_texture = (self.curr_texture + 1) % len(self.animation)
            self.texture = self.animation[self.curr_texture]

            self.timer = 0.0


class Enemies(arcade.Sprite):
    """
    This class will show the enemy animated sprites.
    """
    def __init__(self, path: PathOrTexture, scale: float,
                 character_animation: list[arcade.Texture],
                 maze: list[list[int]], personality: Personality,
                 home_corner: Cell) -> None:
        super().__init__(path, scale)

        self.curr_texture: int = 0
        self.animation: list[arcade.Texture] = character_animation
        self.timer: float = 0.0

        self.brain: Greddy = Greddy(maze, personality, home_corner)
        self.spawn: Cell = home_corner

    def update_animation(self, delta_time: float = 1 / 60,
                         *args: Any, **kwargs: Any) -> None:
        self.timer += delta_time

        if self.timer > (1 / ANIM_SPEED):
            self.curr_texture = (self.curr_texture + 1) % len(self.animation)
            self.texture = self.animation[self.curr_texture]

            self.timer = 0.0

    def next_move(self, player_pos: Cell, player_dir: Cell = (0, 0),
             mode: Mode = Mode.CHASE) -> Cell:
        self.cell: Cell = self.brain.next_move(self.spawn, player_pos,
                                               player_dir, mode)

        return self.cell
