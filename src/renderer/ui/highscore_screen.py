import os
import arcade

# ----| CONSTANTS |---- #
PATH = "assets/menu/main/"
# --------------------- #

class HighscoreView(arcade.View):
    
    def __init__(self) -> None:
        super().__init__()
        from src.renderer.game_engine import GameEngine
        self.window = GameEngine()
        
        # Loads the background
        try:
            if not os.path.exists("assets/"):
                raise ValueError

            self.background: arcade.Texture
            self.background = arcade.load_texture(f"{PATH}main_menu.png")
        except FileNotFoundError:
                raise ValueError("\033[1;91mBackground file not found!\033[0m")

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            self.window.switch_menu()

    def on_draw(self) -> None:
        self.clear()

        # Draws the background
        arcade.draw_texture_rect(self.background, 
                                 arcade.LBWH(0, 0, self.width, self.height))
