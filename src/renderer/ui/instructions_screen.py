import os
import arcade

# ----| CONSTANTS |---- #
PATH = "assets/menu/main/"
FONT_PATH = "assets/font/"
# --------------------- #

class InstructionsView(arcade.View):
    """
    This class will display the game's control and instructions.
    """
    def __init__(self) -> None:
        super().__init__()
        self.text_list: list[arcade.Text] = []

        # Loads the background
        try:
            if not os.path.exists("assets/"):
                raise ValueError

            self.background: arcade.Texture = \
                arcade.load_texture(f"{PATH}main_menu.png")
            arcade.load_font(f"{FONT_PATH}PublicPixel.ttf")

        except FileNotFoundError:
            raise ValueError("\033[1;91mBackground file not found!\033[0m")
        
        self.game_instructions()

    def game_instructions(self) -> None:
        # Controls during the game
        commands = arcade.Text(text="Commands:", x=30, y=770,
                               color=arcade.color.BLACK, font_size=30,
                               align="left", font_name="Public Pixel")

        play = arcade.Text(text="- Play with WASD or the arrows", x=30,
                           y=700, color=arcade.color.BLACK, font_size=20,
                           align="left", font_name="Public Pixel")

        pause = arcade.Text(text="- Press SPACE to pause", x=30, y=650,
                            color=arcade.color.BLACK, font_size=20,
                            align="left", font_name="Public Pixel")

        quit = arcade.Text(text="- Press ESC to quit", x=30, y=600,
                           color=arcade.color.BLACK, font_size=20,
                           align="left", font_name="Public Pixel")

        self.text_list.append(commands)
        self.text_list.append(play)
        self.text_list.append(pause)
        self.text_list.append(quit)

        # Rules of the game
        rules = arcade.Text(text="Rules:", x=30, y=530,
                            color=arcade.color.BLACK, font_size=28,
                            align="left", font_name="Public Pixel")

        rule1 = arcade.Text(text="- The Minotaur avoids humans", x=30,
                            y=460, color=arcade.color.BLACK, font_size=20,
                            align="left", font_name="Public Pixel")

        rule2 = arcade.Text(text="- Bones gives points", x=30, y=410,
                            color=arcade.color.BLACK, font_size=20,
                            align="left", font_name="Public Pixel")

        rule3 = arcade.Text(text="- Axes gives more points and", x=30,
                            y=360, color=arcade.color.BLACK, font_size=20,
                            align="left", font_name="Public Pixel")

        rule4 = arcade.Text(text="gives the ability to eat humans", x=30,
                            y=310, color=arcade.color.BLACK, font_size=20,
                            align="left", font_name="Public Pixel")

        self.text_list.append(rules)
        self.text_list.append(rule1)
        self.text_list.append(rule2)
        self.text_list.append(rule3)
        self.text_list.append(rule4)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            self.window.switch_menu()

    def on_draw(self) -> None:
        self.clear()

        # Draws the background
        arcade.draw_texture_rect(self.background, 
                                 arcade.LBWH(0, 0, self.width, self.height))

        # Prints the instructions
        for text in self.text_list:
            text.draw()
