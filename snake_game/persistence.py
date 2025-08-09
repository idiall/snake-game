from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_HS_PATH = Path.home() / ".snake_game_highscore.json"


def load_high_score() -> int:
    try:
        if not _HS_PATH.exists():
            return 0
        data: Any
        with _HS_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and isinstance(data.get("high_score"), int):
            return int(data["high_score"])
    except Exception:
        # Corrupt or unreadable file; ignore and start fresh
        return 0
    return 0


def save_high_score(score: int) -> None:
    try:
        _HS_PATH.parent.mkdir(parents=True, exist_ok=True)
        with _HS_PATH.open("w", encoding="utf-8") as f:
            json.dump({"high_score": int(score)}, f)
    except Exception:
        # Best-effort; ignore write errors
        pass
