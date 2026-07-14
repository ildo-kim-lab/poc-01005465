"""crud.py에 대한 regression / safety 테스트.

각 테스트는 storage.DATA_FILE을 임시 경로로 monkeypatch하여
실제 data/todos.json에 영향을 주지 않는다.
"""

import storage
import crud


def use_temp_data_file(monkeypatch, tmp_path):
    monkeypatch.setattr(storage, "DATA_FILE", tmp_path / "todos.json")


# ----- Create -----


def test_create_assigns_incrementing_id(monkeypatch, tmp_path):
    use_temp_data_file(monkeypatch, tmp_path)

    first = crud.create_todo("첫 번째", "설명1")
    second = crud.create_todo("두 번째", "설명2")

    assert first["id"] == 1
    assert second["id"] == 2


def test_create_defaults_done_to_false(monkeypatch, tmp_path):
    use_temp_data_file(monkeypatch, tmp_path)

    todo = crud.create_todo("제목", "설명")

    assert todo["done"] is False


# ----- Read -----


def test_read_all_returns_all_created(monkeypatch, tmp_path):
    use_temp_data_file(monkeypatch, tmp_path)

    crud.create_todo("A", "a")
    crud.create_todo("B", "b")

    assert len(crud.read_all()) == 2


def test_find_by_id_returns_none_when_missing(monkeypatch, tmp_path):
    use_temp_data_file(monkeypatch, tmp_path)

    assert crud.find_by_id(999) is None


def test_search_by_keyword_matches_title_or_description(monkeypatch, tmp_path):
    use_temp_data_file(monkeypatch, tmp_path)

    crud.create_todo("장보기", "우유 사기")
    crud.create_todo("운동", "헬스장 가기")

    results = crud.search_by_keyword("우유")

    assert len(results) == 1
    assert results[0]["title"] == "장보기"


# ----- Update -----


def test_update_changes_only_given_fields(monkeypatch, tmp_path):
    use_temp_data_file(monkeypatch, tmp_path)

    todo = crud.create_todo("제목", "설명")

    updated = crud.update_todo(todo["id"], done=True)

    assert updated["title"] == "제목"
    assert updated["description"] == "설명"
    assert updated["done"] is True


def test_update_missing_id_returns_none(monkeypatch, tmp_path):
    use_temp_data_file(monkeypatch, tmp_path)

    assert crud.update_todo(999, title="x") is None


# ----- Delete -----


def test_delete_removes_only_target_record(monkeypatch, tmp_path):
    use_temp_data_file(monkeypatch, tmp_path)

    a = crud.create_todo("A", "a")
    b = crud.create_todo("B", "b")

    result = crud.delete_todo(a["id"])

    assert result is True
    remaining = crud.read_all()
    assert len(remaining) == 1
    assert remaining[0]["id"] == b["id"]


def test_delete_missing_id_returns_false_without_side_effects(monkeypatch, tmp_path):
    use_temp_data_file(monkeypatch, tmp_path)

    crud.create_todo("A", "a")

    result = crud.delete_todo(999)

    assert result is False
    assert len(crud.read_all()) == 1


# ----- Safety: 삭제된 id 재사용 금지 -----


def test_deleted_id_is_not_reused_after_new_create(monkeypatch, tmp_path):
    use_temp_data_file(monkeypatch, tmp_path)

    first = crud.create_todo("A", "a")
    second = crud.create_todo("B", "b")

    crud.delete_todo(second["id"])
    third = crud.create_todo("C", "c")

    assert third["id"] != first["id"]
    assert third["id"] != second["id"]
    assert third["id"] == 3


def test_delete_all_then_recreate_does_not_reuse_ids(monkeypatch, tmp_path):
    use_temp_data_file(monkeypatch, tmp_path)

    a = crud.create_todo("A", "a")
    b = crud.create_todo("B", "b")

    crud.delete_todo(a["id"])
    crud.delete_todo(b["id"])

    assert crud.read_all() == []

    c = crud.create_todo("C", "c")

    assert c["id"] not in (a["id"], b["id"])
