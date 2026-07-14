"""crud.py의 기본 CRUD 동작에 대한 regression 테스트."""

import crud


# ----- Create -----


def test_create_assigns_incrementing_id(temp_data_file):
    first = crud.create_todo("첫 번째", "설명1")
    second = crud.create_todo("두 번째", "설명2")

    assert first["id"] == 1
    assert second["id"] == 2


def test_create_defaults_done_to_false(temp_data_file):
    todo = crud.create_todo("제목", "설명")

    assert todo["done"] is False


# ----- Read -----


def test_read_all_returns_all_created(temp_data_file):
    crud.create_todo("A", "a")
    crud.create_todo("B", "b")

    assert len(crud.read_all()) == 2


def test_find_by_id_returns_none_when_missing(temp_data_file):
    assert crud.find_by_id(999) is None


def test_search_by_keyword_matches_title_or_description(temp_data_file):
    crud.create_todo("장보기", "우유 사기")
    crud.create_todo("운동", "헬스장 가기")

    results = crud.search_by_keyword("우유")

    assert len(results) == 1
    assert results[0]["title"] == "장보기"


# ----- Update -----


def test_update_changes_only_given_fields(temp_data_file):
    todo = crud.create_todo("제목", "설명")

    updated = crud.update_todo(todo["id"], done=True)

    assert updated["title"] == "제목"
    assert updated["description"] == "설명"
    assert updated["done"] is True


# ----- Delete -----


def test_delete_removes_target_record(temp_data_file):
    todo = crud.create_todo("A", "a")

    result = crud.delete_todo(todo["id"])

    assert result is True
    assert crud.read_all() == []
