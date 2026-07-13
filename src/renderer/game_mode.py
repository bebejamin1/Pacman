import arcade

# ----| CONSTANTS |---- #
WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 1080
WINDOW_TITLE = "PAC-MAN"

PATH = "src/assets/"
SPRITE_SIZE = 24
CHARACTER_SIZE = 1
CHARACTER_SPEED = 2


class Game(arcade.Window):
    """
    This class will show the game and make the user
    able to control the character's movement.
    """

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            arcade.close_window()

        elif symbol == arcade.key.UP or symbol == arcade.key.W:
            self.player.change_y += CHARACTER_SPEED
        elif symbol == arcade.key.DOWN or symbol == arcade.key.S:
            self.player.change_y -= CHARACTER_SPEED
        elif symbol == arcade.key.LEFT or symbol == arcade.key.A:
            self.player.change_x -= CHARACTER_SPEED
            self.player.scale_x = (-1 * CHARACTER_SIZE)
        elif symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.player.change_x += CHARACTER_SPEED
            self.player.scale_x = CHARACTER_SIZE

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.UP or symbol == arcade.key.W:
            self.player.change_y = 0
        elif symbol == arcade.key.DOWN or symbol == arcade.key.S:
            self.player.change_y = 0
        elif symbol == arcade.key.LEFT or symbol == arcade.key.A:
            self.player.change_x = 0
        elif symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.player.change_x = 0