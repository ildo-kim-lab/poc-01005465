"""JSON 파일 기반 데이터 저장/조회 계층."""

import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "todos.json"


def load_todos():
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_todos(todos):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)
