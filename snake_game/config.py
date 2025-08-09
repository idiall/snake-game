from __future__ import annotations

# Game configuration constants

# Screen and grid
CELL_SIZE: int = 24
GRID_COLS: int = 24
GRID_ROWS: int = 20
WIDTH: int = GRID_COLS * CELL_SIZE
HEIGHT: int = GRID_ROWS * CELL_SIZE
TITLE: str = "Snake Game"

# Timing
TICK_RATE: int = 6   # game logic updates per second (slower)
MAX_FPS: int = 60    # render frame cap

# Dynamic speed curve (score-based)
# Start at TICK_RATE, then every SPEED_SCORE_STEP points, increase by SPEED_STEP,
# capped at SPEED_MAX.
SPEED_STEP: int = 1
SPEED_SCORE_STEP: int = 5
SPEED_MAX: int = 14

# Colors (R, G, B)
COLOR_BG: tuple[int, int, int] = (18, 18, 18)
COLOR_GRID: tuple[int, int, int] = (28, 28, 28)
COLOR_SNAKE: tuple[int, int, int] = (40, 200, 120)
COLOR_SNAKE_HEAD: tuple[int, int, int] = (60, 220, 140)
COLOR_FOOD: tuple[int, int, int] = (220, 60, 60)
COLOR_TEXT: tuple[int, int, int] = (230, 230, 230)
COLOR_SNAKE_EYE: tuple[int, int, int] = (12, 12, 12)
