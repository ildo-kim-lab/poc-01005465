"""데이터 안전성(오삭제/오수정 방지, id 재사용 금지)에 대한 safety 테스트."""

import crud


def test_delete_removes_only_target_record(temp_data_file):
    a = crud.create_todo("A", "a")
    b = crud.create_todo("B", "b")

    crud.delete_todo(a["id"])

    remaining = crud.read_all()
    assert len(remaining) == 1
    assert remaining[0]["id"] == b["id"]


def test_delete_missing_id_returns_false_without_side_effects(temp_data_file):
    crud.create_todo("A", "a")

    result = crud.delete_todo(999)

    assert result is False
    assert len(crud.read_all()) == 1


def test_update_missing_id_returns_none_without_side_effects(temp_data_file):
    crud.create_todo("A", "a")

    result = crud.update_todo(999, title="x")

    assert result is None
    assert crud.read_all()[0]["title"] == "A"


def test_deleted_id_is_not_reused_after_new_create(temp_data_file):
    first = crud.create_todo("A", "a")
    second = crud.create_todo("B", "b")

    crud.delete_todo(second["id"])
    third = crud.create_todo("C", "c")

    assert third["id"] != first["id"]
    assert third["id"] != second["id"]
    assert third["id"] == 3


def test_delete_all_then_recreate_does_not_reuse_ids(temp_data_file):
    a = crud.create_todo("A", "a")
    b = crud.create_todo("B", "b")

    crud.delete_todo(a["id"])
    crud.delete_todo(b["id"])

    assert crud.read_all() == []

    c = crud.create_todo("C", "c")

    assert c["id"] not in (a["id"], b["id"])
