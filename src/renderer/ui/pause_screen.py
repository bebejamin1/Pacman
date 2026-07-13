import arcade

class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_draw(self):
        self.clear()

        player_sprite = self.game_view.player_sprite
        arcade.draw_sprite(player_sprite)

        arcade.draw_lbwh_rectangle_filled(left=0, bottom=0,
                                          right=SCREEN_WIDTH,
                                          top=SCREEN_HEIGHT,
                                          color=arcade.color.BLACK[:3] + (200,))

        arcade.draw_text("PAUSED", WIDTH / 2, HEIGHT / 2 + 50,
                         arcade.color.WHITE, font_size=50, anchor_x="center")

        arcade.draw_text("Press Esc. to return",
                         WIDTH / 2,
                         HEIGHT / 2,
                         arcade.color.WHITE,
                         font_size=20,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)