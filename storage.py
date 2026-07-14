"""JSON 파일 기반 데이터 저장/조회 계층."""

import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "todos.json"


def _default_state():
    return {"next_id": 1, "todos": []}


def load_state():
    if not DATA_FILE.exists():
        return _default_state()
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
