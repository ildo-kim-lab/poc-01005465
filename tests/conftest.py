"""테스트 전반에서 사용하는 공용 fixture."""

import pytest

import storage


@pytest.fixture
def temp_data_file(monkeypatch, tmp_path):
    """실제 data/todos.json 대신 임시 경로를 사용하도록 격리한다."""
    monkeypatch.setattr(storage, "DATA_FILE", tmp_path / "todos.json")
