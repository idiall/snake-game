from __future__ import annotations

from ..types import GridPos
from ..config import GRID_COLS, GRID_ROWS


def wall_collision(head: GridPos) -> bool:
    x, y = head
    return not (0 <= x < GRID_COLS and 0 <= y < GRID_ROWS)


def self_collision(head: GridPos, body_without_head: list[GridPos]) -> bool:
    return head in body_without_head


def food_collision(head: GridPos, food_pos: GridPos) -> bool:
    return head == food_pos
