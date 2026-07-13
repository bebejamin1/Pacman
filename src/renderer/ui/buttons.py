import arcade

from abc import ABC, abstractmethod

class BaseButton(arcade.Sprite, ABC):
    """
    An abstract base class used to define the buttons action.
    """
    @abstractmethod
    def on_click(self) -> None:
        pass


class StartButton(BaseButton):
    """
    A button that start the game.
    """
    def __init__(self, center_x: float, center_y: float, 
                 texture: arcade.Sprite, view: arcade.View) -> None:
        super().__init__(center_x, center_y, path, view)
        
    def on_click(self) -> None:
        print("Game Start!")


class InstructionButton(BaseButton):
    """
    A button that shows the game's instructions.
    """
    def __init__(self, center_x: float, center_y: float,
                 texture: arcade.Sprite, view: arcade.View) -> None:
        super().__init__(center_x, center_y, path, view)

    def on_click(self) -> None:
        if self.view.window:
            self.view.window.show_view()


class HighscoreButton(BaseButton):
    """
    A button that shows the game's leaderboard.
    """
    def __init__(self, center_x: float, center_y: float,
                 texture: arcade.Sprite, view: arcade.View) -> None:
        super().__init__(center_x, center_y, path, view)

    def on_click(self) -> None:
        if self.view.window:
            self.view.window.show_view()


class ExitButton(BaseButton):
    """
    A button that quits the game.
    """
    def __init__(self, center_x: float, center_y: float,
                 texture: arcade.Sprite, view: arcade.View) -> None:
        super().__init__(center_x, center_y, path, view)

    def on_click(self) -> None:
        arcade.exit()