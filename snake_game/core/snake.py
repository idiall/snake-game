from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque, Iterable, Set

from ..config import GRID_COLS, GRID_ROWS
from ..types import Direction, GridPos


@dataclass(slots=True)
class Snake:
    body: Deque[GridPos]
    direction: Direction
    grow_pending: int = 0

    def __init__(self, start: GridPos, length: int = 3, direction: Direction = Direction.RIGHT) -> None:
        self.direction = direction
        # Initial body extends to the left from start
        self.body = deque((start[0] - i, start[1]) for i in range(length))
        self.grow_pending = 0

    @property
    def head(self) -> GridPos:
        return self.body[0]

    @property
    def cells(self) -> Set[GridPos]:
        return set(self.body)

    def change_direction(self, new_dir: Direction) -> None:
        # Prevent reversing directly into itself
        if new_dir is not None and new_dir is not self.direction.opposite() and new_dir is not self.direction:
            self.direction = new_dir

    def step(self) -> GridPos:
        hx, hy = self.head
        if self.direction is Direction.UP:
            new_head = (hx, hy - 1)
        elif self.direction is Direction.DOWN:
            new_head = (hx, hy + 1)
        elif self.direction is Direction.LEFT:
            new_head = (hx - 1, hy)
        else:
            new_head = (hx + 1, hy)

        self.body.appendleft(new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()
        return new_head

    def grow(self, amount: int = 1) -> None:
        self.grow_pending += amount

    def hits_wall(self) -> bool:
        x, y = self.head
        return not (0 <= x < GRID_COLS and 0 <= y < GRID_ROWS)

    def hits_self(self) -> bool:
        head = self.head
        # If duplicates exist, head collides with body
        return head in list(self.body)[1:]
