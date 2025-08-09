# Snake Game (pygame)

A classic Snake game implemented in Python using pygame. Grid-based movement, simple controls, and a clean, modular codebase with type hints.

## Requirements
- Python 3.10+
- Windows/macOS/Linux

## Quick start (Windows PowerShell)
From the project root:

```powershell
# Create virtual environment
python -m venv .venv

# Install dependencies (no need to activate)
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -r requirements.txt

# Run the game
.\.venv\Scripts\python -m snake_game
```

You can also activate the environment first if you prefer:

```powershell
.\.venv\Scripts\Activate.ps1
python -m snake_game
```

## Controls
- Arrow keys / WASD: Move
- R: Restart (after game over)
- Esc: Quit

## Project structure
```
snake_game/
  snake_game/
    __init__.py
    __main__.py          # Entry point, initializes App and loop
    config.py            # Game constants
    types.py             # Direction enum and core types
    core/
      __init__.py
      game.py            # Game state and orchestration
      snake.py           # Snake model and logic
      food.py            # Food placement
      input.py           # Input handling
      renderer.py        # Drawing grid/snake/food/HUD
  requirements.txt
  pyproject.toml         # Tooling config (black, ruff, isort, mypy, pytest)
  README.md
```

## Notes
- Fixed timestep update loop for deterministic simulation; rendering is decoupled.
- Snake uses deque for O(1) head/tail operations; set is used for O(1) occupancy checks.
- Code is typed; run mypy/ruff/black as needed (configured in `pyproject.toml`).

## Roadmap
- High score persistence (JSON)
- Sounds and custom font
- Packaging (console script already provided)
