from __future__ import annotations

import pygame as pg

from ..types import Direction


class Input:
    def __init__(self) -> None:
        self.pending: Direction | None = None

    def process_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            new_dir = Direction.from_key(event.key)
            if new_dir is not None:
                self.pending = new_dir

    def consume_direction(self) -> Direction | None:
        d = self.pending
        self.pending = None
        return d
