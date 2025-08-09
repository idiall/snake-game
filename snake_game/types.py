from __future__ import annotations

from enum import Enum, auto
from typing import NewType, Tuple

# Basic typed aliases for clarity
GridPos = Tuple[int, int]  # (col, row) on the grid


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

    def opposite(self) -> "Direction":
        if self is Direction.UP:
            return Direction.DOWN
        if self is Direction.DOWN:
            return Direction.UP
        if self is Direction.LEFT:
            return Direction.RIGHT
        return Direction.LEFT

    @staticmethod
    def from_key(key: int) -> "Direction | None":
        import pygame as pg

        mapping = {
            pg.K_UP: Direction.UP,
            pg.K_w: Direction.UP,
            pg.K_DOWN: Direction.DOWN,
            pg.K_s: Direction.DOWN,
            pg.K_LEFT: Direction.LEFT,
            pg.K_a: Direction.LEFT,
            pg.K_RIGHT: Direction.RIGHT,
            pg.K_d: Direction.RIGHT,
        }
        return mapping.get(key)
