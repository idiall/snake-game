from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Set

from ..config import GRID_COLS, GRID_ROWS
from ..types import GridPos


@dataclass(slots=True)
class Food:
    pos: GridPos

    @staticmethod
    def random(exclude: Set[GridPos]) -> "Food":
        # Simple random placement avoiding excluded cells
        while True:
            p = (random.randint(0, GRID_COLS - 1), random.randint(0, GRID_ROWS - 1))
            if p not in exclude:
                return Food(pos=p)
