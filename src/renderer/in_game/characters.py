import arcade

from typing import Any
from pathlib import Path
from arcade.types import PathOrTexture

from src.engine.algo import Greddy, Personality, Cell, Mode

# ----| CONSTANTS |---- #
ANIM_SPEED = 10
HIT_BOX_HALF_WIDTH = 45.0  # ne pas mettre 50 sinon il traverse
HIT_BOX_HALF_HEIGHT = 45.0
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

        self.cell: Cell = (0, 0)  # ajout: la case des fantomes

        hw, hh = HIT_BOX_HALF_WIDTH, HIT_BOX_HALF_HEIGHT
        self.hit_box = arcade.hitbox.HitBox(
            ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)),
            self.position, self.scale)

    def update_animation(self, delta_time: float = 1 / 60,
                         *args: Any, **kwargs: Any) -> None:
        self.timer += delta_time

        if (self.timer > (1 / ANIM_SPEED)):
            self.curr_texture = (self.curr_texture + 1) % len(self.animation)
            self.texture = self.animation[self.curr_texture]

            self.timer = 0.0


class Enemies(arcade.Sprite):
    """
    This class will show the enemy animated sprites.
    """
    def __init__(self, path: str | Path, flee_texture: str | Path,
                 scale: float, maze: list[list[int]],
                 personality: Personality, home_corner: Cell) -> None:
        super().__init__(path, scale)
        self.chase_texture: arcade.Texture = arcade.load_texture(path)
        self.flee_texture: arcade.Texture = arcade.load_texture(flee_texture)

        self.brain: Greddy = Greddy(maze, personality, home_corner)

        self.spawn: Cell = home_corner
        self.cell: Cell = home_corner

        self.eaten: bool = False

        self.respawn_timer: float = 0.0

    def update_sprite(self, flee: bool) -> None:
        if flee:
            self.texture = self.flee_texture
        else:
            self.texture = self.chase_texture

    def next_move(self, player_pos: Cell, player_dir: Cell = (0, 0),
                  mode: Mode = Mode.CHASE) -> Cell:
        self.cell = self.brain.next_move(
            self.cell, player_pos, player_dir, mode)

        return self.cell
