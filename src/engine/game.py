"""Cheat-mode toggles, shared between the game view and the cheat menu."""

from dataclasses import dataclass


@dataclass
class Cheats:
    """Cheat-mode toggles, used for peer review purposes."""

    invincible: bool = False
    freeze_ghosts: bool = False
    speed_boost: bool = False
