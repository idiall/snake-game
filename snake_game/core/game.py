from __future__ import annotations

from dataclasses import dataclass

import pygame as pg

from ..config import GRID_COLS, GRID_ROWS, TICK_RATE, SPEED_STEP, SPEED_SCORE_STEP, SPEED_MAX
from ..types import Direction
from ..persistence import load_high_score, save_high_score
from .food import Food
from .input import Input
from .renderer import Renderer
from .snake import Snake


@dataclass(slots=True)
class GameState:
    snake: Snake
    food: Food
    score: int
    high_score: int
    game_over: bool = False


class Game:
    def __init__(
        self,
        screen: pg.Surface,
        base_tick_rate: int = TICK_RATE,
        speed_step: int = SPEED_STEP,
        speed_score_step: int = SPEED_SCORE_STEP,
        speed_max: int = SPEED_MAX,
    ) -> None:
        self.screen = screen
        self.renderer = Renderer(screen)
        self.input = Input()
        self.state = self._new_game()
        # Speed configuration (can be overridden by CLI)
        self._base_tick_rate = int(base_tick_rate)
        self._speed_step = int(speed_step)
        self._speed_score_step = int(speed_score_step)
        self._speed_max = int(speed_max)

    def _new_game(self) -> GameState:
        start = (GRID_COLS // 2, GRID_ROWS // 2)
        snake = Snake(start=start, length=3, direction=Direction.RIGHT)
        food = Food.random(exclude=snake.cells)
        # Keep previous high score if state exists; otherwise load from disk
        previous_high = getattr(self, "state", None).high_score if hasattr(self, "state") else None
        high = previous_high if isinstance(previous_high, int) else load_high_score()
        return GameState(snake=snake, food=food, score=0, high_score=high, game_over=False)

    def handle_event(self, event: pg.event.Event) -> None:
        if self.state.game_over:
            if event.type == pg.KEYDOWN and event.key == pg.K_r:
                self.state = self._new_game()
            return
        self.input.process_event(event)

    def update(self, dt: float) -> None:
        if self.state.game_over:
            return

        new_dir = self.input.consume_direction()
        if new_dir is not None:
            self.state.snake.change_direction(new_dir)

        head = self.state.snake.step()

        # Collisions
        if self.state.snake.hits_wall() or self.state.snake.hits_self():
            self.state.game_over = True
            # Update high score if applicable and persist
            if self.state.score > self.state.high_score:
                self.state.high_score = self.state.score
                save_high_score(self.state.high_score)
            return

        if head == self.state.food.pos:
            self.state.score += 1
            self.state.snake.grow(1)
            self.state.food = Food.random(exclude=self.state.snake.cells)

    def render(self) -> None:
        self.renderer.draw_grid()
        self.renderer.draw_snake(list(self.state.snake.body), self.state.snake.direction)
        self.renderer.draw_food(self.state.food.pos)
        self.renderer.draw_hud(self.state.score, self.state.high_score)
        if self.state.game_over:
            self.renderer.draw_game_over(self.state.score, self.state.high_score)
        pg.display.flip()

    def get_tick_rate(self) -> int:
        # Increase tick rate by configured step every configured score threshold
        inc = (self.state.score // self._speed_score_step) * self._speed_step
        return min(self._base_tick_rate + inc, self._speed_max)
