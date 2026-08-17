import arcade

from typing import Any
from pathlib import Path
from arcade.types import PathOrTexture

from src.engine.algo import Greddy, Personality, Cell, Mode

ANIM_SPEED = 10
HIT_BOX_HALF_WIDTH = 1
HIT_BOX_HALF_HEIGHT = 1


class Player(arcade.Sprite):
    """Animated player sprite, cycling through its walk textures."""

    def __init__(self, path: PathOrTexture, scale: float,
                 character_animation: list[arcade.Texture]) -> None:
        """Load the player's sprite and its walk animation frames.

        Args:
            path: Initial texture path, or a pre-loaded texture.
            scale: Scale factor applied to the sprite.
            character_animation: Ordered walk-cycle textures.
        """
        super().__init__(path, scale)

        self.curr_texture: int = 0
        self.animation: list[arcade.Texture] = character_animation
        self.timer: float = 0.0

        self.cell: Cell = (0, 0)

        hw, hh = HIT_BOX_HALF_WIDTH, HIT_BOX_HALF_HEIGHT
        self.hit_box = arcade.hitbox.HitBox(
            ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)),
            self.position, self.scale)

    def update_animation(self, delta_time: float = 1 / 60,
                         *args: Any, **kwargs: Any) -> None:
        """Advance the walk-cycle animation by one frame if due.

        Args:
            delta_time: Elapsed time, in seconds, since the last frame.
            *args: Unused, required by Arcade's sprite update signature.
            **kwargs: Unused, required by Arcade's sprite update signature.
        """
        self.timer += delta_time

        if (self.timer > (1 / ANIM_SPEED)):
            self.curr_texture = (self.curr_texture + 1) % len(self.animation)
            self.texture = self.animation[self.curr_texture]

            self.timer = 0.0


class Enemies(arcade.Sprite):
    """Animated ghost sprite, backed by a greedy movement brain."""

    def __init__(self, path: str | Path, flee_texture: str | Path,
                 scale: float, maze: list[list[int]],
                 personality: Personality, home_corner: Cell) -> None:
        """Load the ghost's chase/flee textures and its movement brain.

        Args:
            path: Texture path used while chasing.
            flee_texture: Texture path used while frightened.
            scale: Scale factor applied to the sprite.
            maze: Wall-bitmask grid the ghost moves through.
            personality: Behaviour driving the ghost's target selection.
            home_corner: Cell the ghost spawns at and returns to.
        """
        super().__init__(path, scale)
        self.chase_texture: arcade.Texture = arcade.load_texture(path)
        self.flee_texture: arcade.Texture = arcade.load_texture(flee_texture)

        self.brain: Greddy = Greddy(maze, personality, home_corner)

        self.spawn: Cell = home_corner
        self.cell: Cell = home_corner

        self.eaten: bool = False

        self.respawn_timer: float = 0.0

    def update_sprite(self, flee: bool) -> None:
        """Switch between the chase and flee textures.

        Args:
            flee: Whether the ghost is currently frightened.
        """
        if flee:
            self.texture = self.flee_texture
        else:
            self.texture = self.chase_texture

    def next_move(self, player_pos: Cell, player_dir: Cell = (0, 0),
                  mode: Mode = Mode.CHASE) -> Cell:
        """Ask the movement brain for the next cell and update state.

        Args:
            player_pos: Player's current cell.
            player_dir: Player's current movement direction.
            mode: Current ghost mode (chase or frightened).

        Returns:
            The cell the ghost is now moving to.
        """
        self.cell = self.brain.next_move(
            self.cell, player_pos, player_dir, mode)

        return self.cell
