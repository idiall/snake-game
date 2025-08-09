from __future__ import annotations

import sys
import argparse
import time
from dataclasses import dataclass

import pygame as pg

from . import __version__
from .config import (
    HEIGHT,
    MAX_FPS,
    TICK_RATE,
    TITLE,
    WIDTH,
    SPEED_STEP,
    SPEED_SCORE_STEP,
    SPEED_MAX,
)
from .core.game import Game


@dataclass(slots=True)
class ClockConfig:
    tick_rate: int = TICK_RATE
    max_fps: int = MAX_FPS


class App:
    def __init__(self, clock_cfg: ClockConfig) -> None:
        self.clock_cfg = clock_cfg
        self.screen: pg.Surface
        self.clock = pg.time.Clock()
        self._accumulator = 0.0
        self._dt = 1.0 / float(self.clock_cfg.tick_rate)
        self._running = True
        self.game: Game | None = None

    def init(self) -> None:
        pg.display.set_caption(f"{TITLE} v{__version__}")
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        parser = argparse.ArgumentParser(description="Snake Game")
        parser.add_argument("--tick", type=int, default=TICK_RATE, help="Base tick rate (updates per second)")
        parser.add_argument("--speed-step", type=int, default=SPEED_STEP, help="Increase in tick rate per threshold")
        parser.add_argument(
            "--speed-score-step", type=int, default=SPEED_SCORE_STEP, help="Score threshold for each speed increase"
        )
        parser.add_argument("--speed-max", type=int, default=SPEED_MAX, help="Maximum tick rate cap")
        args = parser.parse_args()
        self.game = Game(
            self.screen,
            base_tick_rate=args.tick,
            speed_step=args.speed_step,
            speed_score_step=args.speed_score_step,
            speed_max=args.speed_max,
        )

    def handle_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self._running = False
            else:
                # Forward all other events to the game (for input handling)
                assert self.game is not None
                self.game.handle_event(event)

    def update(self, dt: float) -> None:
        assert self.game is not None
        self.game.update(dt)

    def render(self) -> None:
        assert self.game is not None
        self.game.render()

    def run(self) -> None:
        self.init()
        prev = time.perf_counter()
        while self._running:
            now = time.perf_counter()
            frame_time = max(0.0, min(now - prev, 0.25))  # clamp to avoid spiral of death
            prev = now

            self._accumulator += frame_time
            self.handle_events()

            # Recompute fixed timestep from current game speed (score-based)
            assert self.game is not None
            self._dt = 1.0 / float(self.game.get_tick_rate())

            while self._accumulator >= self._dt:
                self.update(self._dt)
                self._accumulator -= self._dt

            self.render()
            self.clock.tick(self.clock_cfg.max_fps)


def main() -> int:
    pg.init()
    try:
        App(ClockConfig()).run()
        return 0
    finally:
        pg.quit()


if __name__ == "__main__":
    sys.exit(main())
