

import os
import arcade

from typing import Any

from src.renderer.in_game.maze import Maze
from src.renderer.in_game.characters import Character

from src.parsing.parse import parse_conf

# ----| CONSTANTS |---- #
PATH = "assets/background/"
MAZE_PATH = "assets/maze/"

CHARACTER_SIZE = 0.65
# --------------------- #


class GameView(arcade.View):
    """
    This class will show the game and make the user
    able to control the character's movement.
    """
    def __init__(self) -> None:
        super().__init__()
        self.config: list[Any] = parse_conf("data/config.json")
        self.seed: int = self.config[1].get("seed")
        self.total_time: int = self.config[1].get("level_max_time")
        self.lvl: list[dict[str, Any]] = self.config[1].get("level")
        self.lvl_nb: int = 0

        self.rules: dict[str, Any] = self.config[1]
        self.lives: int = self.rules.get("live")
        self.flee: bool = False

        self.speed: float = 2

        self._maze_generation()
        self._collectibles()
        self._load_sprite()
        self._load_hud()

        self.player: Character = self.maze.player

        self.enemy_list: arcade.SpriteList[arcade.Sprite] = \
            arcade.SpriteList()

        self.physic_engine = arcade.PhysicsEngineSimple(self.player,
                                                        self.maze.wall_list)

    def on_draw(self) -> None:
        self.clear()

        arcade.draw_texture_rect(self.background, arcade.LBWH(0, 0,
                                                              self.width,
                                                              self.height))

        # Draws the maze and its collectibles
        self.maze.ground_list.draw()
        self.maze.wall_list.draw()
        self.maze.pacgum_list.draw()
        self.maze.super_pac.draw()

        # Draws entities
        self.maze.player_list.draw()

        # Draws the HUD
        self.level_text.draw()
        self.timer_text.draw()
        self.life_text.draw()
        self.score_text.draw()
        self.text.draw()

    def on_update(self, delta_time: float) -> None:
        # Updates entities
        self.maze.player_list.update()

        # Makes the physics of the game
        self.physic_engine.update()

        # Entities animations
        self.player.update_animation(delta_time * 2, None, None)

        # Checks the collisions with collectibles
        pac_hit = arcade.check_for_collision_with_list(self.player,
                                                       self.maze.pacgum_list)
        if pac_hit:
            for p in pac_hit:
                self.score += self.rules.get("pacgum_points")
                self.score_text.text = self.score
                p.kill()

                if len(self.maze.pacgum_list) == 0:
                    if len(self.lvl) >= self.lvl_nb:
                        self.lvl_nb += 1

                        lvl_width: int = self.lvl[self.lvl_nb]["width"]
                        lvl_height: int = self.lvl[self.lvl_nb]["height"]

                        self.next_level(lvl_width, lvl_height)

                    else:
                        self.window.switch_end(True, self.score)

        sup_pac_hit = arcade.check_for_collision_with_list(self.player,
                                                           self.maze.super_pac)
        if sup_pac_hit:
            for p in sup_pac_hit:
                self.score += self.rules.get("super_pacgum_points")
                self.score_text.text = self.score
                p.kill()
                self.flee = True

        # Checks the collisions with other entities
        # enemy_hit = arcade.check_for_collision_with_list(self.player,
        #                                                  self.enemy)
        # if enemy_hit:
        #     if self.flee is True:
        #         self.score += self.rules.get("ghost_points")
        #         self.score_text.text = self.score
        #     else:
        #         self.lives -= 1
        #         if self.lives == 0:
        #             self.window.switch_end()
        #         else:
        #             restart level function

        # Updates the countdown
        self.time_elapsed -= delta_time
        minutes = int(self.time_elapsed // 60)
        seconds = int(self.time_elapsed % 60)
        self.timer_text.text = f"{minutes:02d}:{seconds:02d}"

        if "-" in self.timer_text.text:
            self.window.switch_end(False, self.score)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.ESCAPE:
            self.window.switch_menu()

        if symbol == arcade.key.SPACE:
            self.window.switch_pause()

        if symbol == arcade.key.C:
            self.window.switch_cheat()

        elif symbol == arcade.key.UP or symbol == arcade.key.W:
            self.player.change_y += self.speed
        elif symbol == arcade.key.DOWN or symbol == arcade.key.S:
            self.player.change_y -= self.speed
        elif symbol == arcade.key.LEFT or symbol == arcade.key.A:
            self.player.change_x -= self.speed
            self.player.scale_x = (CHARACTER_SIZE * -0.5)
        elif symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.player.change_x += self.speed
            self.player.scale_x = (CHARACTER_SIZE * 0.5)

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
        self.level = self.lvl[self.lvl_nb].get("name")

        self.level_text = arcade.Text(
            text=f"{self.level}",
            x=self.width / 2, y=self.height - 50,
            color=arcade.color.LAVENDER,
            font_size=25, anchor_x="center",
            font_name="Public Pixel"
                                     )

        self.timer_text = arcade.Text(
            text="00:00",
            x=self.width / 2, y=self.height - 85,
            color=arcade.color.LAVENDER,
            font_size=20, anchor_x="center",
            font_name="Public Pixel"
                                    )
        self.time_elapsed = self.config[1].get("level_max_time")

        self.life_text = arcade.Text(
            text=f"x{self.life}",
            x=50, y=self.height - 50,
            color=arcade.color.LAVENDER,
            font_size=25, anchor_x="left",
            font_name="Public Pixel"
                                    )

        self.score_text = arcade.Text(
            text=f"{self.score}",
            x=self.width - 50, y=self.height - 50,
            color=arcade.color.LAVENDER,
            font_size=25, anchor_x="right",
            font_name="Public Pixel"
                                     )

        self.text = arcade.Text(
            text="Press SPACE to pause",
            x=self.width / 2, y=100,
            color=arcade.color.LAVENDER,
            font_size=10, anchor_x="center",
            font_name="Public Pixel"
                               )

    def _maze_generation(self) -> None:
        self.game = self.window.new_game(self.config[1], self.lvl)

        self.maze: Maze = Maze(self.config[1], self.lvl_nb,
                               self.window.first_maze,
                               self.width, self.height)
        self.maze.generate_maze()

    def next_level(self, width: int, height: int) -> None:
        self.next_maze: list[list[int]] = self.window.new_maze((width,
                                                                height),
                                                               self.seed)

        self.maze = Maze(self.config[1], self.lvl_nb, self.next_maze,
                         self.width, self.height)
        self.maze.generate_maze()

        self.time_elapsed = self.config[1].get("level_max_time")

    def _collectibles(self) -> None:
        self.pacgum: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        self.super_pac: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()

    def _load_sprite(self) -> None:
        try:
            if not os.path.exists("assets/"):
                raise ValueError

            self.background = arcade.load_texture(f"{PATH}maze_back.png")

            self.wall = arcade.load_texture(f"{MAZE_PATH}front_wall.png")
            self.ground = arcade.load_texture(f"{MAZE_PATH}ground.png")

            self.maze._load_player()

        except FileNotFoundError:
            raise ValueError("\033[1;91mError: Assets folder not found\033[0m")
