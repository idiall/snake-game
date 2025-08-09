from __future__ import annotations

import pygame as pg

from ..config import (
    CELL_SIZE,
    COLOR_BG,
    COLOR_FOOD,
    COLOR_GRID,
    COLOR_SNAKE,
    COLOR_SNAKE_HEAD,
    COLOR_SNAKE_EYE,
    COLOR_TEXT,
    HEIGHT,
    WIDTH,
)
from ..types import GridPos


class Renderer:
    def __init__(self, screen: pg.Surface) -> None:
        self.screen = screen
        self.font = pg.font.SysFont(None, 24)
        self.title_font = pg.font.SysFont(None, 36)

    def draw_grid(self) -> None:
        self.screen.fill(COLOR_BG)
        # Subtle grid lines
        for x in range(0, WIDTH, CELL_SIZE):
            pg.draw.line(self.screen, COLOR_GRID, (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, CELL_SIZE):
            pg.draw.line(self.screen, COLOR_GRID, (0, y), (WIDTH, y), 1)

    def draw_snake(self, cells: list[GridPos], direction) -> None:
        if not cells:
            return
        pad = max(2, CELL_SIZE // 8)  # small gap between segments
        radius = max(4, CELL_SIZE // 4)

        # Draw body (excluding head)
        for (cx, cy) in cells[1:]:
            rect = pg.Rect(cx * CELL_SIZE + pad, cy * CELL_SIZE + pad, CELL_SIZE - 2 * pad, CELL_SIZE - 2 * pad)
            pg.draw.rect(self.screen, COLOR_SNAKE, rect, border_radius=radius)

        # Draw head with distinct color
        hx, hy = cells[0]
        head_rect = pg.Rect(hx * CELL_SIZE + pad, hy * CELL_SIZE + pad, CELL_SIZE - 2 * pad, CELL_SIZE - 2 * pad)
        pg.draw.rect(self.screen, COLOR_SNAKE_HEAD, head_rect, border_radius=radius)

        # Eyes placement based on direction
        ex = head_rect.x
        ey = head_rect.y
        w = head_rect.width
        h = head_rect.height
        eye_r = max(2, CELL_SIZE // 10)
        offset = max(3, CELL_SIZE // 6)

        # default: looking right
        left_eye = (ex + w - offset, ey + offset)
        right_eye = (ex + w - offset, ey + h - offset)

        try:
            from ..types import Direction

            if direction is Direction.UP:
                left_eye = (ex + offset, ey + offset)
                right_eye = (ex + w - offset, ey + offset)
            elif direction is Direction.DOWN:
                left_eye = (ex + offset, ey + h - offset)
                right_eye = (ex + w - offset, ey + h - offset)
            elif direction is Direction.LEFT:
                left_eye = (ex + offset, ey + offset)
                right_eye = (ex + offset, ey + h - offset)
            else:  # RIGHT
                left_eye = (ex + w - offset, ey + offset)
                right_eye = (ex + w - offset, ey + h - offset)
        except Exception:
            pass

        pg.draw.circle(self.screen, COLOR_SNAKE_EYE, left_eye, eye_r)
        pg.draw.circle(self.screen, COLOR_SNAKE_EYE, right_eye, eye_r)

    def draw_food(self, pos: GridPos) -> None:
        rect = pg.Rect(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pg.draw.rect(self.screen, COLOR_FOOD, rect)

    def draw_hud(self, score: int, high_score: int) -> None:
        msg = f"Score: {score}   High: {high_score}"
        surf = self.font.render(msg, True, COLOR_TEXT)
        self.screen.blit(surf, (8, 8))

    def draw_game_over(self, score: int, high_score: int) -> None:
        # Dim background
        overlay = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 160))  # semi-transparent black
        self.screen.blit(overlay, (0, 0))

        title = self.title_font.render("Game Over", True, COLOR_TEXT)
        info = self.font.render("Press R to Restart", True, COLOR_TEXT)
        score_surf = self.font.render(f"Score: {score}   High: {high_score}", True, COLOR_TEXT)

        # Center the messages
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        score_rect = score_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))
        info_rect = info.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))

        self.screen.blit(title, title_rect)
        self.screen.blit(score_surf, score_rect)
        self.screen.blit(info, info_rect)
