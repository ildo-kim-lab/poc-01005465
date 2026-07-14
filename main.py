"""JSON 파일 기반 할 일 목록 CRUD 콘솔 애플리케이션."""

import crud

MENU = """
===== 할 일 목록 관리 =====
1. 생성 (Create)
2. 전체 조회 (Read - 목록)
3. 검색 (Read - id/키워드)
4. 수정 (Update)
5. 삭제 (Delete)
0. 종료
===========================
"""


def print_todo(todo):
    status = "완료" if todo["done"] else "미완료"
    print(f"[{todo['id']}] {todo['title']} - {todo['description']} ({status})")


def handle_create():
    title = input("제목: ").strip()
    description = input("설명: ").strip()
    todo = crud.create_todo(title, description)
    print(f"생성되었습니다. (id={todo['id']})")


def handle_read_all():
    todos = crud.read_all()
    if not todos:
        print("등록된 할 일이 없습니다.")
        return
    for todo in todos:
        print_todo(todo)


def handle_search():
    keyword = input("검색할 id 또는 키워드를 입력하세요: ").strip()

    if keyword.isdigit():
        todo = crud.find_by_id(int(keyword))
        results = [todo] if todo else []
    else:
        results = crud.search_by_keyword(keyword)

    if not results:
        print("일치하는 할 일이 없습니다.")
        return
    for todo in results:
        print_todo(todo)


def handle_update():
    raw_id = input("수정할 항목의 id: ").strip()
    if not raw_id.isdigit():
        print("id는 숫자로 입력해야 합니다.")
        return

    todo = crud.find_by_id(int(raw_id))
    if todo is None:
        print("해당 id의 할 일이 없습니다.")
        return

    print_todo(todo)
    print("변경하지 않을 항목은 입력 없이 Enter를 누르세요.")

    title = input(f"제목 [{todo['title']}]: ").strip()
    description = input(f"설명 [{todo['description']}]: ").strip()
    done_input = input("완료 여부 (y/n) [입력 없으면 유지]: ").strip().lower()

    done = None
    if done_input == "y":
        done = True
    elif done_input == "n":
        done = False

    updated = crud.update_todo(
        todo["id"],
        title=title or None,
        description=description or None,
        done=done,
    )
    print("수정되었습니다.")
    print_todo(updated)


def handle_delete():
    raw_id = input("삭제할 항목의 id: ").strip()
    if not raw_id.isdigit():
        print("id는 숫자로 입력해야 합니다.")
        return

    todo_id = int(raw_id)
    todo = crud.find_by_id(todo_id)
    if todo is None:
        print("해당 id의 할 일이 없습니다.")
        return

    print_todo(todo)
    confirm = input("정말 삭제하시겠습니까? (y/n): ").strip().lower()
    if confirm != "y":
        print("삭제를 취소했습니다.")
        return

    crud.delete_todo(todo_id)
    print("삭제되었습니다.")


def main():
    actions = {
        "1": handle_create,
        "2": handle_read_all,
        "3": handle_search,
        "4": handle_update,
        "5": handle_delete,
    }

    while True:
        print(MENU)
        choice = input("메뉴 선택: ").strip()

        if choice == "0":
            print("프로그램을 종료합니다.")
            break

        action = actions.get(choice)
        if action is None:
            print("올바른 메뉴 번호를 입력하세요.")
            continue

        action()


if __name__ == "__main__":
    main()
