import arcade
from arcade.types import PathOrTexture

class Object(arcade.Sprite):
    """
    This class will show the objects (different gums as
    well as the wall and ground) animated sprites.
    """
    def __init__(self, path: PathOrTexture, scale: float) -> None:
        super().__init__(path, scale)
