import arcade
from arcade.types import PathOrTexture


class Object(arcade.Sprite):
    """Static sprite used for maze tiles and collectibles.

    Shared by walls, ground tiles, pacgums and super-pacgums, which are
    all plain, non-animated textures placed on the maze grid.
    """

    def __init__(self, path: PathOrTexture, scale: float,
                 angle: float) -> None:
        """Load the texture and place it at the given scale and angle.

        Args:
            path: Path to the sprite's texture, or a pre-loaded texture.
            scale: Scale factor applied to the texture.
            angle: Rotation angle, in degrees.
        """
        super().__init__(path, scale, angle)
