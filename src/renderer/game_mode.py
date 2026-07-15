import os
import arcade

from typing import Any

from src.renderer.in_game.characters import Character
from src.renderer.in_game.sprite import Object

from src.parsing.parse import parse_conf

# ----| CONSTANTS |---- #
WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 1080
WINDOW_TITLE = "PAC-MAN"

PATH = "assets/background/"
PLAYER_PATH = "assets/player/"
MAZE_PATH = "assets/maze/"
SPRITE_SIZE = 24
CHARACTER_SIZE = 1
CHARACTER_SPEED = 2
# --------------------- #

class GameView(arcade.View):
    """
    This class will show the game and make the user
    able to control the character's movement.
    """
    def __init__(self) -> None:
        super().__init__()
        self.config = parse_conf("data/config.json")
        self.total_time = self.config[1].get("level_max_time")

        self.maze: list[dict[str, Any]] = self.config[1].get("level")

        self.player_list: arcade.SpriteList[arcade.Sprite] = \
            arcade.SpriteList()

        self.enemy_list: arcade.SpriteList[arcade.Sprite] = \
            arcade.SpriteList()

        self.wall_list: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        self.ground_list: arcade.SpriteList[arcade.Sprite] = \
            arcade.SpriteList()

        self.pacgum: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        self.super_pac: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()

        # self._build_walls()
        self._load_sprite()
        self._load_hud()
        # self.physic_engine = arcade.PhysicsEngineSimple(self.player,
        #                                                 self.wall_list)

    def on_draw(self) -> None:
        self.clear()

        arcade.draw_texture_rect(self.background, arcade.LBWH(0, 0, 
                                                              self.width,
                                                              self.height))

        # Draws the HUD
        self.level_text.draw()
        self.timer_text.draw()
        self.life_text.draw()
        self.score_text.draw()
        self.text.draw()

    def on_update(self, delta_time: float) -> None:
        # self.physic_engine.update()
        # pacgum_hit = arcade.check_for_collision_with_list(self.player,
        #                                                   self.pacgum)
        # super_pac_hit = arcade.check_for_collision_with_list(self.player,
        #                                                      self.super_pac)
        
        # enemy_hit = arcade.check_for_collision_with_list(self.player,
        #                                                  self.enemy)

        # Updated timer
        self.time_elapsed -= delta_time
        minutes = int(self.time_elapsed // 60)
        seconds = int(self.time_elapsed % 60)
        self.timer_text.text = f"{minutes:02d}:{seconds:02d}"

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            self.window.switch_menu()

        if symbol == arcade.key.SPACE:
            self.window.switch_pause()

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

    def _load_hud(self) -> None:
        self.life = self.config[1].get("live")
        self.score = 0
        self.level = self.maze[0].get("name")

        self.level_text = arcade.Text(text=f"{self.level}",
                                 x=WINDOW_WIDTH / 2, y=WINDOW_HEIGHT - 50,
                                 color=arcade.color.LAVENDER,
                                 font_size=25, anchor_x="center", 
                                 font_name="Public Pixel")
                                 
        self.timer_text = arcade.Text(text="00:00",
                                      x=WINDOW_WIDTH / 2, y=WINDOW_HEIGHT - 100,
                                      color=arcade.color.LAVENDER,
                                      font_size=20, anchor_x="center", 
                                      font_name="Public Pixel")
        self.time_elapsed = self.config[1].get("level_max_time")

        self.life_text = arcade.Text(text=f"x{self.life}",
                                x=50, y=WINDOW_HEIGHT - 50,
                                color=arcade.color.LAVENDER,
                                font_size=25, anchor_x="left", 
                                font_name="Public Pixel")
        
        self.score_text = arcade.Text(text=f"{self.score}",
                                 x=WINDOW_WIDTH - 50, y=WINDOW_HEIGHT - 50,
                                 color=arcade.color.LAVENDER,
                                 font_size=25, anchor_x="right", 
                                 font_name="Public Pixel")

        self.text = arcade.Text(text="Press SPACE to pause",
                                x=WINDOW_WIDTH / 2, y=100,
                                color=arcade.color.LAVENDER,
                                font_size=10, anchor_x="center", 
                                font_name="Public Pixel")

    # def _build_walls(self, x: float, y: float) -> None:
    #     try:
    #         front_wall = Object(f"{MAZE_PATH}front_wall.png", 1)
    #     except FileNotFoundError:
    #         raise ValueError("\033[1;91mError: wall asset not found\033[0m")
    #     front_wall.center_x = x * SPRITE_SIZE + (SPRITE_SIZE / 2) + OFFSET_X
    #     front_wall.center_y = ((WINDOW_HEIGHT - 100) - (y * SPRITE_SIZE) -
    #                      (SPRITE_SIZE / 2) + OFFSET_Y)
    #     self.wall_list.append(wall)

    def _load_sprite(self) -> None:
        try:
            if not os.path.exists("assets/"):
                raise ValueError

            self.background = arcade.load_texture(f"{PATH}maze_back.png")

            # character_animation = [
            #     arcade.load_texture(f"{PLAYER_PATH}character1.png"),
            #     arcade.load_texture(f"{PLAYER_PATH}character2.png"),
            #     arcade.load_texture(f"{PLAYER_PATH}character3.png"),
            #     arcade.load_texture(f"{PLAYER_PATH}character4.png"),
            # ]

            # self.player = Character(f"{PLAYER_PATH}character1.png", CHARACTER_SIZE,
            #                         character_animation)
            # self.player.center_x = (((self.maze.entry_x * SPRITE_SIZE) +
            #                         (SPRITE_SIZE / 2)) + OFFSET_X)
            # self.player.center_y = (((WINDOW_HEIGHT - 100) -
            #                         (self.maze.entry_y * SPRITE_SIZE) -
            #                         (SPRITE_SIZE / 2)) + OFFSET_Y)
            # self.player_list.append(self.player)

        except FileNotFoundError:
            raise ValueError("\033[1;91mError: player asset not found\033[0m")
